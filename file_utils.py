import os
import time
import shutil
from datetime import datetime

BAK_DIR_NAME = 'bak'

def back_dir(src_dir):
    if not os.path.exists(src_dir):
        return None
    else:
        count = 0
        bak_dir = os.path.join(src_dir, BAK_DIR_NAME)
        if not os.path.exists(bak_dir):
            os.makedirs(bak_dir)
        now = datetime.now()
        date_string = now.strftime("%Y%m%d%H%M%S")
        for filename in os.listdir(src_dir):
            src_filename = os.path.join(src_dir, filename)
            print(f'src_filename: {src_filename}')
            # skip hidden files / folders / bak folder itself
            if (not os.path.isfile(src_filename)) or filename.startswith('.') or filename.startswith('bak'):
                continue
            # Create the backup filename by appending the date and time string
            backup_filename = os.path.join(bak_dir, f"{filename}.{date_string}")
            # Move the file to the backup location
            print(f'move :{src_filename} to {backup_filename}')
            shutil.move(src_filename, backup_filename)
            count = count + 1

        return count 

def download_wait(path_to_downloads, timeout_s):
    seconds = 0
    dl_wait = True
    while dl_wait and seconds < timeout_s:
        time.sleep(1)
        dl_wait = False
        for fname in os.listdir(path_to_downloads):
            if fname.endswith('.crdownload'):
                dl_wait = True
        seconds += 1
    return seconds