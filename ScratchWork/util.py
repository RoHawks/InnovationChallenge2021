import math
from tf_pose import common
import numpy as np

def calcTheta(humans):
	for human in humans:
		limbs = {}
		centers = {}
		for i in range(common.CocoPart.Background.value):
			if i not in human.body_parts.keys():
				continue

			body_part = human.body_parts[i]
			center = (body_part.x, body_part.y)
			centers[common.CocoPart(i)] = center

		for pair_order, pair in enumerate(common.CocoPairsRender): # not exactly sure why this is looping, isnt it just going to end up overwriting the dict? - forrest
			if pair[0] not in human.body_parts.keys() or pair[1] not in human.body_parts.keys():
				continue
			try:
				limbs["right"] = np.subtract(centers[common.CocoPart.RHip], centers[common.CocoPart.RKnee])
				limbs["left"] = np.subtract(centers[common.CocoPart.LHip], centers[common.CocoPart.LKnee])
			except KeyError:
				return 0 # if cant detect r or l hip

		return limbs.get("right").dot(limbs.get("left")) / (np.linalg.norm(limbs.get("right")) * (np.linalg.norm(limbs.get("left"))))
	return 0 # no humans in frame