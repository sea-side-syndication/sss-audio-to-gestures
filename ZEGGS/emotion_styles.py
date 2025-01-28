from enum import Enum
import random
from pathlib import Path
from typing import List, Tuple

class Emotion(Enum):
    NEUTRAL = "neutral"
    SAD = "sad"
    HAPPY = "happy"
    RELAXED = "relaxed"
    OLD = "old"
    ANGRY = "angry"
    AGREEMENT = "agreement"
    DISAGREEMENT = "disagreement"
    FLIRTY = "flirty"
    PENSIVE = "pensive"
    SCARED = "scared"
    DISTRACTED = "distracted"
    SARCASTIC = "sarcastic"
    THREATENING = "threatening"
    STILL = "still"
    LAUGHING = "laughing"
    SNEAKY = "sneaky"
    TIRED = "tired"
    SPEECH = "speech"


# Emotion to style mapping with tuples of (regular, mirrored) file pairs
EMOTION_STYLES = {
    Emotion.NEUTRAL: [
        ("001_Neutral_0_x_1_0.bvh", "001_Neutral_0_mirror_x_1_0.bvh"),
        ("002_Neutral_1_x_1_0.bvh", "002_Neutral_1_mirror_x_1_0.bvh"),
        ("003_Neutral_2_x_1_0.bvh", "003_Neutral_2_mirror_x_1_0.bvh"),
        ("004_Neutral_3_x_1_0.bvh", "004_Neutral_3_mirror_x_1_0.bvh"),
        ("005_Neutral_4_x_1_0.bvh", "005_Neutral_4_mirror_x_1_0.bvh")
    ],
    Emotion.SAD: [
        ("006_Sad_0_x_1_0.bvh", "006_Sad_0_mirror_x_1_0.bvh"),
        ("007_Sad_1_x_1_0.bvh", "007_Sad_1_mirror_x_1_0.bvh"),
        ("008_Sad_2_x_1_0.bvh", "008_Sad_2_mirror_x_1_0.bvh"),
        ("009_Sad_3_x_1_0.bvh", "009_Sad_3_mirror_x_1_0.bvh"),
        ("010_Sad_4_x_1_0.bvh", "010_Sad_4_mirror_x_1_0.bvh")
    ],
    Emotion.HAPPY: [
        ("011_Happy_0_x_1_0.bvh", "011_Happy_0_mirror_x_1_0.bvh"),
        ("012_Happy_1_x_1_0.bvh", "012_Happy_1_mirror_x_1_0.bvh"),
        ("013_Happy_2_x_1_0.bvh", "013_Happy_2_mirror_x_1_0.bvh"),
        ("014_Happy_3_x_1_0.bvh", "014_Happy_3_mirror_x_1_0.bvh"),
        ("015_Happy_4_x_1_0.bvh", "015_Happy_4_mirror_x_1_0.bvh")
    ],
    Emotion.RELAXED: [
        ("016_Relaxed_0_x_1_0.bvh", "016_Relaxed_0_mirror_x_1_0.bvh"),
        ("017_Relaxed_1_x_1_0.bvh", "017_Relaxed_1_mirror_x_1_0.bvh"),
        ("018_Relaxed_2_x_1_0.bvh", "018_Relaxed_2_mirror_x_1_0.bvh"),
        ("019_Relaxed_3_x_1_0.bvh", "019_Relaxed_3_mirror_x_1_0.bvh"),
        ("020_Relaxed_4_x_1_0.bvh", "020_Relaxed_4_mirror_x_1_0.bvh")
    ],
    Emotion.OLD: [
        ("021_Old_0_x_1_0.bvh", "021_Old_0_mirror_x_1_0.bvh"),
        ("022_Old_1_x_1_0.bvh", "022_Old_1_mirror_x_1_0.bvh"),
        ("023_Old_2_x_1_0.bvh", "023_Old_2_mirror_x_1_0.bvh"),
        ("024_Old_3_x_1_0.bvh", "024_Old_3_mirror_x_1_0.bvh"),
        ("025_Old_4_x_1_0.bvh", "025_Old_4_mirror_x_1_0.bvh")
    ],
    Emotion.ANGRY: [
        ("026_Angry_0_x_1_0.bvh", "026_Angry_0_mirror_x_1_0.bvh"),
        ("027_Angry_1_x_1_0.bvh", "027_Angry_1_mirror_x_1_0.bvh"),
        ("028_Angry_2_x_1_0.bvh", "028_Angry_2_mirror_x_1_0.bvh"),
        ("029_Angry_3_x_1_0.bvh", "029_Angry_3_mirror_x_1_0.bvh")
    ],
    Emotion.AGREEMENT: [
        ("030_Agreement_0_x_1_0.bvh", "030_Agreement_0_mirror_x_1_0.bvh"),
        ("032_Agreement_1_x_1_0.bvh", "032_Agreement_1_mirror_x_1_0.bvh"),
        ("033_Agreement_2_x_1_0.bvh", "033_Agreement_2_mirror_x_1_0.bvh")
    ],
    Emotion.DISAGREEMENT: [
        ("031_Disagreement_0_x_1_0.bvh", "031_Disagreement_0_mirror_x_1_0.bvh"),
        ("034_Disagreement_1_x_1_0.bvh", "034_Disagreement_1_mirror_x_1_0.bvh"),
        ("035_Disagreement_2_x_1_0.bvh", "035_Disagreement_2_mirror_x_1_0.bvh")
    ],
    Emotion.FLIRTY: [
        ("036_Flirty_0_x_1_0.bvh", "036_Flirty_0_mirror_x_1_0.bvh"),
        ("037_Flirty_1_x_1_0.bvh", "037_Flirty_1_mirror_x_1_0.bvh"),
        ("038_Flirty_2_x_1_0.bvh", "038_Flirty_2_mirror_x_1_0.bvh")
    ],
    Emotion.PENSIVE: [
        ("039_Pensive_0_x_1_0.bvh", "039_Pensive_0_mirror_x_1_0.bvh"),
        ("040_Pensive_1_x_1_0.bvh", "040_Pensive_1_mirror_x_1_0.bvh"),
        ("041_Pensive_2_x_1_0.bvh", "041_Pensive_2_mirror_x_1_0.bvh")
    ],
    Emotion.SCARED: [
        ("042_Scared_0_x_1_0.bvh", "042_Scared_0_mirror_x_1_0.bvh"),
        ("043_Scared_1_x_1_0.bvh", "043_Scared_1_mirror_x_1_0.bvh"),
        ("044_Scared_2_x_1_0.bvh", "044_Scared_2_mirror_x_1_0.bvh")
    ],
    Emotion.DISTRACTED: [
        ("045_Distracted_0_x_1_0.bvh", "045_Distracted_0_mirror_x_1_0.bvh"),
        ("046_Distracted_1_x_1_0.bvh", "046_Distracted_1_mirror_x_1_0.bvh"),
        ("047_Distracted_2_x_1_0.bvh", "047_Distracted_2_mirror_x_1_0.bvh")
    ],
    Emotion.SARCASTIC: [
        ("048_Sarcastic_0_x_1_0.bvh", "048_Sarcastic_0_mirror_x_1_0.bvh"),
        ("049_Sarcastic_1_x_1_0.bvh", "049_Sarcastic_1_mirror_x_1_0.bvh"),
        ("050_Sarcastic_2_x_1_0.bvh", "050_Sarcastic_2_mirror_x_1_0.bvh")
    ],
    Emotion.THREATENING: [
        ("051_Threatening_0_x_1_0.bvh", "051_Threatening_0_mirror_x_1_0.bvh"),
        ("052_Threatening_1_x_1_0.bvh", "052_Threatening_1_mirror_x_1_0.bvh"),
        ("053_Threatening_2_x_1_0.bvh", "053_Threatening_2_mirror_x_1_0.bvh")
    ],
    Emotion.STILL: [
        ("054_Still_0_x_1_0.bvh", "054_Still_0_mirror_x_1_0.bvh"),
        ("055_Still_1_x_1_0.bvh", "055_Still_1_mirror_x_1_0.bvh"),
        ("056_Still_2_x_1_0.bvh", "056_Still_2_mirror_x_1_0.bvh")
    ],
    Emotion.LAUGHING: [
        ("057_Laughing_0_x_1_0.bvh", "057_Laughing_0_mirror_x_1_0.bvh"),
        ("058_Laughing_1_x_1_0.bvh", "058_Laughing_1_mirror_x_1_0.bvh")
    ],
    Emotion.SNEAKY: [
        ("059_Sneaky_0_x_1_0.bvh", "059_Sneaky_0_mirror_x_1_0.bvh"),
        ("060_Sneaky_1_x_1_0.bvh", "060_Sneaky_1_mirror_x_1_0.bvh"),
        ("061_Sneaky_2_x_1_0.bvh", "061_Sneaky_2_mirror_x_1_0.bvh")
    ],
    Emotion.TIRED: [
        ("062_Tired_0_x_1_0.bvh", "062_Tired_0_mirror_x_1_0.bvh"),
        ("063_Tired_1_x_1_0.bvh", "063_Tired_1_mirror_x_1_0.bvh"),
        ("064_Tired_2_x_1_0.bvh", "064_Tired_2_mirror_x_1_0.bvh")
    ],
    Emotion.SPEECH: [
        ("065_Speech_0_x_1_0.bvh", "065_Speech_0_mirror_x_1_0.bvh"),
        ("066_Speech_1_x_1_0.bvh", "066_Speech_1_mirror_x_1_0.bvh"),
        ("067_Speech_2_x_1_0.bvh", "067_Speech_2_mirror_x_1_0.bvh")
    ]
}


def get_random_style_for_emotion(emotion: Emotion = Emotion.NEUTRAL, mirrored: bool = False) -> Path:
    """
    Returns a random style file path for given emotion

    Args:
        emotion (Emotion): The emotion to get a style for
        styles_path (Path): Base path where the style files are located
        mirrored (bool): If True, returns the mirrored version of the animation

    Returns:
        Path: Path to the randomly selected style file

    If emotion is not found, returns a random neutral style
    """
    if emotion not in EMOTION_STYLES:
        emotion = Emotion.NEUTRAL

    style_pair = random.choice(EMOTION_STYLES[emotion])
    selected_file = style_pair[1] if mirrored else style_pair[0]
    return selected_file


def get_all_styles_for_emotion(emotion: Emotion, styles_path: Path) -> List[Tuple[Path, Path]]:
    """
    Returns all available style pairs (regular and mirrored) for given emotion

    Args:
        emotion (Emotion): The emotion to get styles for
        styles_path (Path): Base path where the style files are located

    Returns:
        List[Tuple[Path, Path]]: List of tuples containing (regular, mirrored) file path pairs
    """
    if emotion not in EMOTION_STYLES:
        emotion = Emotion.NEUTRAL

    return [(styles_path / reg, styles_path / mir) for reg, mir in EMOTION_STYLES[emotion]]

# Example usage:
# styles_path = Path("B:/Developer/Projects/PARSER/clean")
#
# # Get random regular animation
# style_path = get_random_style_for_emotion(Emotion.HAPPY, styles_path)
#
# # Get random mirrored animation
#mirrored_style_path = get_random_style_for_emotion(Emotion.HAPPY, mirrored=True)
#
# # Get all styles for an emotion
# all_style_pairs = get_all_styles_for_emotion(Emotion.HAPPY, styles_path)
#print(get_random_style_for_emotion())