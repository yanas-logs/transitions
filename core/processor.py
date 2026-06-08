import cv2
from core.transitions import Transitions

class Processor:
    def __init__(self, video_path_a: str, video_path_b: str, output_path: str):
        self.video_path_a = video_path_a
        self.video_path_b = video_path_b
        self.output_path = output_path

    def _get_video_properties(self, cap: cv2.VideoCapture) -> tuple:
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        return fps, width, height

    def apply_transition(self, duration_seconds: float):
        cap_a = cv2.VideoCapture(self.video_path_a)
        cap_b = cv2.VideoCapture(self.video_path_b)

        fps, width, height = self._get_video_properties(cap_a)
        total_frames_a = int(cap_a.get(cv2.CAP_PROP_FRAME_COUNT))
        transition_frames = int(fps * duration_seconds)
        main_frames_a = total_frames_a - transition_frames

        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(self.output_path, fourcc, fps, (width, height))

        for _ in range(main_frames_a):
            ret, frame = cap_a.read()
            if not ret:
                break
            out.write(frame)

        for i in range(transition_frames):
            ret_a, frame_a = cap_a.read()
            ret_b, frame_b = cap_b.read()

            if not ret_a or not ret_b:
                break

            alpha = i / (transition_frames - 1)
            transition_frame = VideoTransitions.cross_dissolve_blur(frame_a, frame_b, alpha)
            out.write(transition_frame)

            while True:
            ret, frame = cap_b.read()
            if not ret:
                break
            out.write(frame)

        cap_a.release()
        cap_b.release()
        out.release()
