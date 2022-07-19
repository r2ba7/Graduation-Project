#!/usr/bin/python3
#
# Copyright (c) 2020, NVIDIA CORPORATION. All rights reserved.
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.
#

import jetson.inference
import jetson.utils
import argparse, cv2, sys, helper, serial, time
from lane_detection import *
from helperfunctions import *

#from time import perf_counter

# parse the command line
parser = argparse.ArgumentParser(description="Locate objects in a live camera stream using an object detection DNN.", 
                                 formatter_class=argparse.RawTextHelpFormatter, epilog=jetson.inference.detectNet.Usage() +
                                 jetson.utils.videoSource.Usage() + jetson.utils.videoOutput.Usage() + jetson.utils.logUsage())

parser.add_argument("input_URI", type=str, default="", nargs='?', help="URI of the input stream")
parser.add_argument("output_URI", type=str, default="", nargs='?', help="URI of the output stream")
parser.add_argument("--network", type=str, default="ssd-mobilenet-v2", help="pre-trained model to load (see below for options)")
parser.add_argument("--overlay", type=str, default="box,labels,conf", help="detection overlay flags (e.g. --overlay=box,labels,conf)\nvalid combinations are:  'box', 'labels', 'conf', 'none'")
parser.add_argument("--threshold", type=float, default=0.65, help="minimum detection threshold to use") 

is_headless = ["--headless"] if sys.argv[0].find('console.py') != -1 else [""]



try:
    opt = parser.parse_known_args()[0]
except:
    print("")
    parser.print_help()
    sys.exit(0)
    
net = jetson.inference.detectNet(opt.network, sys.argv, opt.threshold)
input = jetson.utils.videoSource(opt.input_URI, argv=sys.argv)
output = jetson.utils.videoOutput(opt.output_URI, argv=sys.argv + is_headless)

# UART
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

#time.sleep(1)
#End UART

# process frames until the user exits


#direction = 'F'
i = 0
# lane_follower = HandCodedLaneFollower()
# width, height = [], []
while True:
    # capture the next image
    img = input.Capture()
    detections = net.Detect(img, overlay="box,conf")
    # Convert from Cuda to BGR numpy array
    img_array = jetson.utils.cudaToNumpy(img)
    #print('shape of the image', img_array.shape)
    X, Y, _ = img.shape
    sep1 = img_array.shape[0]*0.3333
    sep2 = img_array.shape[0]*0.6667
    Data_arr = []
    #For loop start
    for detection in detections:

        #Detected labels
        if detection.ClassID == 1:
            label = 'P'
        #elif detection.ClassID == 2:
        else:
            label = 'C'
        #End detected labels

        #Position Handling
        position = position_handling(detection, sep1, sep2)
        #End Position Handling

        #Handle distance for both human and car because different sizes
        distance = distance_estimation(detection, img_array)
        #End Distance Handling
        #For UART
        Data = "{}{}{}-".format(str(distance), position, label)
        cv2.putText(img_array, position,
                    (int(detection.Right) - 35, int(detection.Top) + 40),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (255, 0, 0), 2)

        cv2.putText(img_array, str(label),
                    (int(detection.Left) + 20, int(detection.Top) + 40),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (125, 125, 255), 2)
                    
        cv2.putText(img_array, str(distance),
                    (int(detection.Left) + 20, int(detection.Bottom) - 40),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1, (0, 0, 255), 2)

        Data_arr.append(Data)
    # # #Lane Detection Part  
    # img_array = lane_follower.follow_lane(img_array)
    # if lane_follower.curr_steering_angle >= 0 and lane_follower.curr_steering_angle <= 85:
    #     dir = 'L'
    #         #direction = 'L'
    # elif lane_follower.curr_steering_angle >= 86 and lane_follower.curr_steering_angle <= 120:
    #     dir = 'F'
    #         #direction = 'F'
    # elif lane_follower.curr_steering_angle >= 121 and lane_follower.curr_steering_angle <= 180:
    #     dir = 'R'
    # # # #End Lane Detection Part
    # # # # str(lane_follower.curr_steering_angle) + " " + 
    # cv2.putText(img_array, str(dir), (50,50), cv2.FONT_HERSHEY_SIMPLEX , 1 , (255, 0, 0)  , 2 , cv2.LINE_AA )
    # # # #End Lane Detection  
    # # # #FPS
    # #Dir = '@{}{}'.format(direction, lane_follower.curr_steering_angle)
    # Dir = '@{}'.format(dir)
    # Data_arr.append(Dir)
    # Data_arr = [''.join(Data_arr[:])][0]
    # #UART Writing
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
        # print("Error occurred. Exiting Program")
        # print("Error: " + str(exception_error))
        continue
    #UART DONE

    #For Loop Ends
    i += 1
    img = jetson.utils.cudaFromNumpy(img_array)
    output.Render(img)
    # print out performance info
    #net.PrintProfilerTimes()

    # exit on input/output EOS
    if not input.IsStreaming() or not output.IsStreaming():
    #     serial_port.close()
        print(i)
        break
        
