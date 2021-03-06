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


import sys
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


	def run(self):
		""" contains main while loop to constantly capture webcam, process, and output

		:return: None
		"""
		input = "ScratchWork/person.jpg"

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
				image = common.read_imgfile(input, None, None)

				#raw_frame = cv2.flip(raw_frame, 1)

				# STEP 2: process frames
				if raw_frame is None:
					continue

				humans = e.inference(raw_frame, resize_to_default=True, upsample_size=4)
				testhuman = e.inference(image, resize_to_default=True, upsample_size=4)

				# display FPS
				cv2.putText(raw_frame,
							"cosine angles: " + str(calcThetas(humans) + " " + compareBodies(calcThetas(humans[0]), calcThetas(testhuman[0]))),
							(10, 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
							(0, 255, 0), 2)
				fps_time = time.time()

				# convert frame to RGB
				color_frame = cv2.cvtColor(raw_frame, cv2.COLOR_BGR2RGB)

				# add alpha channel
				out_frame_rgba = np.zeros(
					(self.height, self.width, 4), np.uint8)
				out_frame_rgba[:, :, :3] = color_frame
				out_frame_rgba[:, :, 3] = 255

				# STEP 3: send to virtual camera
				# virtual_cam.send(out_frame_rgba)
				virtual_cam.send(out_frame_rgba)
				virtual_cam.sleep_until_next_frame()


# run program
if __name__ == '__main__':
	try:
		instance = Control()
		# instance.logger.startTimer()
		instance.run()
		# instance.logger.endTimer()
	except Exception as e:
		print("Something went wrong" + str(e))
		print(e)
	except:
		print("general error")
