# based off post https://learnopencv.com/deep-learning-based-human-pose-estimation-using-opencv-cpp-python/ 


import cv2
import numpy as np
# pre-trained model
protoFile = "poseNN/pose_deploy_linevec.prototxt"
weightsFile = "poseNN/pose_iter_440000.caffemodel"  # this is the COCO model
nPoints = 18
POSE_PAIRS = [[1, 0], [1, 2], [1, 5], [2, 3], [3, 4], [5, 6], [6, 7], [1, 8], [8, 9], [9, 10], [1, 11], [11, 12], [12, 13], [0, 14], [0, 15], [14, 16], [15, 17]]
threshold = 0.1

# Read the network into memory
net = cv2.dnn.readNetFromCaffe(protoFile, weightsFile)

def drawSkeleton(frame):
	# step 1: process input into a form understandable by the network
	height, width, chanels = frame.shape
	inWidth = 368
	inHeight = 368
	input = cv2.dnn.blobFromImage(frame, 1.0 / 255, (inWidth, inHeight), (0, 0, 0), swapRB=False, crop=False)

	# step 2: foward propogate through the ML network
	net.setInput(input)
	output = net.forward()

	H = output.shape[2]
	W = output.shape[3]

	# step 3: determine the skeleton based on the probability domain sfound by the networke

	# Empty list to store the detected keypoints
	points = []
	for i in range(nPoints):
		# confidence map of corresponding body's part.
		probMap = output[0, i, :, :]

		# Find global maxima of the probMap.
		minVal, prob, minLoc, point = cv2.minMaxLoc(probMap)

		# Scale the point to fit on the original image
		x = (width * point[0]) / W
		y = (height * point[1]) / H

		if prob > threshold:
			# Add the point to the list if the probability is greater than the threshold
			points.append((int(x), int(y)))
		else:
			points.append(None)

    # Draw Skeleton
    for pair in POSE_PAIRS:
        partA = pair[0]
        partB = pair[1]

        if points[partA] and points[partB]:
            cv2.line(frame, points[partA], points[partB], (0, 255, 255), 2)
            cv2.circle(frame, points[partA], 8, (0, 0, 255), thickness=-1, lineType=cv2.FILLED)

    # cv2.imshow('Output-Skeleton', frame)

    return frame
