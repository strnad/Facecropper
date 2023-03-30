import os
import sys
import face_recognition
from PIL import Image

def crop_and_resize_images(input_path, output_path, offset=None, face_percentage=None, resize=None):
    if os.path.isfile(input_path):
        files = [input_path]
    elif os.path.isdir(input_path):
        files = [os.path.join(input_path, f) for f in os.listdir(input_path) if f.endswith(('.png', '.jpg', '.jpeg'))]
    else:
        print("Invalid input path")
        sys.exit(1)

    if not os.path.exists(output_path):
        os.makedirs(output_path)

    for file in files:
        image = face_recognition.load_image_file(file)
        face_locations = face_recognition.face_locations(image)

        if face_locations:
            top, right, bottom, left = face_locations[0]

            if offset:
                top -= offset[0]
                right += offset[1]
                bottom += offset[2]
                left -= offset[3]

            if face_percentage:
                h, w = bottom - top, right - left
                dh, dw = int(h * (face_percentage - 1) / 2), int(w * (face_percentage - 1) / 2)
                top -= dh
                right += dw
                bottom += dh
                left -= dw

            pil_image = Image.fromarray(image)
            pil_image = pil_image.crop((left, top, right, bottom))

            if resize:
                pil_image = pil_image.resize((resize, resize), Image.ANTIALIAS)

            output_filename = os.path.join(output_path, os.path.basename(file))
            pil_image.save(output_filename)
        else:
            print(f"No face detected in {file}")

input_path = "input_folder"  # or "input_file.jpg"
output_path = "output_folder"
offset = (10, 10, 10, 10)  # Optional: (top_offset, right_offset, bottom_offset, left_offset)
face_percentage = 1.5  # Optional: 1.5 means 150% of the original face size
resize = 200  # Optional: size in pixels

crop_and_resize_images(input_path, output_path, offset, face_percentage, resize)
