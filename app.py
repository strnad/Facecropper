import cv2
import os
import sys
import argparse
import numpy as np

def crop_and_resize(input_path, output_path, offset_x=0, offset_y=0, face_percent=75, resize=None):
    net = cv2.dnn.readNetFromCaffe("models/deploy.prototxt", "models/res10_300x300_ssd_iter_140000_fp16.caffemodel")

    if os.path.isdir(input_path):
        images = [os.path.join(input_path, img) for img in os.listdir(input_path) if img.endswith(('.jpg', '.png', '.jpeg'))]
    elif os.path.isfile(input_path):
        images = [input_path]
    else:
        raise ValueError("Invalid input path")

    for img_path in images:
        img = cv2.imread(img_path)
        (h, w) = img.shape[:2]

        #add variable to keep track of face detection
        face_detected = False

        blob = cv2.dnn.blobFromImage(cv2.resize(img, (300, 300)), 1.0, (300, 300), (104.0, 177.0, 123.0))
        net.setInput(blob)
        detections = net.forward()

        for i in range(detections.shape[2]):
            confidence = detections[0, 0, i, 2]
            if confidence > 0.5:
                face_detected = True
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                (startX, startY, endX, endY) = box.astype("int")
                face = img[startY:endY, startX:endX]
                face_h, face_w = face.shape[:2]

                offsetX = int(face_w * offset_x / 100)
                offsetY = int(face_h * offset_y / 100)
                crop_startX = max(startX - offsetX, 0)
                crop_startY = max(startY - offsetY, 0)
                crop_endX = min(endX + offsetX, w)
                crop_endY = min(endY + offsetY, h)

                cropped_face = img[crop_startY:crop_endY, crop_startX:crop_endX]

                if resize:
                    cropped_face = cv2.resize(cropped_face, (resize, resize))

                output_file = os.path.join(output_path, os.path.basename(img_path))
                cv2.imwrite(output_file, cropped_face)


        # Print a message if no face was detected
        if not face_detected:
            print(f"No faces detected in {img_path}") 


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    #parser.add_argument("input_path", help="Path to the image file or folder containing images")
    #parser.add_argument("output_path", help="Path to the output folder")
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    #parser.add_argument("input_path", help="Path to the image file or folder containing images")
    #parser.add_argument("output_path", help="Path to the output folder")
    parser.add_argument("--offset_x", type=int, default=0, help="Percentage of horizontal offset around the face (default: 0)")
    parser.add_argument("--offset_y", type=int, default=0, help="Percentage of vertical offset around the face (default: 0)")
    parser.add_argument("--face_percent", type=int, default=75, help="Percentage of the face size in the cropped photo (default: 75)")
    parser.add_argument("--resize", type=int, default=512, help="Resize the output image to the specified size (default: 512)")

    args = parser.parse_args()

    crop_and_resize(
        input_path="_INPUT",
        output_path="_OUTPUT",
        offset_x=args.offset_x,
        offset_y=args.offset_y,
        face_percent=args.face_percent,
        resize=args.resize
    )
