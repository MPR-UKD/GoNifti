# GoNifti GUI

GoNifti GUI is a Python-based graphical user interface that allows users to convert DICOM images to Nifti format. This project can be considered as very helpful for radiologists or medical imaging experts who often work with DICOM images and need to convert them to another format that is better suited for further analysis or processing.

![](/assets/img.png)
### Requirements
- Python 3
- PyQt5
- Nibabel
- Numpy
- Pydicom

### Installation
1. Clone the GitHub repository to your computer
```bash
git clone https://github.com/ludgerradke/GoNifti
```
2. Install the required dependencies
```bash
pip install PyQt5 nibabel numpy pydicom
```

### Usage
1. Start the application by running the `GoNiftiGUI.py` script.
````bash
python GoNiftiGUI.py
````
2. Select the root folder that contains the DICOM images to be converted.

3. Select the desired conversion mode:

- `save_in_separate_dir:` The converted Nifti images will be saved in a separate folder that is located in the same parent folder as the root folder and has the name of the root folder with the suffix "_as_nifti".
- `save_in_folder:` The converted Nifti images will be saved in the same folder as the DICOM images and have the name "nifti.nii.gz".
- `save_in_exam_date:` The converted Nifti images will be saved in the same folder as the DICOM images and have the same filename extension as Nifti.
4. Click the "Convert" button.
5. After the conversion is complete, a message will be displayed indicating that the transformation is complete.

### How it works
The script uses the functions `find_dicom_folders` and `dicom_to_nifti` from the `utils` module to find the DICOM folders and convert them to Nifti format, respectively. The `GoNiftiGUI` class creates the graphical user interface and connects the buttons to the appropriate functions. The `dicom_to_nifti` function uses the Nibabel and Pydicom libraries to perform the conversion.

### License
This project is licensed under the GNU 3.0 license and contributions are welcome.

### Executable
The project also includes a compiled executable version of the program in the `dist` folder, which can be used without the need for installing any dependencies or having Python installed on the system. Simply extract the contents of the `GoNifti.zip` archive and run the `go_nifti.exe` file.