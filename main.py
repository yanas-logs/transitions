import os
from core.processor import Processor

def main():
    source_a = "testing/input/video-black.mp4"
    source_b = "testing/input/video-white.mp4"
    output_video = "testing/output/result.mp4"
    transition_duration = 1.5

    os.makedirs("testing/output", exist_ok=True)

    processor = Processor(source_a, source_b, output_video)
    print("Processing transition... Please wait.")
    processor.apply_transition(transition_duration)
    print(f"Successfully generated: {output_video}")

if __name__ == "__main__":
    main()