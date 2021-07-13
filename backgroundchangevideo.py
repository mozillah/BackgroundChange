# import the necessary packages
from imutils.video import VideoStream
import argparse
# import datetime
from datetime import datetime,timedelta
import imutils
import time
import cv2
import os
import json
from os.path import join
from glob import glob




# # construct the argument parser and parse the arguments
# ap = argparse.ArgumentParser()
# ap.add_argument("-v", "--video", help="path to the video file")
# ap.add_argument("-a", "--min-area", type=int, default=100, help="minimum area size")
# ap.add_argument("-f", "--frames-length", type=int, default=5000, help="frame array length")
# ap.add_argument("-t", "--timespan", type=int, default=60, help="timespan to record video")
# args = vars(ap.parse_args())

def main(video="",output_video="",minarea="",framelength="",timespan=""):
	# if the video argument is None, then we are reading from webcam
	# def save_recording(video_name_,fps,width,height):
	# 	now = datetime.now()
	# 	# video_name = str(datetime.now().strftime("%Y-%m-%d %H-%M-%S")) + ".mp4"  
	# 	out = cv2.VideoWriter(video_name_,cv2.VideoWriter_fourcc('X','V','I','D'), fps, (width,height))
	# 	return out


	# if args.get("video", None) is None:
	# 	print("No input video is given...")
	# 	exit(0)
	# else:
	vs = cv2.VideoCapture(video)
	#initialize the first frame in the video stream

	firstFrame = None

	frame_width = int(vs.get(3))
	frame_height = int(vs.get(4))
	fps = vs.get(cv2.CAP_PROP_FPS)
	codec=vs.get(cv2.CAP_PROP_FOURCC)
	print(f"fps =={fps} , codec=={codec}")

	fourcc = cv2.VideoWriter_fourcc(*'mp4v')
	print(fourcc)
	print(f"fourcc=={codec}")
	fileTypes =('*.avi', '*.mp4','*.webm')

	# output_video = str(datetime.now().strftime("%Y-%m-%d %H-%M-%S"))+".mp4"
	# if args["video"][-4:] != ".smp":
	#     output_video = args["video"][:-4]+'finaltrack_output.avi'
	print(output_video)
	out = cv2.VideoWriter(output_video,cv2.VideoWriter_fourcc('X','V','I','D'), fps, (frame_width,frame_height))
	
	# out=save_recording(video_name_=output_video,fps=fps,width=frame_width,height=frame_height)
	# out = cv2.VideoWriter(output_video,cv2.VideoWriter_fourcc('M','J','P','G'), fps,(frame_width, frame_height))
	frameCount = 0
	disconnect_count=0
	frame = vs.read()
	frame = frame if vs is None else frame[1]
	print("""Please Select  ROI """)
	try:
		ROIs = cv2.selectROIs("frame", frame, False, False)
		x,y,w,h= ROIs[0]
	except:
		print("""No ROI is selected Closing""")
		exit(0)
	cv2.destroyWindow("frame")
	print(ROIs)
		
	while True:
		# grab the current frame and initialize the occupied/unoccupied text
		# if vs.isOpened():
		ret,frame = vs.read()
		if ret is False:
			break
		# frame = frame if frame is None else frame[1]
		print("frame")
		text = "Unoccupied"
		# if the frame could not be grabbed, then we have reached the end
		# of the video
		# resize the frame, convert it to grayscale, and blur it
		# frame = imutils.resize(frame, width=500)
		# imCrop = im[int(r[1]):int(r[1]+r[3]), int(r[0]):int(r[0]+r[2])]
		if frame is not None:
			gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
			gray = cv2.GaussianBlur(gray, (21, 21), 0)
			# if the first frame is None, initialize it
			if firstFrame is None:
				firstFrame = gray
				continue
			frameDelta = cv2.absdiff(firstFrame, gray)
			thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]
			# dilate the thresholded image to fill in holes, then find contours
			# on thresholded image
			firstFrame = gray
			thresh = cv2.dilate(thresh, None, iterations=2)
			imCrop = thresh[int(y):int(y + h), int(x):int(x + w)]
			cnts = cv2.findContours(imCrop.copy(), cv2.RETR_EXTERNAL,
				cv2.CHAIN_APPROX_SIMPLE)
			cnts = imutils.grab_contours(cnts)
			# loop over the contours
			for c in cnts:
				# if the contour is too small, ignore it
				if cv2.contourArea(c) < minarea:
					continue
				# compute the bounding box for the contour, draw it on the frame,
				# and update the text
				# (x, y, w, h) = cv2.boundingRect(c)
				text = "Occupied"
				timestamp = datetime.now()
			# cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
			cv2.imshow("Security Feed", frame)
			# cv2.imshow("Thresh", thresh)
			# cv2.imshow("Frame Delta", frameDelta)
		
		if frame is None:
			disconnect_count+=1
				
		# if disconnect_count > 20:
		# 	vs = cv2.VideoCapture(args["video"])
		# 	time.sleep(5)
		# 	disconnect_count = 0
		try:
			if frame is not None and text == "Occupied":
				print(timestamp)
				frameCount+=1
				print(frameCount)
				out.write(frame)
		except NameError:
			print("Ignore")
		# draw the text and timestamp on the frame
		# cv2.putText(frame, "Room Status: {}".format(text), (10, 20),
		# 	cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
		# cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
		# 	(10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
		# show the frame and record if the user presses a key

		# if frameCount > args["frames_length"] or frame is None:
		# if frameCount > framelength and frame is not None:
		# 	out.release()
		# 	cv2.waitKey(1000)
		# 	out=save_recording(video_name_=output_video,fps=fps,width=frame_width,height=frame_height)
		# 	frameCount = 0
		
		key = cv2.waitKey(1) & 0xFF
		# if the `q` key is pressed, break from the lop
		if key == ord("q"):
			break
	# cleanup the camera and close any open windows
	# if frame is None:
	vs.release()
	# vs.stop() if frame is None else vs.release()
	out.release() 
	cv2.destroyAllWindows()






if __name__ == "__main__":
    
	parser = argparse.ArgumentParser(description='Object Detection using YOLO in OPENCV')
	parser.add_argument('--image', help='Path to image file.')
	parser.add_argument("-v",'--video', help='Path to video file.')
	parser.add_argument('--folder', help='Path to video file')
	parser.add_argument("-a", "--min-area", type=int, default=100, help="minimum area size")
	parser.add_argument("-f", "--frames-length", type=int, default=5000, help="frame array length")
	parser.add_argument("-t", "--timespan", type=int, default=60, help="timespan to record video")
	args = vars(parser.parse_args())
	minarea=100
	framesLength=5000
	timespan=60
	if(args["min_area"]):
		minarea= args["min_area"]
	
	if(args["frames_length"]):
		framesLength= args["frames_length"]
	
	if(args["timespan"]):
		timespan= args["timespan"]
	fileTypes =('*.avi', '*.mp4','*.webm')
	args = parser.parse_args()
	if (args.video):
    # Open the video file
		if not os.path.isfile(args.video):
			print("Input video file ", args.video, " doesn't exist")
			sys.exit(1)
		video_name = args.video
		outputFile = video_name[:-4]+'output.avi'
		main(video=video_name,output_video=outputFile,minarea=minarea,framelength=framesLength,timespan=timespan)
	if (args.folder):
		if os.path.exists(args.folder):    
			files = []
			output_folder= join(args.folder, 'newumarfishtest')
			if not os.path.exists(output_folder):
				os.makedirs(output_folder)
			for ext in fileTypes:
				files.extend(glob(join(args.folder, ext)))
			for filepath in files:
				print(filepath)  
				if os.path.isfile(filepath):
					output_file = os.path.basename(filepath)
                    # outputFile = video_name[:-4]+'_output.avi'
					filename = os.path.basename(filepath)
					outfile  = filename[:-4]+'output.avi'
					output_file = join(output_folder, outfile)
					print("Input video file ",filepath)
					print(output_file)
					main(video=filepath,output_video=output_file,minarea=minarea,framelength=framesLength,timespan=timespan)

                    # main(video_name=filepath,output_video=output_file)
