import cv2
import os
import pandas as pd
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog, QLabel, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QImage, QPixmap
from concurrent.futures import ThreadPoolExecutor
import numpy as np
import qdarkstyle

class CertificateGenerator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        
        # Variables for rectangle and image processing
        self.point1x, self.point1y, self.point2x, self.point2y = 100, 100, 200, 200
        self.image = None
        self.resizeImage = None
        self.height_scale = 0.5
        self.width_scale = 0.5
        self.output_dir = None
        self.csv_data = None
        self.window_name = "Certificate Editor"

    def initUI(self):
        self.setWindowTitle("Certificate Generator")
        self.setGeometry(100, 100, 500, 300)

        # Main layout
        central_widget = QWidget()
        main_layout = QVBoxLayout()

        # Load buttons
        load_image_button = QPushButton("Load Certificate Image")
        load_image_button.clicked.connect(self.load_image)
        main_layout.addWidget(load_image_button)

        load_csv_button = QPushButton("Load CSV File")
        load_csv_button.clicked.connect(self.load_csv)
        main_layout.addWidget(load_csv_button)

        select_output_button = QPushButton("Select Output Directory")
        select_output_button.clicked.connect(self.select_output_directory)
        main_layout.addWidget(select_output_button)

        # Generate button
        generate_button = QPushButton("Generate Certificates")
        generate_button.clicked.connect(self.generate_certificates)
        main_layout.addWidget(generate_button)

        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    def load_image(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Certificate Image")
        if file_path:
            self.image = cv2.imread(file_path)
            if self.image is not None:
                new_size = (int(self.image.shape[1] * self.width_scale), int(self.image.shape[0] * self.height_scale))
                self.resizeImage = cv2.resize(self.image, new_size)
                self.point1x, self.point1y, self.point2x, self.point2y = 50, 50, 150, 150
                self.setup_opencv_window()
                self.statusBar().showMessage("Image loaded and resized successfully.")
            else:
                self.statusBar().showMessage("Failed to load image.")

    def load_csv(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select CSV File")
        if file_path:
            try:
                self.csv_data = pd.read_csv(file_path)
                self.statusBar().showMessage(f"CSV loaded with {len(self.csv_data)} entries.")
            except Exception as e:
                self.statusBar().showMessage(f"Failed to load CSV: {e}")

    def select_output_directory(self):
        directory = QFileDialog.getExistingDirectory(self, "Select Output Directory")
        if directory:
            self.output_dir = directory
            self.statusBar().showMessage(f"Output directory set to: {self.output_dir}")

    def setup_opencv_window(self):
        cv2.namedWindow(self.window_name)

        # Create trackbars for rectangle coordinates
        cv2.createTrackbar("X1", self.window_name, self.point1x, self.resizeImage.shape[1], self.update_rectangle)
        cv2.createTrackbar("Y1", self.window_name, self.point1y, self.resizeImage.shape[0], self.update_rectangle)
        cv2.createTrackbar("X2", self.window_name, self.point2x, self.resizeImage.shape[1], self.update_rectangle)
        cv2.createTrackbar("Y2", self.window_name, self.point2y, self.resizeImage.shape[0], self.update_rectangle)

        while True:
            temp_image = self.resizeImage.copy()
            cv2.rectangle(temp_image, (self.point1x, self.point1y), (self.point2x, self.point2y), (255, 0, 0), 2)
            cv2.imshow(self.window_name, temp_image)

            if cv2.waitKey(1) & 0xFF == 27:  # Press Esc to exit
                cv2.destroyWindow(self.window_name)
                break

    def update_rectangle(self, _):
        self.point1x = cv2.getTrackbarPos("X1", self.window_name)
        self.point1y = cv2.getTrackbarPos("Y1", self.window_name)
        self.point2x = cv2.getTrackbarPos("X2", self.window_name)
        self.point2y = cv2.getTrackbarPos("Y2", self.window_name)

    def generate_certificates(self):
        if self.resizeImage is None or self.csv_data is None or self.output_dir is None:
            self.statusBar().showMessage("Ensure all inputs are loaded before proceeding.")
            return

        self.statusBar().showMessage("Generating certificates...")
        with ThreadPoolExecutor() as executor:
            for _, row in self.csv_data.iterrows():
                name = row.get('Name', 'Unknown')
                executor.submit(self.create_certificate, name)

        self.statusBar().showMessage("Certificates generated successfully.")

    def create_certificate(self, name):
        temp_image = self.resizeImage.copy()
        centrex = (self.point1x + self.point2x) // 2
        cv2.putText(temp_image, name, (centrex - 10, self.point2y), cv2.FONT_HERSHEY_COMPLEX, 1.0, (0, 0, 0), 2)

        output_image = os.path.join(self.output_dir, f"{name}.jpg")
        cv2.imwrite(output_image, temp_image)


if __name__ == "__main__":
    app = QApplication([])
    window = CertificateGenerator()
    window.show()
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    app.exec_()
    cv2.destroyAllWindows()
