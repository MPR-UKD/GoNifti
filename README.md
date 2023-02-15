[![Actions Status](https://github.com/ludgerradke/GoNifti/actions/workflows/python3.10.yml/badge.svg)](https://github.com/ludgerradke/GoNifti/actions/workflows/python3.10.yml/badge.svg)
[![Actions Status](https://github.com/ludgerradke/GoNifti/actions/workflows/python3.11.yml/badge.svg)](https://github.com/ludgerradke/GoNifti/actions/workflows/python3.11.yml/badge.svg)

# GoNifti
GoNifti is a Python-based tool that allows users to convert DICOM images to Nifti format, either through a graphical user interface (GUI) or a command-line interface (CLI).

## Data format
To use GoNifti, the input data must be in a specific format: each subfolder can contain only one MR sequence and the DICOM files must have the ".dcm" file extension. If the input data does not meet these requirements, a tool such as [DicomTranslator](https://github.com/ludgerradke/DICOM_Translator) can be used to preprocess the data.

## Requirements
- Python 3.10
- PyQt5
- Nibabel
- Numpy
- Pydicom
- Click

# Installation
1. Clone the GitHub repository to your computer
```bash
git clone https://github.com/ludgerradke/GoNifti
```
2. Install the required dependencies
```bash
pip install PyQt5 nibabel numpy pydicom click
```

## Usage
### GUI
![](/assets/img.png)
1. Start the application by running the GoNiftiGUI.py script.
```bash
python GoNiftiGUI.py
```
2. Select the root folder that contains the DICOM images to be converted.

3. Select the desired conversion mode:

- `save_in_separate_dir`: The converted Nifti images will be saved in a separate folder that is located in the same parent folder as the root folder and has the name of the root folder with the suffix "_as_nifti".
- `save_in_folder`: The converted Nifti images will be saved in the same folder as the DICOM images and have the name "nifti.nii.gz".
- `save_in_exam_date`: The converted Nifti images will be saved in the same folder as the DICOM images and have the same filename extension as Nifti.

4. Click the "Convert" button.
5. After the conversion is complete, a message will be displayed indicating that the transformation is complete.

### CLI
```bash
$ python .\GoNifti.py --help

Usage: GoNifti.py [OPTIONS] ROOT_FOLDER

Options:
  --mode [save_in_separate_dir|save_in_folder|save_in_exam_date]
  --cpus [1|2|3|4|5|6|7|8|9|10|11|12]
  --help                          Show this message and exit.
```

```bash
$ python .\GoNifti.py <path>

Found 161 DICOM folders.
Converting DICOM to NIFTI  [####################################]  100%          
Transformation completed.
```

1. Open a terminal and navigate to the project directory.
2. Run the CLI script by using the command `pathon gonifti [ROOT_FOLDER] --mode [MODE] --cpus [CPUS]`, where `ROOT_FOLDER` is the path to the folder containing the DICOM images to be converted, `MODE` is the desired conversion mode (save_in_separate_dir, save_in_folder, or save_in_exam_date), and `CPUS` is the number of CPUs to use for the conversion process (default is 1).
3. After the conversion is complete, a message will be displayed indicating that the transformation is complete.

For example, to convert DICOM images in the folder /path/to/dicom/folder using the save_in_separate_dir conversion mode and 4 CPUs, you would run the following command:
```bash
python gonifti.py /path/to/dicom/folder --mode save_in_separate_dir --cpus 4
```

## License
This project is licensed under the GNU 3.0 license and contributions are welcome.

## Executable
The project also includes a compiled executable version of the program in the **dist** folder, which can be used without the need for installing any dependencies or having Python installed on the system.