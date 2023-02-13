import os
import shutil

# python go_exe.py
if os.path.exists(r"./build"):
    shutil.rmtree(r"./build")
if os.path.exists(r"./dist"):
    shutil.rmtree(r"./dist")
os.system(
    "pyinstaller --collect-submodules=pydicom GoNiftiGUI.py --onedir"
)
shutil.make_archive("./dist/DICOMTranslator", "zip", "./dist/go_nifti")
os.system(
    "pyinstaller --collect-submodules=pydicom GoNiftiGUI.py --onefile"
)
