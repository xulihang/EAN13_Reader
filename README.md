# EAN13-Reader

EAN13 1D Barcode Reader

Files explaination:

* `decode.py`: decode barcode images using a simlar edge distance algorithm to increase tolerance
* `decode-simple.py`: decode simple barcode images
* `detect.py`: detect possible barcode areas in an image using a basic contours finding method
* `read.py`: read the barcodes in an image
* `camera.py`: read the barcodes from camera stream

## Install

1. Install Python
2. Install dependencies:

    ```
    pip install -r requirements.txt
    ```

## Workflow

The program first detects possible barcode areas and then tries to decode them. Here are the specific workflows of detection and decoding.

Detection workflow:

1. Transform the image to grayscale 
2. Thresholding
3. Invert
4. Dilate
5. Find contours and filter out small contours
6. Get the min area rects of contours, crop and rotate them before sending them to decode

Decoding workflow:

1. Transform the image to grayscale 
2. Thresholding
3. The decoding is done line by line from the bottom. It will read bars and decode their patterns following the EAN13 specification

## Benchmark

The reader is integrated in the [barcode performacne test tool](https://github.com/xulihang/Barcode-Reading-Performance-Test).

## References

* https://www.dcode.fr/barcode-ean13
* https://mark-borg.github.io/blog/2016/barcode-reader/
* https://github.com/zchrissirhcz/ean13-barcode-recognition
* https://www.ijser.org/researchpaper/Robust-Algorithm-for-Developing-Barcode-Recognition-System-using-Web-cam.pdf
* [Locating and Decoding EAN-13 Barcodes from Images Captured by Digital Cameras](http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.941.3486&rep=rep1&type=pdf)


