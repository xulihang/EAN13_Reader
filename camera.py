#coding=utf8
import read as reader
import argparse
import datetime
import time
import threading
import cv2


ap = argparse.ArgumentParser()
ap.add_argument("-i", "--index", type=int, default=0, help="camera index")
ap.add_argument("-f", "--fps", type=float, default=5.0, help="frame per second")
ap.add_argument("-vw", "--width", type=int, default=640, help="video width")
ap.add_argument("-vh", "--height", type=int, default=480, help="video height")
args = vars(ap.parse_args())

fps = args["fps"]
camera = cv2.VideoCapture(args["index"])
camera.set(cv2.CAP_PROP_FRAME_WIDTH,args["width"])
camera.set(cv2.CAP_PROP_FRAME_HEIGHT,args["height"])
size = (int(camera.get(cv2.CAP_PROP_FRAME_WIDTH)),
            int(camera.get(cv2.CAP_PROP_FRAME_HEIGHT)))
print('size:'+repr(size))


decoding = False

detected_frames = []

def decode(frame):
    global decoding
    decoding = True
    result_dict = reader.decode_image(frame)
    results = result_dict["results"]
    if len(results)>0:
        result = results[0]
        barcode_text = result["barcodeText"]
        print("Found barcode: "+barcode_text)
        img = show_detected_barcode_frame(frame,resized_width,resized_height,result)
        detected_frames.append(img)
    decoding = False
    

def show_detected_barcode_frame(frame, resized_width,resized_height, result):
    frame_clone=frame.copy()
    cv2.line(frame_clone,(result["x1"],result["y1"]),(result["x2"],result["y2"]),(0,255,0),3)
    cv2.line(frame_clone,(result["x2"],result["y2"]),(result["x3"],result["y3"]),(0,255,0),3)
    cv2.line(frame_clone,(result["x3"],result["y3"]),(result["x4"],result["y4"]),(0,255,0),3)
    cv2.line(frame_clone,(result["x4"],result["y4"]),(result["x1"],result["y1"]),(0,255,0),3)
    cv2.putText(frame_clone, "Text: {}".format(result["barcodeText"]), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
    resized_frame=cv2.resize(frame_clone,(resized_width,resized_height))
    return resized_frame

while True:
    start = time.time()
    grabbed, frame = camera.read()

    if grabbed == False:
        break
        
    end = time.time()
    
    seconds = end - start
    if seconds < 1.0 / fps:
        time.sleep(1.0 / fps - seconds)
    
    width=frame.shape[1]
    height=frame.shape[0]
    
    resized_width=640
    scale=resized_width/width
    resized_height=int(height*scale)
    resized = cv2.resize(frame, (resized_width, resized_height))
    
    if decoding == False:
        threading.Thread(target=decode, args=(resized,)).start()
    else:
        print("Still decoding. Skip this frame.")
    
    if len(detected_frames)>0:
        cv2.imshow("Detected Frame", detected_frames.pop(0))
    cv2.imshow("Video Stream", resized)
    
    key = cv2.waitKey(1) & 0xFF
    # if the `q` key is pressed, break from the lop
    if key == ord("q"):
        break

camera.release()
cv2.destroyAllWindows()