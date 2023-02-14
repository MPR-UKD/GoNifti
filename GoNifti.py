import click
import time
from pathlib import Path
from utils import find_dicom_folders, dicom_to_nifti, save_nifti


def validate_root_folder(ctx, param, value):
    if not Path(value).exists():
        raise click.BadParameter(f"Folder {value} does not exist.")
    return Path(value)


@click.command()
@click.argument('root_folder', callback=validate_root_folder)
@click.option('--mode', default='save_in_separate_dir', type=click.Choice(['save_in_separate_dir', 'save_in_folder', 'save_in_exam_date']))
def convert(root_folder, mode):
    dicom_folders = find_dicom_folders(root_folder)
    click.echo(f"Found {len(dicom_folders)} DICOM folders.")
    with click.progressbar(dicom_folders, label="Converting DICOM to NIFTI") as bar:
        for folder in bar:
            nifti_img = dicom_to_nifti(folder)
            if not nifti_img:
                continue
            if mode == 'save_in_folder':
                save_path = folder / 'nifti.nii.gz'
            elif mode == 'save_in_exam_date':
                save_path = folder.with_suffix('.nii.gz')
            elif mode == 'save_in_separate_dir':
                nii_root = root_folder.name + '_as_nifti'
                nii_root_folder = root_folder.parent / nii_root
                nii_root_folder.mkdir(exist_ok=True)
                rel_path = folder.relative_to(root_folder)
                save_path = nii_root_folder / (rel_path.with_suffix('.nii.gz'))
            else:
                raise click.ClickException("Invalid mode.")
            save_nifti(nifti_img, save_path)
    click.echo("Transformation completed.")


if __name__ == '__main__':
    convert()
