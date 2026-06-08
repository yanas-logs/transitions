import os
from core.processor import Processor

def main():
    video_a = "testing/input/video1.mp4"
    video_b = "testing/input/video2.mp4"
    output_video = "testing/output/result.mp4"
    transition_duration = 1.5 

    os.makedirs("testing/output", exist_ok=True)

    processor = Processor(video_a, video_b, output_video)
    print("Transition on process... Please wait.")
    processor.apply_transition(transition_duration)
    print(f"Successfully: {output_video}")

if __name__ == "__main__":
    main()
