import os
import shutil

# python go_exe.py
if os.path.exists(r"./build"):
    shutil.rmtree(r"./build")
if os.path.exists(r"./dist"):
    shutil.rmtree(r"./dist")
os.system(
    "pyinstaller --hidden-import=PyQt5 --collect-submodules=pydicom GoNiftiGUI.py --onedir"
)
os.system(
    "pyinstaller --hidden-import=PyQt5 --collect-submodules=pydicom GoNiftiGUI.py --onefile"
)
os.system(
    "pyinstaller --hidden-import=PyQt5 --collect-submodules=pydicom GoNifti.py --onedir"
)
os.system(
    "pyinstaller --hidden-import=PyQt5 --collect-submodules=pydicom GoNifti.py --onefile"
)