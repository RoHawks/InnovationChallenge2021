from tf_pose.networks import get_graph_path
from tf_pose.estimator import TfPoseEstimator
import cv2
from tf_pose import common
import time
import numpy as np
from util import calcThetas
from util import Angle



input = "ScratchWork/person.jpg"
# estimate human poses from a single image !
image = common.read_imgfile(input, None, None)
w, h = 400, 400

e = TfPoseEstimator(get_graph_path("mobilenet_v2_small"), target_size=(w, h))
humans = e.inference(image, resize_to_default=True, upsample_size=4)

centers = {}

#raw_frame = TfPoseEstimator.draw_humans(raw_frame, humans, imgcopy=False)

# display FPS

# angles = {}

measures = calcThetas(humans[0])
y = 10
for angle in Angle:
	out = str(angle.name) + ": " + str(measures[angle.value])[:5]
	cv2.putText(image,
            out,
            (10, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
            (0, 255, 0), 2)
	y += 20

# for human in humans:
# 	for i in range(common.CocoPart.Background.value):
# 		if i not in human.body_parts.keys():
# 			continue

# 	human.body_parts[common.CocoPart.LHip]


out = TfPoseEstimator.draw_humans(image, humans, imgcopy=False)

cv2.imwrite('output.png', out)
