import numpy as np
import cv2

from PIL import Image

def preprocess_image(image_path, threshold=128):
    img = Image.open(image_path).convert('L')
    img = np.array(img)
    
    _, binary_img = cv2.threshold(img, threshold, 255, cv2.THRESH_BINARY)
    
    return binary_img

def extract_contours(binary_img):
    contours, _ = cv2.findContours(binary_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    return contours

def generate_gcode_from_contours(contours, start_position=(0, 0), feed_rate=1000):
    gcode = []
    
    gcode.append(f"G0 X{start_position[0]} Y{start_position[1]} F{feed_rate}")
    
    for contour in contours:
        for point in contour:
            x, y = point[0]
            gcode.append(f"G1 X{x} Y{y} F{feed_rate}")
    
    gcode.append("M30")
    
    return gcode

def save_gcode(gcode, output_filename):
    with open(output_filename, 'w') as file:
        file.write("\n".join(gcode))

def convert_image_to_gcode(image_path, output_filename, threshold=128, feed_rate=1000):
    binary_img = preprocess_image(image_path, threshold)
    
    contours = extract_contours(binary_img)
    gcode = generate_gcode_from_contours(contours, feed_rate=feed_rate)
    
    save_gcode(gcode, output_filename)
    print(f"G-code saved to {output_filename}")

if __name__ == "__main__":
    image_path = "input_image.png"
    output_filename = "output.gcode"
    
    convert_image_to_gcode(image_path, output_filename)
