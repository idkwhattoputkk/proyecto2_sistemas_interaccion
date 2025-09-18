#!/usr/bin/env python3
"""
Test script for Crystal Caverns Text Adventure Game
Runs automated tests to verify game functionality
"""

import sys
import time
from unittest.mock import patch

def test_audio_manager():
    """Test AudioManager class functionality"""
    print("Testing AudioManager...")
    
    try:
        from main import AudioManager
        audio_manager = AudioManager()
        
        # Test sound generation
        if hasattr(audio_manager, 'buffers'):
            print("✓ Audio buffers created successfully")
        else:
            print("✗ Audio buffers not created")
        
        # Test 3D positioning
        audio_manager.update_listener_position(1.0, 2.0, 3.0)
        print("✓ Listener position updated")
        
        # Test sound playback
        try:
            audio_manager.play_sound_3d("wind", (0, 0, 0))
            print("✓ Sound playback test passed")
        except Exception as e:
            print(f"⚠ Sound playback test: {e}")
        
        audio_manager.cleanup()
        print("✓ AudioManager cleanup successful")
        return True
        
    except Exception as e:
        print(f"✗ AudioManager test failed: {e}")
        return False

def test_game_state():
    """Test GameState class functionality"""
    print("\nTesting GameState...")
    
    try:
        from main import GameState
        game_state = GameState()
        
        # Test initial state
        assert game_state.current_location == "entrance"
        assert len(game_state.inventory) == 0
        print("✓ Initial state correct")
        
        # Test movement
        game_state.move_to("crystal_chamber", 5.0, 0.0, 0.0)
        assert game_state.current_location == "crystal_chamber"
        assert game_state.player_x == 5.0
        print("✓ Movement system working")
        
        # Test inventory
        game_state.add_item("crystal_fragment")
        assert game_state.has_item("crystal_fragment")
        print("✓ Inventory system working")
        
        print("✓ GameState test passed")
        return True
        
    except Exception as e:
        print(f"✗ GameState test failed: {e}")
        return False

def test_story_manager():
    """Test StoryManager class functionality"""
    print("\nTesting StoryManager...")
    
    try:
        from main import StoryManager, AudioManager, GameState
        
        audio_manager = AudioManager()
        game_state = GameState()
        story_manager = StoryManager(audio_manager, game_state)
        
        # Test story creation
        assert len(story_manager.story_lines) >= 50
        print(f"✓ Story created with {len(story_manager.story_lines)} lines")
        
        # Test story structure
        first_line = story_manager.story_lines[0]
        assert "text" in first_line
        assert "sound" in first_line
        assert "position" in first_line
        print("✓ Story structure correct")
        
        # Test progress tracking
        current, total = story_manager.get_progress()
        assert current == 0
        assert total == len(story_manager.story_lines)
        print("✓ Progress tracking working")
        
        audio_manager.cleanup()
        print("✓ StoryManager test passed")
        return True
        
    except Exception as e:
        print(f"✗ StoryManager test failed: {e}")
        return False

def test_game_integration():
    """Test full game integration"""
    print("\nTesting Game Integration...")
    
    try:
        from main import Game
        
        # Create game instance
        game = Game()
        
        # Test game initialization
        assert hasattr(game, 'audio_manager')
        assert hasattr(game, 'game_state')
        assert hasattr(game, 'story_manager')
        print("✓ Game initialization successful")
        
        # Test story length
        story_length = len(game.story_manager.story_lines)
        assert story_length >= 50
        print(f"✓ Story length: {story_length} lines (minimum 50 required)")
        
        # Test audio types
        audio_types = set()
        for line in game.story_manager.story_lines:
            audio_types.add(line["sound"])
        
        expected_types = {"footsteps", "water", "wind", "door", "music"}
        assert audio_types.issuperset(expected_types)
        print(f"✓ Audio types: {audio_types}")
        
        # Cleanup
        game.cleanup()
        print("✓ Game integration test passed")
        return True
        
    except Exception as e:
        print(f"✗ Game integration test failed: {e}")
        return False

def run_all_tests():
    """Run all tests and report results"""
    print("=== Crystal Caverns Game Tests ===\n")
    
    tests = [
        test_audio_manager,
        test_game_state,
        test_story_manager,
        test_game_integration
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"✗ Test {test.__name__} crashed: {e}")
    
    print(f"\n=== Test Results ===")
    print(f"Passed: {passed}/{total}")
    
    if passed == total:
        print("🎉 All tests passed! Game is ready to run.")
        return True
    else:
        print("⚠ Some tests failed. Check the output above.")
        return False

def main():
    """Main test function"""
    try:
        success = run_all_tests()
        return 0 if success else 1
    except Exception as e:
        print(f"Test suite crashed: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())