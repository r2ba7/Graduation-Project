def position_handling(detection, sep1, sep2):
    """
    This function handles the position of the detected object.
    """
    #Sure Cases
    if detection.Right < sep1:
        position = 'L'        
    elif detection.Left > sep1 and detection.Right < sep2:
        position = 'F'
    elif detection.Left > sep2 and detection.Right > sep2:
        position = 'R'
    # elif detection.Right) > sep2 and detection.Left) < sep1:
    #     position = 'F'

    #End Sure Cases
    #Start Corner Cases
    #Handle Left and Forward Overlap
    if detection.Left < sep1 and detection.Right > sep1 and detection.Right < sep2: 
            thresh1 = detection.Right - sep1
            thresh2 = sep1 - detection.Left
            if thresh1 > thresh2:
                position = 'F'
            else:
                position = 'L'
    #End Overlap1
    #Handle Forward and Right Overlap            
    if detection.Left < sep2 and detection.Right > sep2:
        thresh1 = detection.Right - sep2
        thresh2 = sep2 - detection.Left
        if thresh1 > thresh2:
            position = 'R'
        else:
            position = 'F'
    return position
    #End Overlap2
    #End Corner Cases

def distance_estimation(detection, img):
    """
    This function estimates the distance of the detected object.
    """
    if detection.ClassID == 1:
        #Compare height for human
        #Y for human
        ratio = detection.Height/img.shape[1]
        if ratio > 0.65:
            distance = 'N'
        elif ratio > 0.3 and ratio < 0.65:
            distance = 'M' 
        elif ratio < 0.3:
            distance = 'F'
            #compare width for car
    else:
        ratio = detection.Width/img.shape[0]
        if ratio > 0.3:
            distance = 'N'
        elif ratio > 0.2 and ratio < 0.3:
            distance = 'M' 
        elif ratio < 0.2:
            distance = 'F'
    return distance