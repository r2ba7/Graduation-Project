import numpy as np
import serial, cv2, math, time


_SHOW_IMAGE = False
      
def gstreamer_pipeline(
    sensor_id=0,
    capture_width=1920,
    capture_height=1080,
    display_width=960,
    display_height=540,
    framerate=30,
    flip_method=2,
):
    return (
        "nvarguscamerasrc sensor-id=%d !"
        "video/x-raw(memory:NVMM), width=(int)%d, height=(int)%d, framerate=(fraction)%d/1 ! "
        "nvvidconv flip-method=%d ! "
        "video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! "
        "videoconvert ! "
        "video/x-raw, format=(string)BGR ! appsink"
        % (
            sensor_id,
            capture_width,
            capture_height,
            framerate,
            flip_method,
            display_width,
            display_height,
        )
    )

serial_port = serial.Serial(
    port="/dev/ttyTHS1",
    baudrate = 9600,
    bytesize = serial.EIGHTBITS, 
    parity = serial.PARITY_NONE,
    stopbits = serial.STOPBITS_ONE, 
    timeout = 1,
    xonxoff = False,
    rtscts = False,
    dsrdtr = False,
    writeTimeout = 2
    )

class HandCodedLaneFollower(object):

    def __init__(self, car=None):
        #logging.info('Creating a HandCodedLaneFollower...')
        self.car = car
        self.curr_steering_angle = 90
        self.dir = []

    def follow_lane(self, frame):
        # Main entry point of the lane follower
        #show_image("orig", frame)

        lane_lines, frame = detect_lane(frame)
        final_frame = self.steer(frame, lane_lines)

        return final_frame

    def steer(self, frame, lane_lines):
        #logging.debug('steering...')
        if len(lane_lines) == 0:
            #logging.error('No lane lines detected, nothing to do.')
            return frame

        new_steering_angle = compute_steering_angle(frame, lane_lines)
        self.curr_steering_angle = stabilize_steering_angle(self.curr_steering_angle, new_steering_angle, len(lane_lines))

        if self.car is not None:
            self.car.front_wheels.turn(self.curr_steering_angle)
        curr_heading_image = display_heading_line(frame, self.curr_steering_angle)
        #show_image("heading", curr_heading_image)

        return curr_heading_image


############################
# Frame processing steps
############################
def detect_edge(image):
    #(image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    # _, thresh = cv2.threshold(image, 150, 255, cv2.THRESH_BINARY)
    # blur = cv2.GaussianBlur(thresh,(9, 9), 0)
    # edges = cv2.Canny(blur, 200,400)
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    #show_image("hsv", hsv)
    sensitivity = 70
    lower_white = np.array([0,0,255-sensitivity], dtype=np.uint8)
    upper_white = np.array([255,sensitivity,255], dtype=np.uint8)
    mask = cv2.inRange(hsv, lower_white, upper_white)
    # (3, 3)
    blur = cv2.GaussianBlur(mask, (3, 3), 0)
    # imgHLS = cv2.cvtColor(image, cv2.COLOR_BGR2HLS)
    # lower = np.uint8([  0, 200,   0])
    # upper = np.uint8([255, 230, 255])
    # white_mask = cv2.inRange(imgHLS, lower, upper)
    # detect edges
    # 100-200
    edges = cv2.Canny(blur, 200, 400)
    return edges


def detect_lane(frame):
    #logging.debug('detecting lane lines...')

    edges = detect_edge(frame)
    #show_image('edges', edges)

    cropped_edges = region_of_interest(edges)
    #show_image('edges cropped', cropped_edges)

    line_segments = detect_line_segments(cropped_edges)
    line_segment_image = display_lines(frame, line_segments)
    #show_image("line segments", line_segment_image)

    lane_lines = average_slope_intercept(frame, line_segments)
    lane_lines_image = display_lines(frame, lane_lines)
    #show_image("lane lines", lane_lines_image)

    return lane_lines, lane_lines_image



def region_of_interest(canny):
    height, width = canny.shape
    mask = np.zeros_like(canny)

    # only focus bottom half of the screen

    polygon = np.array([[
        (0, height * 1 / 4),
        (width, height * 1 / 4),
        (width, height),
        (0, height),
    ]], np.int32)

    cv2.fillPoly(mask, polygon, 255)
    #show_image("mask", mask)
    masked_image = cv2.bitwise_and(canny, mask)
    return masked_image


def detect_line_segments(cropped_edges):
    # tuning min_threshold, minLineLength, maxLineGap is a trial and error process by hand
    rho = 1  # precision in pixel, i.e. 1 pixel
    angle = np.pi / 180  # degree in radian, i.e. 1 degree
    min_threshold = 10  # minimal of votes
    line_segments = cv2.HoughLinesP(cropped_edges, rho, angle, min_threshold, np.array([]), minLineLength=8,
                                    maxLineGap=4)

    #if line_segments is not None:
        #for line_segment in line_segments:
            #logging.debug('detected line_segment:')
            #logging.debug("%s of length %s" % (line_segment, length_of_line_segment(line_segment[0])))

    return line_segments


def average_slope_intercept(frame, line_segments):
    """
    This function combines line segments into one or two lane lines
    If all line slopes are < 0: then we only have detected left lane
    If all line slopes are > 0: then we only have detected right lane
    """
    # alpha1 = 0
    # alpha2 = 0
    # beta1 = 0
    # beta2 = 0   
    lane_lines = []
    if line_segments is None:
        #logging.info('No line_segment segments detected')
        return lane_lines

    height = frame.shape[0]
    width = frame.shape[1]
    left_fit = []
    right_fit = []

    boundary = 1/3
    left_region_boundary = width * (1 - boundary)  # left lane line segment should be on left 2/3 of the screen
    right_region_boundary = width * boundary # right lane line segment should be on left 2/3 of the screen

    for line_segment in line_segments:
        for x1, y1, x2, y2 in line_segment:
            if x1 == x2:
                #logging.info('skipping vertical line segment (slope=inf): %s' % line_segment)
                continue
            #if x1 == alpha1 or x2 == alpha2 or y1 == beta1 or y2 == beta2:
                #logging.info('skipping same lines: %s' % line_segment)
            fit = np.polyfit((x1, x2), (y1, y2), 1)
            slope = fit[0]
            intercept = fit[1]
            if slope < 0:
                if x1 < left_region_boundary and x2 < left_region_boundary:
                    left_fit.append((slope, intercept))
            else:
                if x1 > right_region_boundary and x2 > right_region_boundary:
                    right_fit.append((slope, intercept))
            # alpha1 = x1 
            # alpha2 = x2
            # beta1 = y1
            # beta2 = y2         

    left_fit_average = np.average(left_fit, axis=0)
    if len(left_fit) > 0:
        lane_lines.append(make_points(frame, left_fit_average))

    right_fit_average = np.average(right_fit, axis=0)
    if len(right_fit) > 0:
        lane_lines.append(make_points(frame, right_fit_average))

    #logging.debug('lane lines: %s' % lane_lines)  # [[[316, 720, 484, 432]], [[1009, 720, 718, 432]]]
    
    return lane_lines


def compute_steering_angle(frame, lane_lines):
    """ Find the steering angle based on lane line coordinate
        We assume that camera is calibrated to point to dead center
    """
    if len(lane_lines) == 0:
        #logging.info('No lane lines detected, do nothing')
        return -90

    height = frame.shape[0]
    width = frame.shape[1]
    if len(lane_lines) == 1:
        #logging.debug('Only detected one lane line, just follow it. %s' % lane_lines[0])
        x1, _, x2, _ = lane_lines[0][0]
        x_offset = x2 - x1
    else:
        _, _, left_x2, _ = lane_lines[0][0]
        _, _, right_x2, _ = lane_lines[1][0]
        camera_mid_offset_percent = 0.02 # 0.0 means car pointing to center, -0.03: car is centered to left, +0.03 means car pointing to right
        mid = int(width / 2 * (1 + camera_mid_offset_percent))
        x_offset = (left_x2 + right_x2) / 2 - mid

    # find the steering angle, which is angle between navigation direction to end of center line
    y_offset = int(height / 2)

    angle_to_mid_radian = math.atan(x_offset / y_offset)  # angle (in radian) to center vertical line
    angle_to_mid_deg = int(angle_to_mid_radian * 180.0 / math.pi)  # angle (in degrees) to center vertical line
    steering_angle = angle_to_mid_deg + 90  # this is the steering angle needed by picar front wheel

    #logging.debug('new steering angle: %s' % steering_angle)
    return steering_angle


def stabilize_steering_angle(curr_steering_angle, new_steering_angle, num_of_lane_lines, max_angle_deviation_two_lines=10, max_angle_deviation_one_lane=1):
    """
    Using last steering angle to stabilize the steering angle
    This can be improved to use last N angles, etc
    if new angle is too different from current angle, only turn by max_angle_deviation degrees
    """
    if num_of_lane_lines == 2 :
        # if both lane lines detected, then we can deviate more
        max_angle_deviation = max_angle_deviation_two_lines
    else :
        # if only one lane detected, don't deviate too much
        max_angle_deviation = max_angle_deviation_one_lane
    
    angle_deviation = new_steering_angle - curr_steering_angle
    if abs(angle_deviation) > max_angle_deviation:
        stabilized_steering_angle = int(curr_steering_angle
                                        + max_angle_deviation * angle_deviation / abs(angle_deviation))
    else:
        stabilized_steering_angle = new_steering_angle
    #logging.info('Proposed angle: %s, stabilized angle: %s' % (new_steering_angle, stabilized_steering_angle))
    return stabilized_steering_angle


############################
# Utility Functions
############################
def display_lines(frame, lines, line_color=(0, 255, 0), line_width=10):
    line_image = np.zeros_like(frame)
    if lines is not None:
        for line in lines:
            for x1, y1, x2, y2 in line:
                cv2.line(line_image, (x1, y1), (x2, y2), line_color, line_width)
    line_image = cv2.addWeighted(frame, 0.8, line_image, 1, 1)
    return line_image


def display_heading_line(frame, steering_angle, line_color=(0, 0, 255), line_width=5, ):
    heading_image = np.zeros_like(frame)
    height = frame.shape[0]
    width = frame.shape[1]

    # figure out the heading line from steering angle
    # heading line (x1,y1) is always center bottom of the screen
    # (x2, y2) requires a bit of trigonometry

    # Note: the steering angle of:
    # 0-89 degree: turn left
    # 90 degree: going straight
    # 91-180 degree: turn right 
    steering_angle_radian = steering_angle / 180.0 * math.pi
    x1 = int(width / 2)
    y1 = height
    x2 = int(x1 - height / 2 / math.tan(steering_angle_radian))
    y2 = int(height / 2)

    cv2.line(heading_image, (x1, y1), (x2, y2), line_color, line_width)
    heading_image = cv2.addWeighted(frame, 0.8, heading_image, 1, 1)

    return heading_image


def length_of_line_segment(line):
    x1, y1, x2, y2 = line
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def show_image(title, frame, show=_SHOW_IMAGE):
    if show:
        cv2.imshow(title, frame)


def make_points(frame, line):
    height = frame.shape[0]
    width = frame.shape[1]
    slope, intercept = line
    y1 = height  # bottom of the frame
    y2 = int(y1 * 1 / 2)  # make points from middle of the frame down

    # bound the coordinates within the frame
    x1 = max(-width, min(2 * width, int((y1 - intercept) / slope)))
    x2 = max(-width, min(2 * width, int((y2 - intercept) / slope)))
    return [[x1, y1, x2, y2]]

def main():
    direction = 'F'
    lane_follower = HandCodedLaneFollower()
    # For argus
    #cap = cv2.VideoCapture('filesrc location={} ! qtdemux ! queue ! h264parse ! omxh264dec ! nvvidconv ! video/x-raw,format=BGRx,width=640,height=480 ! queue ! videoconvert ! queue ! video/x-raw, format=BGR ! appsink'.format(filepath), cv2.CAP_GSTREAMER)
    cap = cv2.VideoCapture(gstreamer_pipeline(flip_method=2), cv2.CAP_GSTREAMER)
    i = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if ret == False:
            break
        Data_arr = []
        #frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
        #print('frame %s' % i )
        combo_image= lane_follower.follow_lane(frame)
        if lane_follower.curr_steering_angle >= 0 and lane_follower.curr_steering_angle <= 72:
           # lane_follower.dir.append('L')
            direction = 'L'
        elif lane_follower.curr_steering_angle >= 73 and lane_follower.curr_steering_angle <= 110:
            #lane_follower.dir.append('F')
            direction = 'F'
        elif lane_follower.curr_steering_angle >= 111 and lane_follower.curr_steering_angle <= 180:
          #  lane_follower.dir.append('R')
            direction = 'R'

        if len(lane_follower.dir) == 5:
            direction = max(set(lane_follower.dir), key = lane_follower.dir.count)
            lane_follower.dir = []
        final_image = cv2.putText(combo_image, str(lane_follower.curr_steering_angle) + " " + direction, (50,50), cv2.FONT_HERSHEY_SIMPLEX , 1 , (255, 0, 0)  , 2 , cv2.LINE_AA )
        cv2.imshow(WINDOW_NAME, final_image)
        Dir = '@{}'.format(direction)
        Data_arr.append(Dir)
        Data_arr = [''.join(Data_arr[:])][0]
        #UART Writing
        try:
            # Send a simple header
            serial_port.write("#".encode())
            while True:
                Data = Data_arr.encode()
                print(Data)
                serial_port.write(Data)
                serial_port.write("#\r\n".encode())
                break


        except KeyboardInterrupt:
            print("Exiting Program")

        except Exception as exception_error:
            continue

        i += 1

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()    
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
