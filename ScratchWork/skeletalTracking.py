import cv2
# Specify the paths for the 2 files
protoFile = "poseNN/pose_deploy_linevec_faster_4_stages.prototxt"
weightsFile = "poseNN/pose_iter_160000.caffemodel" # this is the COCO model

# Read the network into Memory
net = cv2.dnn.readNetFromCaffe(protoFile, weightsFile)

def identifySkeleton(img, keee=4):
	a = img
	return img
