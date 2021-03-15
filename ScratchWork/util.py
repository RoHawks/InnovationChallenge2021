import math
from tf_pose import common
import numpy as np
from enum import Enum
from tf_pose.common import CocoPart


class Angle(Enum):  # the index for the angle with the joint centnered at name
    LElbow = 0
    LShoulder = 1
    LHip = 2
    LKnee = 3
    RElbow = 4
    RShoulder = 5
    RHip = 6
    RKnee = 7


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

        try:
            limbs["right"] = np.subtract(centers[common.CocoPart.RHip], centers[common.CocoPart.RKnee])
            limbs["left"] = np.subtract(centers[common.CocoPart.LHip], centers[common.CocoPart.LKnee])
        except KeyError:
            return 0  # if cant detect r or l hip

        return limbs.get("right").dot(limbs.get("left")) / (
                    np.linalg.norm(limbs.get("right")) * (np.linalg.norm(limbs.get("left"))))
    return 0  # no humans in frame


def cos(bp, point1, rootPoint, point2):
    try:
        x1 = bp[point1.value].x - bp[rootPoint.value].x
        y1 = bp[point1.value].y - bp[rootPoint.value].y
        x2 = bp[point2.value].x - bp[rootPoint.value].x
        y2 = bp[point2.value].y - bp[rootPoint.value].y

        magnitude1 = math.sqrt(x1 ** 2 + y1 ** 2)
        magnitude2 = math.sqrt(x2 ** 2 + y2 ** 2)

        dotProduct = x1 * x2 + y1 * y2

        return dotProduct / (magnitude1 * magnitude2)
    except KeyError:
        return None


def calcThetas(human):
    angle_vector = []
    bp = human.body_parts

    angle_vector.append(cos(bp, CocoPart.LWrist, CocoPart.LElbow, CocoPart.Neck))
    angle_vector.append(cos(bp, CocoPart.LElbow, CocoPart.Neck, CocoPart.LHip))
    angle_vector.append(cos(bp, CocoPart.Neck, CocoPart.LHip, CocoPart.LKnee))
    angle_vector.append(cos(bp, CocoPart.LHip, CocoPart.LKnee, CocoPart.LAnkle))

    angle_vector.append(cos(bp, CocoPart.RWrist, CocoPart.RElbow, CocoPart.Neck))
    angle_vector.append(cos(bp, CocoPart.RElbow, CocoPart.Neck, CocoPart.RHip))
    angle_vector.append(cos(bp, CocoPart.Neck, CocoPart.RHip, CocoPart.RKnee))
    angle_vector.append(cos(bp, CocoPart.RHip, CocoPart.RKnee, CocoPart.RAnkle))

    return angle_vector


def calcBodyThetas(humans):
    for human in humans:
        limbs = {}
        centers = {}
        bodyAngles = [(0, 12), (1, 12), (0, 2), (1, 4), (2, 3), (4, 5), (7, 10), (7, 8), (10, 11)]
        calcAngles = []
        for i in range(common.CocoPart.Background.value):
            if i not in human.body_parts.keys():
                continue

            body_part = human.body_parts[i]
            center = (body_part.x, body_part.y)
            centers[common.CocoPart(i)] = center
        limblabels = ["rightSN", "leftSN", "rightBicep", "rightArm", "leftBicep", "leftArm", "rightTorso", "rightThigh",
                      "rightShin", "leftTorso", "leftThigh", "leftShin", "face"]
        for pair_order, pair in enumerate(common.CocoPairsRender[0:13]):  # not exactly sure why this is looping, isnt
            # it just going to end up overwriting the dict? - forrest
            if pair[0] not in human.body_parts.keys() or pair[1] not in human.body_parts.keys():
                continue
            try:
                limbs[limblabels[pair_order]] = np.subtract(centers[pair[0]], centers[pair[1]])
            except KeyError:
                return 0  # if cant detect r or l hip
        for bodyangle in bodyAngles:
            calcAngles.append(limbs.get(limblabels[bodyangle[0]]).dot(limbs.get(bodyangle[1])) / (
                        np.linalg.norm(limbs.get(limblabels[bodyangle[0]])) * (
                    np.linalg.norm(limbs.get(limblabels[bodyangle[1]])))))
        return calcAngles
    return 0  # no humans in frame
