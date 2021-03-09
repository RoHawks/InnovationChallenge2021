import math
from tf_pose import common
import numpy as np

def calcLegTheta(humans):
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

def calcBodyThetas(humans):
	for human in humans:
		limbs = {}
		centers = {}
		bodyAngles = [(0,12), (1,12), (0,2), (1, 4), (2, 3), (4, 5), (7, 10), (7, 8), (10, 11)]
		calcAngles = []
		for i in range(common.CocoPart.Background.value):
			if i not in human.body_parts.keys():
				continue

			body_part = human.body_parts[i]
			center = (body_part.x, body_part.y)
			centers[common.CocoPart(i)] = center
		limblabels = ["rightSN, leftSN, rightBicep, rightArm, leftBicep, leftArm, rightTorso, rightThigh, rightShin, leftTorso, leftThigh, leftShin, face"]
		for pair_order, pair in enumerate(common.CocoPairsRender[0:13]): # not exactly sure why this is looping, isnt it just going to end up overwriting the dict? - forrest
			if pair[0] not in human.body_parts.keys() or pair[1] not in human.body_parts.keys():
				continue
			try:
				limbs[limblabels[pair_order]] = np.subtract(centers[pair[0]], centers[pair[1]])
			except KeyError:
				return 0 # if cant detect r or l hip
		for bodyangle in bodyAngles:
			calcAngles.append(limbs.get(limblabels[bodyangle[0]]).dot(limbs.get(bodyangle[1])) / (np.linalg.norm(limbs.get(limblabels[bodyangle[0]])) * (np.linalg.norm(limbs.get(limblabels[bodyangle[1]])))))
		return calcAngles
	return 0 # no humans in frame
