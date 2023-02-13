from pathlib import Path
import PyQt5.QtWidgets as QtWidgets
import sys
import ctypes

from utils import find_dicom_folders, dicom_to_nifti, save_nifti


class GoNiftiGUI(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("GoNifti GUI")
        self.resize(600, 60)

        self.root_folder_label = QtWidgets.QLabel("Root folder:")
        self.root_folder_edit = QtWidgets.QLineEdit()
        self.root_folder_button = QtWidgets.QPushButton("Select")

        self.mode_label = QtWidgets.QLabel("Mode:")
        self.mode_combo = QtWidgets.QComboBox()
        self.mode_combo.addItems(["save_in_separate_dir", "save_in_folder", "save_in_exam_date"])

        self.progress_bar = QtWidgets.QProgressBar()

        self.convert_button = QtWidgets.QPushButton("Convert")

        self.root_folder_layout = QtWidgets.QHBoxLayout()
        self.root_folder_layout.addWidget(self.root_folder_label)
        self.root_folder_layout.addWidget(self.root_folder_edit)
        self.root_folder_layout.addWidget(self.root_folder_button)

        self.mode_layout = QtWidgets.QHBoxLayout()
        self.mode_layout.addWidget(self.mode_label)
        self.mode_layout.addWidget(self.mode_combo)

        self.main_layout = QtWidgets.QVBoxLayout()
        self.main_layout.addLayout(self.root_folder_layout)
        self.main_layout.addLayout(self.mode_layout)
        self.main_layout.addWidget(self.progress_bar)
        self.main_layout.addWidget(self.convert_button)

        self.main_widget = QtWidgets.QWidget()
        self.main_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.main_widget)

        self.root_folder_button.clicked.connect(self.select_root_folder)
        self.convert_button.clicked.connect(self.convert)

    def select_root_folder(self):
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.ReadOnly
        folder = QtWidgets.QFileDialog.getExistingDirectory(self, "Select root folder", self.root_folder_edit.text(),
                                                            options=options)
        if folder:
            self.root_folder_edit.setText(folder)

    def convert(self):
        root_folder = Path(self.root_folder_edit.text())
        mode = self.mode_combo.currentText()
        dicom_folders = find_dicom_folders(root_folder)
        self.progress_bar.setMaximum(len(dicom_folders))
        for i, folder in enumerate(dicom_folders):
            nifti_img = dicom_to_nifti(folder)
            if not nifti_img:
                continue
            if mode == 'save_in_folder':
                save_path = folder / 'nifti.nii.gz'
            elif mode == 'save_in_exam_date':
                save_path = folder.with_suffix('.nii.gz')
            elif mode == 'save_in_separate_dir':
                nii_root = root_folder.parent / (root_folder.name + '_as_nifti')
                nii_root.mkdir(exist_ok=True)
                rel_path = folder.relative_to(root_folder)
                save_path = nii_root / (rel_path.with_suffix('.nii.gz'))
            else:
                raise IndexError
            save_nifti(nifti_img, save_path)
            self.progress_bar.setValue(i + 1)
        self.root_folder_edit.clear()
        self.progress_bar.close()
        ctypes.windll.user32.MessageBoxW(
            0,
            f"Transformation completed",
            1,
        )


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = GoNiftiGUI()
    window.show()
    sys.exit(app.exec_())

