import decode as decoder
import detect as detector
import cv2
import numpy as np

if __name__ == "__main__":    
    image = cv2.imread("raw.jpg")
    candidates = detector.detect(image)
    for i in range(len(candidates)):
        candidate = candidates[i]
        cropped = candidate["cropped"]
        rect = candidate["rect"]
        box = cv2.boxPoints(rect) 
        box = np.int0(box)
        ean13, is_valid, thresh = decoder.decode(cropped)
        if is_valid:
            text = "Code: " + ean13
            cv2.line(image,(box[0][0],box[0][1]),(box[1][0],box[1][1]),(0,255,0),3)
            cv2.line(image,(box[1][0],box[1][1]),(box[2][0],box[2][1]),(0,255,0),3)
            cv2.line(image,(box[2][0],box[2][1]),(box[3][0],box[3][1]),(0,255,0),3)
            cv2.line(image,(box[3][0],box[3][1]),(box[0][0],box[0][1]),(0,255,0),3)
            cv2.putText(image, text, (5,50), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)
            cv2.imshow(str(i), image);
    cv2.waitKey(0);
    cv2.destroyAllWindows();
