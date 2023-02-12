import os
from pathlib import Path
from typing import List

import nibabel as nib
import numpy as np
import pydicom


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


def dicom_to_nifti(folder: Path, verbose: bool = False) -> nib.Nifti1Image:
    # Load all DICOM images in the folder
    dicom_files = [pydicom.dcmread(str(file)) for file in folder.glob('*.dcm')]

    # Determine the changing parameter
    changing_parameters = set()
    for d in dicom_files:
        changing_parameters |= set(d.keys())
    changing_parameters -= set(dicom_files[0].keys())

    if verbose:
        print(f"Changed parameters detected: {changing_parameters}")
    # Use the first changing parameter found as the organizing parameter
    organizing_parameter = list(changing_parameters)[0] if changing_parameters else None

    # Organize the DICOM images based on the organizing parameter if found
    if organizing_parameter:
        dicom_files.sort(key=lambda x: x.get(organizing_parameter, 0))
        if verbose:
            print(f"Organizing parameter: {organizing_parameter}")

    # Convert the DICOM images to a 4D Nifti array
    image_data = np.stack([d.pixel_array for d in dicom_files])
    affine = dicom_files[0].affine

    header = nib.Nifti1Header()
    # Transfer DICOM header information to Nifti header
    for key, value in dicom_files[0].items():
        if key not in header:
            try:
                header[key] = value
            except:
                pass

    nifti_img = nib.Nifti1Image(image_data, affine, header)

    return nifti_img


def save_nifti(nifti_img: nib.Nifti1Image, filename: Path):
    nib.save(nifti_img, str(filename))