import os
from PIL import Image
import random
from utils.create_folder import create_folder
from utils.clean_up_folder import clean_up_folder

def binary_quality_search(image_path, output_dir, target_val, cb):

    random_hash = random.randint(100000, 600001)
    temp_dir = os.path.abspath(output_dir) + '/_temp_' + str(random_hash)
    low = 1
    high = 99
    mid = None
    best_quality = -1

    try:

        dir_path, file_name = os.path.split(image_path)
        name, ext = file_name.split('.')
        temp_file = temp_dir + '/' + name + '_' + str(random_hash) + '.' + ext
        passes = 0

        if not create_folder(temp_dir):
            return -1

        while low <= high:

            mid = (high + low) // 2
            
            im = Image.open(image_path)
            im.save(temp_file, format='JPEG', quality=mid, optimize=True)
            
            size = os.stat(temp_file).st_size / 1000

            if size == target_val:
                return mid

            if size > target_val:
                high = mid - 1
            else:
                low = mid + 1

            # size is smalleer than the target val
            # so we have a new best quaility
            if size <= target_val:
                best_quality = mid

            passes += 1

            # let the caller know what
            # percent the process is in.
            # The nature of this search always runs 
            # 7 passes
            if callable(cb):
                cb(to_percent(passes, 7))

    except Exception as e:
        return -1

    finally:
        if(os.path.isdir(temp_dir)):
            clean_up_folder(temp_dir)
    
    # could not match the quality request
    # because it was too low so return the 
    # mid which is lower
    if best_quality == -1 and mid:
        best_quality = mid

    return best_quality


def to_percent(num, total):
    floored_percentage = int(num / total * 100 // 1)
    return str(floored_percentage) + '%'

