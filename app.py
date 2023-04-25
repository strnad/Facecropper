import os
import cv2
import numpy as np
import argparse
from PIL import Image
from io import BytesIO
from PIL import ImageCms

def detect_faces(image, net,threshold):
    (h, w) = image.shape[:2]
    blob = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)), 1.0, (300, 300), (104.0, 177.0, 123.0))
    net.setInput(blob)
    detections = net.forward()
    faces = []
    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > threshold:
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")
            faces.append((startX, startY, endX, endY))
    return faces


def process_image(image, face, offset_x, offset_y, face_percent, resize):
    (startX, startY, endX, endY) = face
    face_width = endX - startX
    face_height = endY - startY

    centerX = startX + face_width // 2
    centerY = startY + face_height // 2

    # Calculate the offset pixels related to the resized square image
    offsetX = int(face_width * (-offset_x / 100))
    offsetY = int(face_height * (-offset_y / 100))

    # Adjust the offsets to the maximum possible value within image bounds
    img_height, img_width = image.shape[:2]
    adjusted_offsetX = max(min(offsetX, img_width - centerX - face_width // 2), -centerX + face_width // 2)
    adjusted_offsetY = max(min(offsetY, img_height - centerY - face_height // 2), -centerY + face_height // 2)

    if offsetX != adjusted_offsetX or offsetY != adjusted_offsetY:
        print(f"Desired offsets (x: {offsetX}, y: {offsetY}) exceed image boundaries. "
              f"Using adjusted offsets (x: {adjusted_offsetX}, y: {adjusted_offsetY}) instead.")

    centerX += adjusted_offsetX
    centerY += adjusted_offsetY

    new_width = int(face_width / (face_percent / 100))
    new_height = new_width

    half_width = new_width // 2
    half_height = new_height // 2

    # Calculate the maximum possible face percentage within image bounds
    max_face_percent_x = (img_width - abs(adjusted_offsetX * 2)) / face_width * 100
    max_face_percent_y = (img_height - abs(adjusted_offsetY * 2)) / face_height * 100
    max_face_percent = min(max_face_percent_x, max_face_percent_y)

    # Adjust the new_width and new_height based on the maximum face percentage
    if face_percent > max_face_percent:
        face_percent = max_face_percent
        new_width = int(face_width / (face_percent / 100))
        new_height = new_width
        half_width = new_width // 2
        half_height = new_height // 2

    # Calculate the minimum possible face percentage to avoid distortion
    min_face_percent = max(face_width / img_width * 100, face_height / img_height * 100)

    # Adjust the new_width and new_height based on the minimum face percentage
    if face_percent < min_face_percent:
        face_percent = min_face_percent
        new_width = int(face_width / (face_percent / 100))
        new_height = new_width
        half_width = new_width // 2
        half_height = new_height // 2

    # Check for necessary variables and adjust if needed
    left_bound = max(centerX - half_width, 0)
    right_bound = min(centerX + half_width, img_width)
    top_bound = max(centerY - half_height, 0)
    bottom_bound = min(centerY + half_height, img_height)

    # Crop the image
    cropped_image = image[top_bound:bottom_bound, left_bound:right_bound]

    # Resize the image
    resized_image = cv2.resize(cropped_image, (resize, resize), interpolation=cv2.INTER_AREA)

    return resized_image

                               
def convert_to_srgb(pil_image,print_info=False):
    # Load the sRGB ICC profile
    srgb_profile = ImageCms.createProfile("sRGB")

    # Check if the image has an embedded ICC profile
    if "icc_profile" in pil_image.info:
        input_icc_profile = ImageCms.ImageCmsProfile(BytesIO(pil_image.info["icc_profile"]))
        transform = ImageCms.buildTransform(input_icc_profile, srgb_profile, "RGB", "RGB")
        srgb_image = ImageCms.applyTransform(pil_image, transform)
        if print_info:
            print("Converted image to sRGB color space.")
    else:
        # If the image does not have an embedded ICC profile, assume it is already in sRGB        
        srgb_image = pil_image
        if print_info:
            print("Image does not have an embedded ICC profile. Assuming it is already in sRGB color space.")

    return srgb_image

def main(input_folder, output_folder, offset_x, offset_y, face_percent, resize, threshold,output_format):
    model = "models/res10_300x300_ssd_iter_140000_fp16.caffemodel"
    proto = "models/deploy.prototxt"

    net = cv2.dnn.readNetFromCaffe(proto, model)

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for file in os.listdir(input_folder):
        if file.lower().endswith((".jpg", ".jpeg", ".png")):
            image_path = os.path.join(input_folder, file)            
            pilimage = Image.open(image_path) 
            pilimageSrgb = convert_to_srgb(pilimage,print_info=True) #convert to sRGB color space
            image = np.array(pilimageSrgb) #convert to numpy array
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)  # Convert from RGB to BGR
            faces = detect_faces(image, net, threshold)
            if len(faces) == 0:
                print(f"\nNo face detected in {file}. Skipping file.")
            else:
                for i, face in enumerate(faces):
                    processed_image = process_image(image, face, offset_x, offset_y, face_percent, resize)
                    output_path = os.path.join(output_folder, f"{os.path.splitext(file)[0]}_face_{i}.{output_format}")
                    cv2.imwrite(output_path, processed_image)
                    print(f"\nProcessed {file} and saved face {i} to {output_path}.")
        else:
            print(f"\nUnsupported file format {file}. Skipping file.")

def run_cli():
    parser = argparse.ArgumentParser(description="Face detection and cropping")
    parser.add_argument("--input_folder", type=str, default="_INPUT", help="Input folder containing images")
    parser.add_argument("--output_folder", type=str, default="_OUTPUT", help="Output folder for processed images")
    parser.add_argument("--offset_x", type=float, default=00.0, help="Horizontal offset of face center")
    parser.add_argument("--offset_y", type=float, default=-10.0, help="Vertical offset of face center")
    parser.add_argument("--face_percent", type=float, default=40.0, help="Size of face in the resulting photo as a percentage")
    parser.add_argument("--resize", type=int, default=512, help="Size of the output image")
    parser.add_argument("--threshold", type=float, default=0.5, help="Threshold of face detection (0-1)")
    parser.add_argument("--output_format", type=str, default="jpg", help="Output format (jpg, png, etc.")    
    args = parser.parse_args()

    main(args.input_folder, args.output_folder, args.offset_x, args.offset_y, args.face_percent, args.resize, args.threshold, args.output_format)

if __name__ == "__main__":
    run_cli()