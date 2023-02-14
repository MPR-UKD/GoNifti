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
