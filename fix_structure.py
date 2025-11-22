import os
import shutil
import time

BASE_DIR = os.getcwd()
PACKAGE_DIR = os.path.join(BASE_DIR, 'decom')
TEMP_DIR = os.path.join(BASE_DIR, 'decom_pkg')

SOURCE_DIRS = ['cli', 'core', 'blockchain', 'database', 'monitoring', 'security', 'tests', 'config', 'scripts']
SOURCE_FILES = ['__init__.py']

def cleanup_and_restructure():
    print(f"Current directory: {BASE_DIR}")
    
    # Create package directory if it doesn't exist
    if not os.path.exists(PACKAGE_DIR):
        os.makedirs(PACKAGE_DIR)
        print(f"Created {PACKAGE_DIR}")

    # Handle the 'decom_pkg' from previous failed attempts
    if os.path.exists(TEMP_DIR):
        print(f"Found {TEMP_DIR}, moving contents to {PACKAGE_DIR}")
        for item in os.listdir(TEMP_DIR):
            s = os.path.join(TEMP_DIR, item)
            d = os.path.join(PACKAGE_DIR, item)
            if os.path.exists(d):
                if os.path.isdir(d):
                    shutil.rmtree(d)
                else:
                    os.remove(d)
            shutil.move(s, d)
        os.rmdir(TEMP_DIR)

    # Move source directories from root to package directory
    for item in SOURCE_DIRS + SOURCE_FILES:
        s = os.path.join(BASE_DIR, item)
        d = os.path.join(PACKAGE_DIR, item)
        
        if os.path.exists(s):
            print(f"Moving {item} to {PACKAGE_DIR}")
            if os.path.exists(d):
                if os.path.isdir(d):
                    shutil.rmtree(d)
                else:
                    os.remove(d)
            shutil.move(s, d)

    # Ensure __init__.py exists
    init_file = os.path.join(PACKAGE_DIR, '__init__.py')
    if not os.path.exists(init_file):
        with open(init_file, 'w') as f:
            pass
        print(f"Created {init_file}")

if __name__ == "__main__":
    try:
        cleanup_and_restructure()
        print("Restructuring complete.")
    except Exception as e:
        print(f"Error: {e}")
