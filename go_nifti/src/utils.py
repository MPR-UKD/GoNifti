import os
from pathlib import Path
from typing import List

import nibabel as nib
import numpy as np
import pydicom
from nibabel import Nifti1Image


def sort_dicom_files(dicom_files: List[pydicom.Dataset]) -> List:
    positions = {}
    for dicom_file in dicom_files:
        position = tuple(dicom_file.ImagePositionPatient)
        if position in positions:
            positions[position].append(dicom_file)
        else:
            positions[position] = [dicom_file]
    sorted_positions = sorted(positions.items(), key=lambda x: x[0][2])
    return [files for position, files in sorted_positions]


def find_dicom_folders(root_folder: Path) -> List[Path]:
    dicom_folders = []
    for root, dirs, files in os.walk(str(root_folder)):
        root = Path(root)
        has_dicom_files = False
        for file in files:
            if file.endswith('.dcm'):
                has_dicom_files = True
                break
        if has_dicom_files:
            dicom_folders.append(root)
    return dicom_folders

def dicom_to_nifti(folder: Path, verbose: bool = True) -> Nifti1Image | None:
    # Load all DICOM images in the folder
    dicom_files = [pydicom.dcmread(str(file)) for file in folder.glob('*.dcm')]

    if "MIMETypeOfEncapsulatedDocument" in dicom_files[0]:
        return None

    #Sort dicom files based on the image position
    dicom_files = sort_dicom_files(dicom_files)

    # Convert the DICOM images to a 4D Nifti array
    image_data = []
    for idx in range(len(dicom_files[0])):
        image_data.append([d[idx].pixel_array for d in dicom_files])

    image_data = np.array(image_data).transpose((1,2,3,0))
    affine = np.eye(4)

    header = nib.Nifti1Header()
    # Transfer DICOM header information to Nifti header
    for idx in range(len(dicom_files[0])):
        for key, value in dicom_files[0][idx].items():
            if key not in header:
                try:
                    header[key] = value
                except:
                    pass
            elif header[key] != value:
                if type(header[key]) != list:
                    header[key] = list(header[key])
                header[key].append(value)

    nifti_img = nib.Nifti1Image(image_data, affine, header)

    return nifti_img


def save_nifti(nifti_img: nib.Nifti1Image, filename: Path):
    filename.parent.mkdir(parents=True, exist_ok=True)
    nib.save(nifti_img, str(filename))