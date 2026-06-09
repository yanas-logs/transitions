import os
from core.processor import Processor

def main():
    source_a = "testing/input/video-black.mp4"
    source_b = "testing/input/video-white.mp4"
    output_video = "testing/output/result.mp4"
    transition_duration = 1.5

    # Options for transition effects
    effects = {
        "1": "cross_dissolve_blur",
        "2": "fade_to_black",
        "3": "fade_to_white"
    }

    print("=== Video Transition Engine ===")
    print("Select the type of transition you want to apply:")
    for key, name in effects.items():
        print(f"[{key}] {name}")
    
    options = input("Enter the number of your choice (default 1): ").strip()
    
    # default to "cross_dissolve_blur" if input is invalid or empty
    selected_effect = effects.get(options, "cross_dissolve_blur")

    os.makedirs("testing/output", exist_ok=True)

    processor = Processor(source_a, source_b, output_video)
    print(f"\nProcessing transition using '{selected_effect}'... Please wait.")
    processor.apply_transition(transition_duration, effect_name=selected_effect)
    print(f"Successfully generated: {output_video}")

if __name__ == "__main__":
    main()