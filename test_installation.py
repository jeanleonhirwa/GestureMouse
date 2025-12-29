"""
Test script to verify GestureMouse installation
"""

import sys

def test_imports():
    """Test if all required packages can be imported"""
    packages = {
        'cv2': 'OpenCV',
        'mediapipe': 'MediaPipe',
        'PyQt6': 'PyQt6',
        'pyautogui': 'PyAutoGUI',
        'numpy': 'NumPy',
        'PIL': 'Pillow'
    }
    
    print("=" * 60)
    print("GestureMouse Installation Test")
    print("=" * 60)
    print("\nTesting package imports...\n")
    
    all_ok = True
    failed_packages = []
    
    for package, name in packages.items():
        try:
            __import__(package)
            print(f"✓ {name:20s} - OK")
        except ImportError as e:
            print(f"✗ {name:20s} - FAILED")
            all_ok = False
            failed_packages.append(name)
    
    print("\n" + "=" * 60)
    
    if all_ok:
        print("✓ SUCCESS: All packages installed successfully!")
        print("\nYou can now run GestureMouse:")
        print("  python run.py")
    else:
        print("✗ FAILED: Some packages could not be imported.")
        print("\nMissing packages:", ", ".join(failed_packages))
        print("\nTo install missing packages, run:")
        print("  pip install -r requirements.txt")
    
    print("=" * 60)
    
    return all_ok

def test_camera():
    """Test if camera is accessible"""
    try:
        import cv2
        print("\nTesting camera access...")
        cap = cv2.VideoCapture(0)
        if cap.isOpened():
            ret, frame = cap.read()
            cap.release()
            if ret:
                print("✓ Camera test - OK")
                return True
            else:
                print("✗ Camera test - Could not read frame")
                return False
        else:
            print("✗ Camera test - Could not open camera")
            return False
    except Exception as e:
        print(f"✗ Camera test - Error: {e}")
        return False

if __name__ == "__main__":
    imports_ok = test_imports()
    
    if imports_ok:
        camera_ok = test_camera()
        sys.exit(0 if camera_ok else 1)
    else:
        sys.exit(1)
