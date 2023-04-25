import os
import re
import sys
from pprint import pprint

from PySide6.QtCore import QSettings
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QApplication,
    QFileDialog,
    QHeaderView,
    QLabel,
    QMainWindow,
    QMessageBox,
    QSizePolicy,
    QSpacerItem,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from src.AssetManager import AssetManager
from src.DecodeHelper import DecodeHelper
from src.EncodeHelper import EncodeHelper


class AzurLaneTachieHelper(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AzurLaneTachieHelper")
        self.setWindowIcon(QIcon("ico/cheshire.ico"))
        self.resize(720, 480)

        self.settings = QSettings("config.ini", QSettings.Format.IniFormat)

        self._init_ui()
        self._init_statusbar()
        self._init_menu()

        self.asset_manager = AssetManager()
        self.decoder = DecodeHelper(self.asset_manager)
        self.encoder = EncodeHelper(self.asset_manager)

    def _layout_abd(self):  # Layout for Assetbundle Dependencies
        label = QLabel("Assetbundle Dependencies")
        label.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        self.tDependency = QTableWidget()
        self.tDependency.setColumnCount(2)
        self.tDependency.setHorizontalHeaderLabels(["Part Name", "Full Path"])
        self.tDependency.horizontalHeader().setSectionResizeMode(
            0, QHeaderView.ResizeMode.ResizeToContents
        )
        self.tDependency.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.tDependency.setSizePolicy(
            QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Fixed
        )

        layout = QVBoxLayout()
        layout.addWidget(label)
        layout.addWidget(self.tDependency)

        return layout

    def _layout_ir(self):  # Layout for Image Replacers
        label = QLabel("Image Replacers")
        label.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        self.tReplacer = QTableWidget()
        self.tReplacer.setColumnCount(2)
        self.tReplacer.setHorizontalHeaderLabels(["Target", "Image Source"])
        self.tReplacer.horizontalHeader().setSectionResizeMode(
            0, QHeaderView.ResizeMode.ResizeToContents
        )
        self.tReplacer.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.tReplacer.setSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Fixed)

        layout = QVBoxLayout()
        layout.addWidget(label)
        layout.addWidget(self.tReplacer)

        return layout

    def _init_ui(self):
        layout = QVBoxLayout()
        layout.addLayout(self._layout_abd())
        layout.addLayout(self._layout_ir())
        layout.addItem(QSpacerItem(0, 0, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding))

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def _init_statusbar(self):
        self.message = QLabel("Ready")
        self.message.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.statusBar().addWidget(self.message)
        self.statusBar().setStyleSheet("QStatusBar::item{border:0px}")

    def _init_menu(self):
        self.mFile = self.menuBar().addMenu("&File")

        self.mFileOpenMetadata = self.mFile.addAction("&Open Metadata")
        self.mFileOpenMetadata.triggered.connect(self.onClickFileOpenMetadata)
        self.mFileOpenMetadata.setCheckable(False)
        self.mFileOpenMetadata.setEnabled(True)
        self.mFileOpenMetadata.setShortcut("Ctrl+M")

        self.mFileImportReplacers = self.mFile.addAction("&Import Replacers")
        self.mFileImportReplacers.triggered.connect(self.onClickFileImportReplacers)
        self.mFileImportReplacers.setCheckable(False)
        self.mFileImportReplacers.setEnabled(False)
        self.mFileImportReplacers.setShortcut("Ctrl+I")

        self.mEdit = self.menuBar().addMenu("&Edit")

        self.mEditDecode = self.mEdit.addAction("&Decode Texture")
        self.mEditDecode.triggered.connect(self.onClickEditDecode)
        self.mEditDecode.setCheckable(False)
        self.mEditDecode.setEnabled(False)
        self.mEditDecode.setShortcut("Ctrl+D")

        self.mEditEncode = self.mEdit.addAction("&Encode Texture")
        self.mEditEncode.triggered.connect(self.onClickEditEncode)
        self.mEditEncode.setCheckable(False)
        self.mEditEncode.setEnabled(False)
        self.mEditEncode.setShortcut("Ctrl+E")

    def onClickFileOpenMetadata(self):
        last = self.settings.value("File/Path", "")
        file, _ = QFileDialog.getOpenFileName(self, "Select Metadata to Open", last)
        if file:
            self.settings.setValue("File/Path", file)
            self.message.setText(f"({os.path.basename(file)})  {file}")
            print("[INFO] Metadata:", file)

            self.asset_manager.analyze(file)
            pprint(self.asset_manager.metas)

            print("[INFO] Dependencies:", self.asset_manager.deps)
            num_deps = len(self.asset_manager.deps)
            self.tDependency.clearContents()
            self.tDependency.setRowCount(num_deps)
            self.tReplacer.setRowCount(num_deps)
            for i, x in enumerate(self.asset_manager.deps):
                self.tDependency.setItem(i, 0, QTableWidgetItem(x))
                self.tDependency.setItem(i, 1, QTableWidgetItem("Not Found"))
                self.tReplacer.setItem(i, 0, QTableWidgetItem(x))

                path = os.path.join(os.path.dirname(file) + "/", x)
                if os.path.exists(path):
                    print("[INFO] Auto-resolved:", path)
                    self.tDependency.setItem(i, 1, QTableWidgetItem(path))
                    self.asset_manager.extract(x, path)

            self.mFileImportReplacers.setEnabled(True)
            self.mEditDecode.setEnabled(True)

    def onClickFileImportReplacers(self):
        last = self.settings.value("File/Path", "")
        files, _ = QFileDialog.getOpenFileNames(self, dir=last)
        if files:
            print("[INFO] Replacers:")
            [print("      ", _) for _ in files]

            for i in range(self.tReplacer.rowCount()):
                name = re.split(r"/|_tex", self.tReplacer.item(i, 0).text())[-2].lower()
                self.tReplacer.setItem(i, 1, QTableWidgetItem(files[i]))
                self.encoder.load_replacer(name, files[i])

            self.mEditEncode.setEnabled(True)

    def onClickEditDecode(self):
        last = self.settings.value("File/Path", "")
        dir = QFileDialog.getExistingDirectory(self, "Select Output Folder", os.path.dirname(last))
        if dir:
            path = self.decoder.exec(dir + "/")
            msg_box = QMessageBox()
            msg_box.setText(f"Successfully written into:\n{path}")
            msg_box.setStandardButtons(
                QMessageBox.StandardButton.Open | QMessageBox.StandardButton.Ok
            )
            if msg_box.exec() == QMessageBox.StandardButton.Open:
                os.startfile(dir)

    def onClickEditEncode(self):
        last = self.settings.value("File/Path", "")
        dir = QFileDialog.getExistingDirectory(self, dir=os.path.dirname(last))
        if dir:
            path = self.encoder.exec(dir + "/")
            msg_box = QMessageBox()
            msg_box.setText(f"Successfully written into:\n{path}")
            msg_box.setStandardButtons(
                QMessageBox.StandardButton.Open | QMessageBox.StandardButton.Ok
            )
            if msg_box.exec() == QMessageBox.StandardButton.Open:
                os.startfile(dir)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = AzurLaneTachieHelper()

    win.show()
    app.exec()
