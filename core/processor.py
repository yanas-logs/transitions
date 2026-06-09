import cv2
import numpy as np
from core.transitions import Transitions

class Processor:
    def __init__(self, path_a: str, path_b: str, output_path: str):
        self.path_a = path_a
        self.path_b = path_b
        self.output_path = output_path

    def _read_source(self, path: str, target_fps: int = 30, duration_sec: float = 3.0) -> tuple[list[np.ndarray], tuple[int, int, int]]:
        cap = cv2.VideoCapture(path)
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        if fps > 0 and width > 0 and height > 0:
            frames = []
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                frames.append(frame)
            cap.release()
            return frames, (fps, width, height)

        cap.release()
        img = cv2.imread(path)
        if img is None:
            raise FileNotFoundError(f"Failed to read file: {path}")

        height, width, _ = img.shape
        total_frames = int(target_fps * duration_sec)
        frames = [img.copy() for _ in range(total_frames)]
        return frames, (target_fps, width, height)

    def apply_transition(self, duration_seconds: float, effect_name: str = "cross_dissolve_blur"):
        frames_a, props_a = self._read_source(self.path_a)
        frames_b, props_b = self._read_source(self.path_b)

        fps, width, height = props_a
        transition_frames = int(fps * duration_seconds)

        for i, frame in enumerate(frames_b):
            if frame.shape[1] != width or frame.shape[0] != height:
                frames_b[i] = cv2.resize(frame, (width, height))

        main_frames_a = max(0, len(frames_a) - transition_frames)

        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(self.output_path, fourcc, fps, (width, height))

        for i in range(main_frames_a):
            out.write(frames_a[i])

        transition_func = getattr(Transitions, effect_name, Transitions.cross_dissolve_blur)

        for i in range(transition_frames):
            idx_a = main_frames_a + i
            idx_b = i

            if idx_a >= len(frames_a) or idx_b >= len(frames_b):
                break

            alpha = i / (transition_frames - 1) if transition_frames > 1 else 1.0
            transition_frame = transition_func(frames_a[idx_a], frames_b[idx_b], alpha)
            out.write(transition_frame)

        for i in range(transition_frames, len(frames_b)):
            out.write(frames_b[i])

        out.release()
        