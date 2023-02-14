import pytest
from pathlib import Path
from utils import find_dicom_folders


def test_find_dicom_folders(tmp_path):
    # create test directory structure
    root = tmp_path / "test"
    root.mkdir()
    subdirs = [
        "subdir1",
        "subdir2",
        "subdir3",
        "subdir4",
        "subdir5",
        "subdir6",
        "subdir7",
    ]
    for subdir in subdirs:
        (root / subdir).mkdir()
        with open(root / subdir / "file.txt", "w") as f:
            f.write("test")

    # create dicom files in test subdirectories
    dicom_files = [
        "image1.dcm",
        "image2.dcm",
        "image3.dcm",
        "image4.dcm",
        "image5.dcm",
        "image6.dcm",
    ]
    for i, subdir in enumerate(subdirs[:6]):
        dicom_dir = root / subdir / f"dicom{i+1}"
        dicom_dir.mkdir()
        for dicom_file in dicom_files:
            with open(dicom_dir / dicom_file, "w") as f:
                f.write("test")

    # find dicom folders
    dicom_folders = find_dicom_folders(root)

    # check that correct folders are found
    expected_folders = [root / subdir / f"dicom{i+1}" for i, subdir in enumerate(subdirs[:6])]
    assert dicom_folders == expected_folders
