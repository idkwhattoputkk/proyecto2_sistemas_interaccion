"""
Alternative audio setup for systems without OpenAL
Provides fallback audio using system audio libraries
"""

import sys
import time
import numpy as np

class FallbackAudioManager:
    """Fallback audio manager when OpenAL is not available"""
    
    def __init__(self):
        self.audio_available = False
        try:
            # Try to import alternative audio libraries
            import pygame
            pygame.mixer.init(frequency=44100, size=-16, channels=1)
            self.audio_available = True
            self.pygame = pygame
        except ImportError:
            try:
                import sounddevice as sd
                self.audio_available = True
                self.sounddevice = sd
            except ImportError:
                print("Warning: No audio libraries available. Game will run silently.")
    
    def play_sound_3d(self, sound_type: str, position: Tuple[float, float, float], 
                      volume: float = 1.0, loop: bool = False):
        """Play sound with basic 3D positioning simulation"""
        if not self.audio_available:
            return
        
        try:
            # Generate simple sound based on type
            sample_rate = 44100
            duration = 0.5
            
            if sound_type == "footsteps":
                freq = 200
            elif sound_type == "water":
                freq = 150
            elif sound_type == "wind":
                freq = 100
            elif sound_type == "door":
                freq = 300
            elif sound_type == "music":
                freq = 440
                duration = 1.0
            else:
                freq = 200
            
            # Generate tone
            t = np.linspace(0, duration, int(sample_rate * duration))
            audio_data = np.sin(2 * np.pi * freq * t) * volume * 0.3
            
            # Simulate 3D positioning by adjusting volume based on distance
            distance = np.sqrt(sum(x*x for x in position))
            if distance > 0:
                volume_adjusted = volume / (1 + distance * 0.5)
                audio_data *= volume_adjusted
            
            # Play audio
            if hasattr(self, 'pygame'):
                # Convert to pygame audio format
                audio_data = (audio_data * 32767).astype(np.int16)
                sound = self.pygame.sndarray.make_sound(audio_data)
                sound.play()
            elif hasattr(self, 'sounddevice'):
                # Play using sounddevice
                self.sounddevice.play(audio_data, sample_rate)
                
        except Exception as e:
            print(f"Audio playback error: {e}")
    
    def update_listener_position(self, x: float, y: float, z: float):
        """Update listener position (no-op for fallback)"""
        pass
    
    def cleanup(self):
        """Clean up audio resources"""
        if hasattr(self, 'pygame'):
            self.pygame.mixer.quit()

def create_audio_manager():
    """Create the best available audio manager"""
    try:
        import openal as al
        from main import AudioManager
        return AudioManager()
    except ImportError:
        print("OpenAL not available, using fallback audio")
        return FallbackAudioManager()
