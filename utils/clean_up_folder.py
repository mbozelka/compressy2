import os

def clean_up_folder(temp_folder):

    try:
        for temp_file in os.listdir(temp_folder):
            file_path = os.path.join(temp_folder, temp_file)
            os.unlink(file_path)
        
        os.rmdir(temp_folder)
        return True

    except Exception as e:
        return False
