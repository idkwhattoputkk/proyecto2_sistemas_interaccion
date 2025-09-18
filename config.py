#!/usr/bin/env python3
"""
Configuration file for Crystal Caverns Text Adventure Game
Contains game settings and audio parameters
"""

# Game Configuration
GAME_TITLE = "Crystal Caverns: A Text Adventure"
GAME_VERSION = "1.0.0"
GAME_AUTHOR = "University Project - Interactive Systems"

# Audio Configuration
AUDIO_SAMPLE_RATE = 44100
AUDIO_CHANNELS = 1
AUDIO_BIT_DEPTH = 16

# Sound Types and Parameters
SOUND_CONFIG = {
    "footsteps": {
        "frequency": 200,
        "duration": 0.5,
        "volume": 0.3
    },
    "water": {
        "frequency": 150,
        "duration": 0.5,
        "volume": 0.4
    },
    "wind": {
        "frequency": 100,
        "duration": 0.5,
        "volume": 0.2
    },
    "door": {
        "frequency": 300,
        "duration": 0.5,
        "volume": 0.5
    },
    "music": {
        "frequencies": [440, 554, 659],  # A major chord
        "duration": 2.0,
        "volume": 0.2
    }
}

# 3D Audio Settings
AUDIO_3D_CONFIG = {
    "max_distance": 10.0,
    "rolloff_factor": 1.0,
    "reference_distance": 1.0
}

# Story Display Settings
STORY_CONFIG = {
    "auto_advance": False,
    "default_delay": 0.5,
    "max_line_length": 80
}

# Game Difficulty Settings
DIFFICULTY_CONFIG = {
    "easy": {
        "audio_cues": True,
        "text_delays": True,
        "progress_indicators": True
    },
    "normal": {
        "audio_cues": True,
        "text_delays": True,
        "progress_indicators": False
    },
    "hard": {
        "audio_cues": False,
        "text_delays": False,
        "progress_indicators": False
    }
}