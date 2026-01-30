import os
from utils.path import resource_path
import time

def load(libs_folder_name="libs"):
    start_time = time.perf_counter()
    libs_root = resource_path(libs_folder_name)

    for item_name in os.listdir(libs_root):
        full_path = os.path.join(libs_root, item_name)
        if os.path.isdir(full_path) and full_path not in os.environ["PATH"]:
            os.environ["PATH"] = full_path + os.pathsep + os.environ["PATH"]
    print(f"Libs loaded in {time.perf_counter()-start_time}")