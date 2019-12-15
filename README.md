# Sight-for-the-blind
A Computer Vision based project which uses yolo algorithm for object detection and google text to speech api to convert text lables of detected objects into speech. The purpose of this project is to help blind people to identify the object and to get an idea of the position of the object in front of them. 

The default speech language is english(en) but can be changed in to any language just by changing the lang parameter in function "tts = gTTS(description, lang='en')". 

Necessary Dependencies:

Install Google Text to Speech python3 library by using "pip3 install gTTS" command.

Install OpenCV 4.1.2 on linux from https://github.com/opencv/opencv/tree/4.1.2

Install darknet on linux follow the instruction in https://pjreddie.com/darknet/install/

Download and Install ffmpeg audio converter from :https://ffmpeg.org/releases/ffmpeg-4.2.1.tar.bz2

Download yolov3 weights : https://pjreddie.com/media/files/yolov3.weights


P.S: This project is expected to go through some performence improvements in near future.
