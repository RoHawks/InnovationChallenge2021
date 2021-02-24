from tf_pose.networks import get_graph_path
from tf_pose.estimator import TfPoseEstimator
import cv2
from tf_pose import common
import time



input = "ScratchWork/person.jpg"
# estimate human poses from a single image !
image = common.read_imgfile(input, None, None)

e = TfPoseEstimator(get_graph_path("mobilenet_v2_small"), target_size=(400,400))
humans = e.inference(image, resize_to_default=True, upsample_size=4)

angles = {}

for human in humans:
    for i in range(common.CocoPart.Background.value):
        if i not in human.body_parts.keys():
            continue
		
	human.body_parts[common.CocoPart.LHip]


out = TfPoseEstimator.draw_humans(image, humans, imgcopy=False)

cv2.imshow('output', out)
cv2.waitKey(5)
time.sleep(10000)
