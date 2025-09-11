#!/usr/bin/env python3
"""
Demo script for Crystal Caverns Text Adventure Game
Shows the first few lines with audio to demonstrate functionality
"""

import time
from main import Game

def run_demo():
    """Run a short demo of the game"""
    print("=== CRYSTAL CAVERNS DEMO ===")
    print("This demo shows the first 5 lines of the story with audio")
    print("=" * 50)
    
    # Create game instance
    game = Game()
    
    # Show first 5 lines
    for i in range(5):
        if game.story_manager.current_line < len(game.story_manager.story_lines):
            # Display progress
            current, total = game.story_manager.get_progress()
            print(f"\n--- Line {current + 1}/{total} ---")
            
            # Display the line with audio
            game.story_manager.display_next_line()
            
            # Small pause between lines
            time.sleep(0.5)
    
    print("\n" + "=" * 50)
    print("Demo completed! Run 'python main.py' for the full experience.")
    
    # Cleanup
    game.cleanup()

if __name__ == "__main__":
    run_demo()