import os
import sys

def resource_path(relative_path: str) -> str:
    try:
        return os.path.join(getattr(sys, "_MEIPASS"), relative_path)
    except AttributeError:
        reference_file = sys.modules['__main__'].__file__
        if reference_file:
            return os.path.join(os.path.dirname(reference_file), relative_path)
        raise RuntimeError("Could not resolve resource path")

def runtime_root(relative_path: str):
    reference_file = sys.modules['__main__'].__file__
    if getattr(sys, "frozen", False): # if exe
        reference_file = sys.executable
    if reference_file:
        return os.path.join(os.path.dirname(reference_file), relative_path)
    raise RuntimeError("Program does not have a reference file")
