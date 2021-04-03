import cv2
import pyvirtualcam
import numpy as np
#from pynput import keyboard
from tf_pose import common
from tf_pose.estimator import TfPoseEstimator
from tf_pose.networks import get_graph_path, model_wh
import time
from tf_pose.common import CocoPart
from util import calcThetas
from comparator import compareBodies
import json
from video_filter import Filter

class Control:
    """ main class for this project. Starts webcam capture and sends output to virtual camera"""

    def __init__(self, webcam_source=1, width=640, height=480, fps=30):
        """ sets user preferences for resolution and fps, starts webcam capture

        :param webcam_source: webcam source 0 is the laptop webcam and 1 is the usb webcam
        :type webcam_source: int
        :param width: width of webcam stream
        :type width: int
        :param height: height of webcam stream
        :type height: int
        :param fps: fps of videocam stream
        :type fps: int
        """
        self.webcam_source = webcam_source

        # initialize webcam capture
        self.cam = cv2.VideoCapture(self.webcam_source)
        self.cam.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.cam.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        self.cam.set(cv2.CAP_PROP_FPS, fps)

        # Query final capture device values (different from what i set??)
        # save as object variables
        self.width = int(self.cam.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.cam.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.fps = self.cam.get(cv2.CAP_PROP_FPS)

        # print out status
        print('webcam capture started ({}x{} @ {}fps)'.format(self.width,
                                                              self.height, self.fps))


        # filter object
        self.videofilter = Filter(self.width, self.height)

    # self.logger = logger.Logger()


    def getangles(self):
        """ contains main while loop to constantly capture webcam, process, and output

        :return: None
        """
        user = "tester"

        with pyvirtualcam.Camera(width=self.width, height=self.height, fps=self.fps) as virtual_cam:
            virtual_cam.delay = 0
            fps_time = 0
            frame_count = 0

            e = TfPoseEstimator(get_graph_path("mobilenet_v2_small"), target_size=(self.width, self.height))

            print(f'virtual camera started ({virtual_cam.width}x{virtual_cam.height} @ {virtual_cam.fps}fps)')
            print('TfPoseEstimator loaded')

            while True:
                frame_count += 1

                # STEP 1: capture video from webcam

                ret, raw_frame = self.cam.read()

                # STEP 2: process frames
                if raw_frame is None:
                    continue

                humans = e.inference(raw_frame, resize_to_default=True, upsample_size=4)
                return str(calcThetas(humans))