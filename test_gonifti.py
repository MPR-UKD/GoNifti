import shutil
from pathlib import Path

from pydicom.data import get_testdata_files

from go_nifti.src.GoNifti import convert


def test_find_dicom_folders(tmp_path):
    # create test directory structure
    root = tmp_path / "test" / "dicom_dir"
    root.mkdir(parents=True)

    # load a DICOM file from pydicom test data and save it in the test directory
    for dcm_file in get_testdata_files("CT_small.dcm"):
        shutil.copy(dcm_file, root / Path(dcm_file).name)

    # call the conversion function with the test directory
    convert(root_folder=root.parent, mode='save_in_separate_dir')
    assert (root.parent / (root.parent.name + '_as_nifti')).exists()(root.parent.parent / (root.parent.name + '_as_nifti')).exists() == True
