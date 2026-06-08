import cv2
import numpy as np

class Transitions:
    @staticmethod
    def cross_dissolve_blur(frame_a: np.ndarray, frame_b: np.ndarray, alpha: float, max_blur: int = 51) -> np.ndarray:
        blur_intensity = int(max_blur * (1.0 - abs(2.0 * alpha - 1.0)))
        if blur_intensity % 2 == 0:
            blur_intensity = max(1, blur_intensity - 1)

        if blur_intensity > 1:
            frame_a = cv2.GaussianBlur(frame_a, (blur_intensity, blur_intensity), 0)
            frame_b = cv2.GaussianBlur(frame_b, (blur_intensity, blur_intensity), 0)

        blended_frame = cv2.addWeighted(frame_a, 1.0 - alpha, frame_b, alpha, 0)
        return blended_frame
