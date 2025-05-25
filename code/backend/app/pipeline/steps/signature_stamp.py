from PIL.Image import Image
import cv2
import numpy as np
import math


def find_signature_stamp(images: list[Image]) -> tuple[bool, bool]:
    res = [False, False]
    for image_PIL in images:
        image = np.array(image_PIL)
        hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)

        # Define blue color range in HSV for signatures and seals
        lower_blue = np.array([80, 14, 12])
        upper_blue = np.array([140, 255, 255])

        # Create a mask for blue regions
        mask = cv2.inRange(hsv, lower_blue, upper_blue)

        # Extract blue regions
        blue_regions = cv2.bitwise_and(image, image, mask=mask)

        # Convert to grayscale
        gray = cv2.cvtColor(blue_regions, cv2.COLOR_BGR2GRAY)

        # Apply Gaussian blur to reduce noise
        blurred = cv2.GaussianBlur(gray, (3, 3), 0)

        # Adaptive thresholding to binarize the image
        thresh = cv2.adaptiveThreshold(
            blurred,
            255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY_INV,
            11,
            2,
        )

        # Morphological operations to filter out printed text
        kernel = np.ones((3, 3), np.uint8)
        dilated = cv2.dilate(
            thresh, kernel, iterations=1
        )  # Restore handwritten shapes
        eroded = cv2.erode(
            dilated, kernel, iterations=2
        )  # Remove small printed text

        # Find external contours
        contours, _ = cv2.findContours(
            eroded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )

        # Minimum area threshold to filter out noise
        image_area = image.shape[0] * image.shape[1]
        min_area = 0.001 * image_area
        max_area = 0.03 * image_area

        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area > min_area and area < max_area:
                # Approximate contour to simplify shape
                epsilon = 0.02 * cv2.arcLength(cnt, True)
                approx = cv2.approxPolyDP(cnt, epsilon, True)

                # Compute bounding box
                _, _, w, h = cv2.boundingRect(approx)
                aspect_ratio = w / h if h != 0 else 0
                if aspect_ratio < 0.4 or aspect_ratio > 4:
                    continue

                # Calculate circularity
                perimeter = cv2.arcLength(approx, True)
                circularity = (
                    (4 * math.pi * area) / (perimeter**2)
                    if perimeter != 0
                    else 0
                )

                # Calculate contour complexity (perimeter-to-area ratio)
                complexity = perimeter / area if area > 0 else float("inf")

                # Compute stroke width variation for handwritten detection
                mask_contour = np.zeros_like(gray)
                cv2.drawContours(mask_contour, [approx], -1, 255, thickness=3)
                distances = cv2.distanceTransform(mask_contour, cv2.DIST_L2, 3)
                stroke_variation = (
                    np.std(distances[distances > 0])
                    if np.sum(distances > 0) > 0
                    else 0
                )

                if (
                    circularity > 0.41
                    and 0.9 < aspect_ratio < 1.3
                    and complexity < 0.3
                ):
                    res[1] = True
                elif (
                    stroke_variation > 0.6
                    and circularity < 0.6
                    and complexity > 0.03
                ):
                    res[0] = True
    return res
