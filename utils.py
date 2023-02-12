import os
from pathlib import Path
from typing import List


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
