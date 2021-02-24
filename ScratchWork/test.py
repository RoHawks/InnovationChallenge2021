from tf_pose.networks import get_graph_path
from tf_pose.estimator import TfPoseEstimator
import cv2
from tf_pose import common
import time
import numpy as np



input = "ScratchWork/person.jpg"
# estimate human poses from a single image !
image = common.read_imgfile(input, None, None)
w, h = 400, 400

e = TfPoseEstimator(get_graph_path("mobilenet_v2_small"), target_size=(w, h))
humans = e.inference(image, resize_to_default=True, upsample_size=4)

centers = {}
limbs = {}
for human in humans:
	for i in range(common.CocoPart.Background.value):
		if i not in human.body_parts.keys():
			continue

		body_part = human.body_parts[i]
		center = (int(body_part.x * w + 0.5), int(body_part.y * h + 0.5))
		centers[common.CocoPart(i)] = center

	for pair_order, pair in enumerate(common.CocoPairsRender):
		if pair[0] not in human.body_parts.keys() or pair[1] not in human.body_parts.keys():
			continue
		limbs["right"] = np.subtract(centers[common.CocoPart.RHip], centers[common.CocoPart.RKnee])
		limbs["left"] = np.subtract(centers[common.CocoPart.LHip], centers[common.CocoPart.LKnee])
		# npimg = cv2.line(npimg, centers[pair[0]], centers[pair[1]], common.CocoColors[pair_order], 3)

#raw_frame = TfPoseEstimator.draw_humans(raw_frame, humans, imgcopy=False)

# display FPS
cv2.putText(image,
            "cosine angle: " + str(limbs.get("right").dot(limbs.get("left")) / (np.linalg.norm(limbs.get("right")) * (np.linalg.norm(limbs.get("left"))))),
            (10, 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
            (0, 255, 0), 2)

# angles = {}

# for human in humans:
# 	for i in range(common.CocoPart.Background.value):
# 		if i not in human.body_parts.keys():
# 			continue

# 	human.body_parts[common.CocoPart.LHip]


out = TfPoseEstimator.draw_humans(image, humans, imgcopy=False)

cv2.imwrite('output.png', out)
