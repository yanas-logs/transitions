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

        return cv2.addWeighted(frame_a, 1.0 - alpha, frame_b, alpha, 0)

    @staticmethod
    def fade_to_black(frame_a: np.ndarray, frame_b: np.ndarray, alpha: float) -> np.ndarray:
        black_screen = np.zeros_like(frame_a)
        
        if alpha < 0.5:
            factor = alpha * 2.0
            return cv2.addWeighted(frame_a, 1.0 - factor, black_screen, factor, 0)
        else:
            factor = (alpha - 0.5) * 2.0
            return cv2.addWeighted(black_screen, 1.0 - factor, frame_b, factor, 0)

    @staticmethod
    def fade_to_white(frame_a: np.ndarray, frame_b: np.ndarray, alpha: float) -> np.ndarray:
        white_screen = np.full_like(frame_a, 255)
        
        if alpha < 0.5:
            factor = alpha * 2.0
            return cv2.addWeighted(frame_a, 1.0 - factor, white_screen, factor, 0)
        else:
            factor = (alpha - 0.5) * 2.0
            return cv2.addWeighted(white_screen, 1.0 - factor, frame_b, factor, 0)