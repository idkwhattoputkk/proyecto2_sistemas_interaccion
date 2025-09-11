#!/usr/bin/env python3
"""
Text Adventure Game with Spatial Audio
A Zork-style game using OpenAL for 3D sound positioning
"""

import time
import sys
import os
from typing import Dict, List, Optional, Tuple
import numpy as np

try:
    import PyOpenAL as al
except ImportError:
    print("Error: pyopenal not found. Please install it with: pip install pyopenal")
    sys.exit(1)

class AudioManager:
    """Manages 3D spatial audio using OpenAL"""
    
    def __init__(self):
        self.device = None
        self.context = None
        self.sources = {}
        self.buffers = {}
        self.listener_pos = [0.0, 0.0, 0.0]
        self.listener_orientation = [0.0, 0.0, -1.0, 0.0, 1.0, 0.0]
        
        try:
            self._initialize_audio()
        except Exception as e:
            print(f"Warning: Audio initialization failed: {e}")
            print("Game will run without audio")
    
    def _initialize_audio(self):
        """Initialize OpenAL device and context"""
        self.device = al.open_device()
        self.context = al.create_context(self.device)
        al.make_context_current(self.context)
        
        # Set listener properties
        al.listener_3f(al.POSITION, *self.listener_pos)
        al.listener_3f(al.ORIENTATION, *self.listener_orientation)
        
        # Create audio buffers for different sound types
        self._create_sound_buffers()
    
    def _create_sound_buffers(self):
        """Create audio buffers with generated sounds"""
        # Generate simple sine wave sounds for different effects
        sample_rate = 44100
        duration = 0.5
        
        # Footsteps sound
        footsteps_freq = 200
        t = np.linspace(0, duration, int(sample_rate * duration))
        footsteps_data = np.sin(2 * np.pi * footsteps_freq * t) * 0.3
        footsteps_data = (footsteps_data * 32767).astype(np.int16)
        
        # Water/river sound
        water_freq = 150
        water_data = np.sin(2 * np.pi * water_freq * t) * 0.4
        water_data = (water_data * 32767).astype(np.int16)
        
        # Wind sound
        wind_freq = 100
        wind_data = np.sin(2 * np.pi * wind_freq * t) * 0.2
        wind_data = (wind_data * 32767).astype(np.int16)
        
        # Door sound
        door_freq = 300
        door_data = np.sin(2 * np.pi * door_freq * t) * 0.5
        door_data = (door_data * 32767).astype(np.int16)
        
        # Ambient music (chord progression)
        music_duration = 2.0
        t_music = np.linspace(0, music_duration, int(sample_rate * music_duration))
        music_data = (np.sin(2 * np.pi * 440 * t_music) + 
                     np.sin(2 * np.pi * 554 * t_music) + 
                     np.sin(2 * np.pi * 659 * t_music)) * 0.2
        music_data = (music_data * 32767).astype(np.int16)
        
        # Store buffers
        self.buffers = {
            'footsteps': footsteps_data,
            'water': water_data,
            'wind': wind_data,
            'door': door_data,
            'music': music_data
        }
    
    def play_sound_3d(self, sound_type: str, position: Tuple[float, float, float], 
                      volume: float = 1.0, loop: bool = False):
        """Play a 3D positioned sound"""
        if not self.device or sound_type not in self.buffers:
            return
        
        try:
            # Create source
            source = al.gen_source()
            
            # Set source properties
            al.source_3f(source, al.POSITION, *position)
            al.source_f(source, al.GAIN, volume)
            al.source_i(source, al.LOOPING, 1 if loop else 0)
            
            # Create buffer and attach to source
            buffer = al.gen_buffer()
            al.buffer_data(buffer, al.FORMAT_MONO16, self.buffers[sound_type], 
                          len(self.buffers[sound_type]) * 2, 44100)
            al.source_i(source, al.BUFFER, buffer)
            
            # Play sound
            al.source_play(source)
            
            # Store source for cleanup
            self.sources[sound_type] = source
            
        except Exception as e:
            print(f"Audio error: {e}")
    
    def update_listener_position(self, x: float, y: float, z: float):
        """Update listener position for 3D audio"""
        if self.device:
            self.listener_pos = [x, y, z]
            al.listener_3f(al.POSITION, *self.listener_pos)
    
    def cleanup(self):
        """Clean up audio resources"""
        if self.device:
            for source in self.sources.values():
                al.delete_source(source)
            al.delete_context(self.context)
            al.close_device(self.device)

class GameState:
    """Manages the current state of the game"""
    
    def __init__(self):
        self.current_location = "entrance"
        self.inventory = []
        self.visited_locations = set()
        self.game_time = 0
        self.player_x, self.player_y, self.player_z = 0.0, 0.0, 0.0
        
    def move_to(self, location: str, x: float, y: float, z: float):
        """Move player to a new location"""
        self.current_location = location
        self.player_x, self.player_y, self.player_z = x, y, z
        self.visited_locations.add(location)
        self.game_time += 1
    
    def add_item(self, item: str):
        """Add item to inventory"""
        if item not in self.inventory:
            self.inventory.append(item)
    
    def has_item(self, item: str) -> bool:
        """Check if player has an item"""
        return item in self.inventory

class StoryManager:
    """Manages the story progression and text display"""
    
    def __init__(self, audio_manager: AudioManager, game_state: GameState):
        self.audio_manager = audio_manager
        self.game_state = game_state
        self.story_lines = self._create_story()
        self.current_line = 0
        
    def _create_story(self) -> List[Dict]:
        """Create the complete story with 50+ lines"""
        return [
            # Introduction (Lines 1-10)
            {
                "text": "You stand at the entrance of the ancient Crystal Caverns, a mysterious underground realm that has claimed many adventurers.",
                "sound": "wind",
                "position": (0, 0, -5),
                "delay": 0.5
            },
            {
                "text": "The wind howls through the cave entrance, carrying whispers of forgotten secrets.",
                "sound": "wind",
                "position": (0, 0, -3),
                "delay": 0.3
            },
            {
                "text": "Your torch flickers, casting dancing shadows on the rough stone walls.",
                "sound": "wind",
                "position": (0, 0, -1),
                "delay": 0.4
            },
            {
                "text": "A narrow path leads downward into darkness, the air growing colder with each step.",
                "sound": "footsteps",
                "position": (0, 0, 0),
                "delay": 0.6
            },
            {
                "text": "You hear the distant sound of water echoing through the caverns.",
                "sound": "water",
                "position": (5, 0, 0),
                "delay": 0.5
            },
            {
                "text": "The path splits into three directions: left, right, and straight ahead.",
                "sound": "footsteps",
                "position": (0, 0, 0),
                "delay": 0.4
            },
            {
                "text": "Ancient runes are carved into the walls, glowing with a faint blue light.",
                "sound": "wind",
                "position": (0, 0, 0),
                "delay": 0.5
            },
            {
                "text": "You choose the left path, drawn by the sound of flowing water.",
                "sound": "footsteps",
                "position": (-2, 0, 0),
                "delay": 0.6
            },
            {
                "text": "The tunnel narrows, forcing you to crouch as you proceed.",
                "sound": "footsteps",
                "position": (-3, 0, 0),
                "delay": 0.4
            },
            {
                "text": "Suddenly, you emerge into a vast chamber filled with crystal formations.",
                "sound": "music",
                "position": (0, 0, 0),
                "delay": 0.8
            },
            
            # Development (Lines 11-25)
            {
                "text": "The crystals hum with an otherworldly energy, creating a mesmerizing melody.",
                "sound": "music",
                "position": (0, 0, 0),
                "delay": 0.6
            },
            {
                "text": "In the center of the chamber, a crystal pedestal holds an ancient tome.",
                "sound": "wind",
                "position": (0, 0, 0),
                "delay": 0.5
            },
            {
                "text": "As you approach, the crystals begin to pulse with increasing intensity.",
                "sound": "music",
                "position": (0, 0, 0),
                "delay": 0.7
            },
            {
                "text": "The tome levitates from the pedestal, pages turning by invisible hands.",
                "sound": "wind",
                "position": (0, 0, 0),
                "delay": 0.6
            },
            {
                "text": "Ancient words appear in the air, glowing with magical energy.",
                "sound": "music",
                "position": (0, 0, 0),
                "delay": 0.5
            },
            {
                "text": "The words speak of a great evil that slumbers deep within the caverns.",
                "sound": "wind",
                "position": (0, 0, 0),
                "delay": 0.7
            },
            {
                "text": "Only the Crystal Key can seal the ancient threat forever.",
                "sound": "music",
                "position": (0, 0, 0),
                "delay": 0.6
            },
            {
                "text": "But the key has been split into three fragments scattered throughout the caverns.",
                "sound": "wind",
                "position": (0, 0, 0),
                "delay": 0.8
            },
            {
                "text": "You must find all three fragments before the evil awakens.",
                "sound": "music",
                "position": (0, 0, 0),
                "delay": 0.6
            },
            {
                "text": "The tome falls to the ground, and the crystals return to their normal state.",
                "sound": "wind",
                "position": (0, 0, 0),
                "delay": 0.5
            },
            {
                "text": "You pick up the tome and place it in your bag - it may contain more secrets.",
                "sound": "footsteps",
                "position": (0, 0, 0),
                "delay": 0.6
            },
            {
                "text": "Returning to the main path, you choose the right tunnel this time.",
                "sound": "footsteps",
                "position": (2, 0, 0),
                "delay": 0.5
            },
            {
                "text": "This passage leads upward, the air becoming warmer and drier.",
                "sound": "footsteps",
                "position": (3, 0, 0),
                "delay": 0.4
            },
            {
                "text": "You hear the sound of wind rushing through narrow crevices above.",
                "sound": "wind",
                "position": (0, 5, 0),
                "delay": 0.5
            },
            {
                "text": "The tunnel opens into a chamber filled with ancient machinery.",
                "sound": "wind",
                "position": (0, 0, 0),
                "delay": 0.6
            },
            
            # Climax (Lines 26-40)
            {
                "text": "Gears and pulleys line the walls, covered in centuries of dust.",
                "sound": "wind",
                "position": (0, 0, 0),
                "delay": 0.5
            },
            {
                "text": "In the center, a massive crystal mechanism pulses with energy.",
                "sound": "music",
                "position": (0, 0, 0),
                "delay": 0.7
            },
            {
                "text": "One of the crystal fragments floats within the mechanism's core.",
                "sound": "music",
                "position": (0, 0, 0),
                "delay": 0.6
            },
            {
                "text": "But the mechanism is protected by a complex puzzle of moving parts.",
                "sound": "wind",
                "position": (0, 0, 0),
                "delay": 0.5
            },
            {
                "text": "You study the ancient tome, finding clues about the mechanism's operation.",
                "sound": "wind",
                "position": (0, 0, 0),
                "delay": 0.7
            },
            {
                "text": "After hours of careful manipulation, the mechanism finally opens.",
                "sound": "door",
                "position": (0, 0, 0),
                "delay": 0.8
            },
            {
                "text": "The first crystal fragment floats into your hand, glowing with power.",
                "sound": "music",
                "position": (0, 0, 0),
                "delay": 0.6
            },
            {
                "text": "Suddenly, the caverns begin to shake violently.",
                "sound": "wind",
                "position": (0, 0, 0),
                "delay": 0.5
            },
            {
                "text": "The ancient evil is awakening - you must hurry to find the other fragments.",
                "sound": "music",
                "position": (0, 0, 0),
                "delay": 0.8
            },
            {
                "text": "You rush back to the main path and take the center tunnel.",
                "sound": "footsteps",
                "position": (0, 0, 2),
                "delay": 0.6
            },
            {
                "text": "This passage leads deep into the heart of the mountain.",
                "sound": "footsteps",
                "position": (0, 0, 4),
                "delay": 0.5
            },
            {
                "text": "The air becomes thick with ancient magic and foreboding.",
                "sound": "wind",
                "position": (0, 0, 0),
                "delay": 0.6
            },
            {
                "text": "You emerge into a vast underground lake, its waters black as night.",
                "sound": "water",
                "position": (0, 0, 0),
                "delay": 0.7
            },
            {
                "text": "In the center of the lake, an island holds the second crystal fragment.",
                "sound": "water",
                "position": (0, 0, 0),
                "delay": 0.6
            },
            {
                "text": "But the waters are home to ancient guardians, awakened by your presence.",
                "sound": "water",
                "position": (0, 0, 0),
                "delay": 0.7
            },
            {
                "text": "You must find a way to cross without alerting the creatures below.",
                "sound": "wind",
                "position": (0, 0, 0),
                "delay": 0.5
            },
            
            # Resolution (Lines 41-55)
            {
                "text": "Using the tome's knowledge, you create a bridge of light across the water.",
                "sound": "music",
                "position": (0, 0, 0),
                "delay": 0.8
            },
            {
                "text": "The guardians remain undisturbed as you cross to the island.",
                "sound": "footsteps",
                "position": (0, 0, 0),
                "delay": 0.6
            },
            {
                "text": "The second fragment joins the first, their combined power growing stronger.",
                "sound": "music",
                "position": (0, 0, 0),
                "delay": 0.7
            },
            {
                "text": "But the caverns shake again, more violently than before.",
                "sound": "wind",
                "position": (0, 0, 0),
                "delay": 0.5
            },
            {
                "text": "You must find the final fragment before it's too late.",
                "sound": "music",
                "position": (0, 0, 0),
                "delay": 0.6
            },
            {
                "text": "Following the fragments' guidance, you discover a hidden passage.",
                "sound": "footsteps",
                "position": (0, 0, 0),
                "delay": 0.5
            },
            {
                "text": "It leads to the deepest chamber, where the ancient evil slumbers.",
                "sound": "wind",
                "position": (0, 0, 0),
                "delay": 0.7
            },
            {
                "text": "The final fragment floats above a massive crystal coffin.",
                "sound": "music",
                "position": (0, 0, 0),
                "delay": 0.6
            },
            {
                "text": "As you reach for it, the coffin begins to crack and glow.",
                "sound": "wind",
                "position": (0, 0, 0),
                "delay": 0.5
            },
            {
                "text": "The ancient evil is breaking free - you have only moments to act.",
                "sound": "music",
                "position": (0, 0, 0),
                "delay": 0.7
            },
            {
                "text": "With all three fragments in hand, you begin the ancient sealing ritual.",
                "sound": "music",
                "position": (0, 0, 0),
                "delay": 0.8
            },
            {
                "text": "The fragments merge into the Crystal Key, glowing with pure light.",
                "sound": "music",
                "position": (0, 0, 0),
                "delay": 0.7
            },
            {
                "text": "You thrust the key into the coffin, sealing the evil once more.",
                "sound": "music",
                "position": (0, 0, 0),
                "delay": 0.8
            },
            {
                "text": "The caverns fall silent, the threat contained for another age.",
                "sound": "wind",
                "position": (0, 0, 0),
                "delay": 0.6
            },
            {
                "text": "You emerge from the caverns as the sun rises over the mountains.",
                "sound": "wind",
                "position": (0, 0, 0),
                "delay": 0.7
            },
            {
                "text": "The Crystal Key rests safely in your possession, a testament to your courage.",
                "sound": "music",
                "position": (0, 0, 0),
                "delay": 0.8
            },
            {
                "text": "Your adventure is complete, but the caverns will always call to those brave enough to enter.",
                "sound": "wind",
                "position": (0, 0, 0),
                "delay": 0.9
            },
            {
                "text": "The End.",
                "sound": "music",
                "position": (0, 0, 0),
                "delay": 1.0
            }
        ]
    
    def display_next_line(self) -> bool:
        """Display the next line of the story with audio"""
        if self.current_line >= len(self.story_lines):
            return False
        
        line_data = self.story_lines[self.current_line]
        
        # Update listener position for 3D audio
        self.audio_manager.update_listener_position(
            self.game_state.player_x,
            self.game_state.player_y,
            self.game_state.player_z
        )
        
        # Play the associated sound
        self.audio_manager.play_sound_3d(
            line_data["sound"],
            line_data["position"]
        )
        
        # Display the text
        print(f"\n{line_data['text']}")
        
        # Wait for the specified delay
        time.sleep(line_data["delay"])
        
        self.current_line += 1
        return True
    
    def get_progress(self) -> Tuple[int, int]:
        """Get current progress in the story"""
        return self.current_line, len(self.story_lines)

class Game:
    """Main game class that orchestrates everything"""
    
    def __init__(self):
        self.audio_manager = AudioManager()
        self.game_state = GameState()
        self.story_manager = StoryManager(self.audio_manager, self.game_state)
        self.running = True
    
    def run(self):
        """Main game loop"""
        print("=== CRYSTAL CAVERNS: A TEXT ADVENTURE ===")
        print("A Zork-style adventure with 3D spatial audio")
        print("Press Enter to advance through the story...")
        print("Type 'quit' to exit the game")
        print("=" * 50)
        
        while self.running and self.story_manager.current_line < len(self.story_manager.story_lines):
            user_input = input("\nPress Enter to continue... ").strip().lower()
            
            if user_input == 'quit':
                self.running = False
                break
            
            # Display progress
            current, total = self.story_manager.get_progress()
            print(f"\nProgress: {current}/{total} lines")
            
            # Display next story line
            if not self.story_manager.display_next_line():
                break
        
        if self.story_manager.current_line >= len(self.story_manager.story_lines):
            print("\n🎉 Congratulations! You've completed the adventure!")
            print(f"Total game time: {self.game_state.game_time} minutes")
        
        self.cleanup()
    
    def cleanup(self):
        """Clean up game resources"""
        self.audio_manager.cleanup()
        print("\nThanks for playing Crystal Caverns!")

def main():
    """Main entry point"""
    try:
        game = Game()
        game.run()
    except KeyboardInterrupt:
        print("\n\nGame interrupted by user.")
    except Exception as e:
        print(f"\nAn error occurred: {e}")
        print("Please check your audio drivers and try again.")

if __name__ == "__main__":
    main()