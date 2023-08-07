if [ -d "./build" ]; then
    rm -r ./build
fi

if [ -d "./dist" ]; then
    rm -r ./dist
fi

pyinstaller --hidden-import=PyQt5 --collect-submodules=pydicom go_nifti/src/GoNiftiGUI.py --onedir

zip -r ./dist/GoNiftiGUI.zip ./dist/GoNiftiGUI

pyinstaller --hidden-import=PyQt5 --collect-submodules=pydicom go_nifti/src/GoNiftiGUI.py --onefile

pyinstaller --hidden-import=PyQt5 --collect-submodules=pydicom go_nifti/src/GoNifti.py --onedir

zip -r ./dist/GoNifti.zip ./dist/GoNifti

pyinstaller --hidden-import=PyQt5 --collect-submodules=pydicom go_nifti/src/GoNifti.py --onefile

python go_nifti/setup.py bdist_wheel
