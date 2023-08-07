import os
import sys
from pathlib import Path

import click
import dicom2nifti

from go_nifti.src.utils import find_dicom_folders, dicom_to_nifti, save_nifti
from go_nifti.src.utils import nifti_change_dtype
import multiprocessing


def validate_root_folder(ctx, param, value):
    if not Path(value).exists():
        raise click.BadParameter(f"Folder {value} does not exist.")
    return Path(value)


def convert_dicom_to_nifti(
    folder: Path, save_path: Path, out_dtype: str | None = None
) -> None:
    """
    Function to convert a DICOM folder to NIFTI format
    """
    stdout, stderr = sys.stdout, sys.stderr
    with open(os.devnull, "w") as f:
        sys.stdout = f
        sys.stderr = f
        try:
            dicom2nifti.dicom_series_to_nifti(folder, save_path)
        except:
            img = dicom_to_nifti(folder)
            save_nifti(img, save_path)
        if out_dtype is not None:
            nifti_change_dtype(nii_path=save_path, dtype=out_dtype)
    sys.stdout = stdout
    sys.stderr = stderr


def convert(
    root_folder: Path,
    mode: str,
    n_processes: int = 1,
    out_dtype: str | None = None,
    compress: bool = False,
) -> None:
    dicom_folders = find_dicom_folders(root_folder)
    click.echo(f"Found {len(dicom_folders)} DICOM folders.")

    with multiprocessing.Pool(processes=n_processes) as pool:
        results = []
        count = 0
        total = len(dicom_folders)
        suffix = ".nii.gz" if compress else ".nii"
        with click.progressbar(length=total, label="Converting DICOM to NIFTI") as bar:
            for folder in dicom_folders:
                if mode == "save_in_folder":
                    save_path = folder / f"nifti{suffix}"
                elif mode == "save_in_exam_date":
                    save_path = folder.with_suffix(suffix)
                elif mode == "save_in_separate_dir":
                    nii_root = root_folder.name + "_as_nifti"
                    nii_root_folder = root_folder.parent / nii_root
                    nii_root_folder.mkdir(exist_ok=True)
                    rel_path = folder.relative_to(root_folder)
                    save_path = nii_root_folder / (rel_path.with_suffix(suffix))
                else:
                    raise click.ClickException("Invalid mode.")
                save_path.parent.mkdir(parents=True, exist_ok=True)

                result = pool.apply_async(
                    convert_dicom_to_nifti, args=(folder, save_path, out_dtype)
                )
                results.append(result)

            # Monitor progress
            for result in results:
                result.wait()
                count += 1
                bar.update(count - bar.pos)

    click.echo("Transformation completed.")


@click.command()
@click.argument("root_folder", callback=validate_root_folder)
@click.option(
    "--mode",
    default="save_in_separate_dir",
    type=click.Choice(["save_in_separate_dir", "save_in_folder", "save_in_exam_date"]),
)
@click.option(
    "--cpus",
    default="1",
    type=click.Choice([str(i + 1) for i in range(multiprocessing.cpu_count())]),
)
@click.option(
    "--out_dtype", default=None, type=click.Choice(["int32", "float32", "float64"])
)
def cli(root_folder, mode, cpus, out_dtype):
    convert(
        root_folder=root_folder, mode=mode, n_processes=int(cpus), out_dtype=out_dtype
    )


@click.option("--compress", default=True, type=click.Choice([True, False]))
def cli(root_folder, mode, cpus, out_dtype, compress):
    convert(
        root_folder=root_folder,
        mode=mode,
        n_processes=int(cpus),
        out_dtype=out_dtype,
        compress=compress,
    )


if __name__ == "__main__":
    cli()
