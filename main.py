import os
import shutil

source = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
os.makedirs("/output", exist_ok=True)
shutil.copyfile(source, "/output/entry.png")
