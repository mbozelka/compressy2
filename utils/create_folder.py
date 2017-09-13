import os

def create_folder(temp_folder):
    try:
        if os.path.exists(temp_folder):
            return True
        
        os.mkdir(temp_folder)
        return True

    except Exception as e:
        return False