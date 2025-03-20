import cv2
import numpy as np

def apply_filter(input_path, output_path, filter_type):
    try:
        image = cv2.imread(input_path)

        if image is None:
            print(f"⚠️ ERROR: Could not read image from {input_path}")
            return False

        print(f"✅ Applying filter: {filter_type} to {input_path}")

        if filter_type == "cartoon":
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            edges = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 9)
            color = cv2.bilateralFilter(image, 9, 300, 300)
            cartoon = cv2.bitwise_and(color, color, mask=edges)
            cv2.imwrite(output_path, cartoon)

        elif filter_type == "edge":
            edges = cv2.Canny(image, 100, 200)
            edges_colored = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)  # Convert to 3-channel
            cv2.imwrite(output_path, edges_colored)

        elif filter_type == "pencil":
            gray, sketch = cv2.pencilSketch(image, sigma_s=60, sigma_r=0.07, shade_factor=0.05)
            cv2.imwrite(output_path, sketch)

        elif filter_type == "grayscale":
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            cv2.imwrite(output_path, gray)

        elif filter_type == "sepia":
            sepia_filter = np.array([[0.272, 0.534, 0.131],
                                     [0.349, 0.686, 0.168],
                                     [0.393, 0.769, 0.189]])
            sepia_image = cv2.transform(image, sepia_filter)
            sepia_image = np.clip(sepia_image, 0, 255).astype(np.uint8)
            cv2.imwrite(output_path, sepia_image)

        elif filter_type == "invert":
            inverted = cv2.bitwise_not(image)
            cv2.imwrite(output_path, inverted)

        else:
            print(f"⚠️ WARNING: Unknown filter '{filter_type}', saving original image.")
            cv2.imwrite(output_path, image)

        print(f"✅ Filter applied successfully. Output saved to {output_path}")
        return True

    except Exception as e:
        print(f"⚠️ ERROR in filter processing: {str(e)}")
        return False
