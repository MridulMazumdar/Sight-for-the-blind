import numpy as np
import time
import cv2
import os
import imutils
import subprocess
from gtts import gTTS 
from pydub import AudioSegment
AudioSegment.converter = os.path.join(os.getcwd(),'ffmpeg')

LABELS = ['person',
'bicycle',
'car',
'motorbike',
'aeroplane',
'bus',
'train',
'truck',
'boat',
'traffic light',
'fire hydrant',
'stop sign',
'parking meter',
'bench',
'bird',
'cat',
'dog',
'horse',
'sheep',
'cow',
'elephant',
'bear',
'zebra',
'giraffe',
'backpack',
'umbrella',
'handbag',
'tie',
'suitcase',
'frisbee',
'skis',
'snowboard',
'sports ball',
'kite',
'baseball bat',
'baseball glove',
'skateboard',
'surfboard',
'tennis racket',
'bottle',
'wine glass',
'cup',
'fork',
'knife',
'spoon',
'bowl',
'banana',
'apple',
'sandwich',
'orange',
'broccoli',
'carrot',
'hot dog',
'pizza',
'donut',
'cake',
'chair',
'sofa',
'pottedplant',
'bed',
'diningtable',
'toilet',
'tvmonitor',
'laptop',
'mouse',
'remote',
'keyboard',
'cell phone',
'microwave',
'oven',
'toaster',
'sink',
'refrigerator',
'book',
'clock',
'vase',
'scissors',
'teddy bear',
'hair drier',
'toothbrush']


net = cv2.dnn.readNetFromDarknet(os.path.join(os.getcwd(),'yolov3.cfg'),os.path.join(os.getcwd(),'yolov3.weights') ) 

ln = net.getLayerNames()
ln = [ln[i[0] - 1] for i in net.getUnconnectedOutLayers()]


cap = cv2.VideoCapture(0)
frame_count = 0
start = time.time()
first = True
frames = []

while (True):


	frame_count += 1
	ret, frame = cap.read()
	frame = cv2.flip(frame,1)
	frames.append(frame)

	if frame_count == 300:
		break
	if ret:
		key = cv2.waitKey(1)
		if frame_count % 60 == 0:
			end = time.time()
			
			(H, W) = frame.shape[:2]
			
			blob = cv2.dnn.blobFromImage(frame, 1 / 255.0, (416, 416),
				swapRB=True, crop=False)
			net.setInput(blob)
			layerOutputs = net.forward(ln)

			
			boxes = []
			confidences = []
			classIDs = []
			centers = []

			
			for output in layerOutputs:
				
				for detection in output:
					
					scores = detection[5:]
					classID = np.argmax(scores) 
					confidence = scores[classID]

					
					if confidence > 0.5:
						
						box = detection[0:4] * np.array([W, H, W, H])
						(centerX, centerY, width, height) = box.astype("int")

						
						x = int(centerX - (width / 2))
						y = int(centerY - (height / 2))

						
						boxes.append([x, y, int(width), int(height)])
						confidences.append(float(confidence))
						classIDs.append(classID)
						centers.append((centerX, centerY))

			
			idxs = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.3)

			texts = []

			
			if len(idxs) > 0:
				
				for i in idxs.flatten():
				
					centerX, centerY = centers[i][0], centers[i][1]
					
					if centerX <= W/3:
						W_pos = "left "
					elif centerX <= (W/3 * 2):
						W_pos = "center "
					else:
						W_pos = "right "
					
					if centerY <= H/3:
						H_pos = "top "
					elif centerY <= (H/3 * 2):
						H_pos = "mid "
					else:
						H_pos = "bottom "

					texts.append(H_pos + W_pos + LABELS[classIDs[i]])

			print(texts)
			
			if texts:
				description = ', '.join(texts)
				tts = gTTS(description, lang='en')
				tts.save('tts.mp3')
				tts = AudioSegment.from_mp3("tts.mp3")
				subprocess.call(["ffplay", "-nodisp", "-autoexit", "tts.mp3"])
	cv2.imshow('frame',frame)
	if cv2.waitKey(0) & 0xFF == ord('q'):
		break		
	 


	 
cap.release()
cv2.destroyAllWindows()
