import decode as decoder
import detect as detector
import cv2
import numpy as np

def decode_image(image):
    result_dict = {}
    results = []        
    
    candidates = detector.detect(image)
    for i in range(len(candidates)):
        candidate = candidates[i]
        cropped = candidate["cropped"]
        rect = candidate["rect"]
        box = cv2.boxPoints(rect) 
        box = np.int0(box)
        ean13, is_valid, thresh = decoder.decode(cropped)
        if is_valid:
            result = {}
            result["barcodeFormat"] = "EAN13"
            result["barcodeText"] = ean13
            result["x1"] = int(box[0][0])
            result["y1"] = int(box[0][1])
            result["x2"] = int(box[1][0])
            result["y2"] = int(box[1][1])
            result["x3"] = int(box[2][0])
            result["y3"] = int(box[2][1])
            result["x4"] = int(box[3][0])
            result["y4"] = int(box[3][1])
            results.append(result)

    result_dict["results"] = results
    return result_dict

if __name__ == "__main__":
    image = cv2.imread("multiple.jpg")
    result_dict = decode_image(image)
    results = result_dict["results"]
    text = "No barcode found"
    if len(results) > 0:
        for result in results:
            if text == "No barcode found":
                text = "Code: "
            ean13 = result["barcodeText"]
            text = text + ean13 + " "
            cv2.line(image,(result["x1"],result["y1"]),(result["x2"],result["y2"]),(0,255,0),3)
            cv2.line(image,(result["x2"],result["y2"]),(result["x3"],result["y3"]),(0,255,0),3)
            cv2.line(image,(result["x3"],result["y3"]),(result["x4"],result["y4"]),(0,255,0),3)
            cv2.line(image,(result["x4"],result["y4"]),(result["x1"],result["y1"]),(0,255,0),3)
    scale_percent = 640/image.shape[1]       
    width = int(image.shape[1] * scale_percent)
    height = int(image.shape[0] * scale_percent)
    dim = (width, height)
    resized = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)
    cv2.putText(resized, text, (5,50), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)
    cv2.imshow("result", resized);
    cv2.waitKey(0);
    cv2.destroyAllWindows();
