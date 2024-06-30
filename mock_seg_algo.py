import time
import shutil
import sys
import os
# copy an image from one folder to the other after the function being called in 1 minute
def mock_seg_algo(input_path):
    os.mkdir("working_dir")
    # copy the target image to the working directory
    shutil.copy2(input_path, "working_dir/input_image.png")
    time.sleep(60)
    shutil.copy2("imgs/mask_1.png", "working_dir/output_img.png")
    print("mock_seg_algo: done!")
    return

if __name__ == "__main__":
    # obtain the input path from the command line
    input_path = sys.argv[1]
    mock_seg_algo(input_path)