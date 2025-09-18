#!/usr/bin/env python3
"""
Installation script for Crystal Caverns Text Adventure Game
Automatically installs required dependencies
"""

import subprocess
import sys
import os

def install_package(package):
    """Install a Python package using pip"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"✓ Successfully installed {package}")
        return True
    except subprocess.CalledProcessError:
        print(f"✗ Failed to install {package}")
        return False

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 7):
        print("✗ Python 3.7 or higher is required")
        return False
    print(f"✓ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    return True

def install_dependencies():
    """Install all required dependencies"""
    print("Installing dependencies for Crystal Caverns...")
    
    # Core dependencies
    core_packages = [
        "numpy",
        "pyopenal"
    ]
    
    # Alternative audio packages (if OpenAL fails)
    fallback_packages = [
        "pygame",
        "sounddevice"
    ]
    
    print("\nInstalling core dependencies...")
    for package in core_packages:
        install_package(package)
    
    print("\nInstalling fallback audio packages...")
    for package in fallback_packages:
        install_package(package)
    
    print("\nDependency installation complete!")

def main():
    """Main installation function"""
    print("=== Crystal Caverns Installation ===")
    
    if not check_python_version():
        sys.exit(1)
    
    install_dependencies()
    
    print("\nInstallation complete! You can now run the game with:")
    print("python main.py")
    
    # Test if the game can run
    try:
        print("\nTesting game installation...")
        import main
        print("✓ Game installation test successful!")
    except Exception as e:
        print(f"✗ Game installation test failed: {e}")
        print("Please check the error messages above and try installing dependencies manually.")

if __name__ == "__main__":
    main()