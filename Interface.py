from PyQt4 import QtGui, QtCore
from PIL import Image, ImageQt
import Editor
import sys
import random

class MainWindow:

    def __init__(self):
        self.main = QtGui.QMainWindow()
        self.w = QtGui.QWidget()
        self.main.setCentralWidget(self.w)
        self.b = QtGui.QLabel(self.w)
        self.original = None
        self.display_image = None
        self.image = None
        self.pixel= None
        self.new_pixel = None
        self.image_copy = None
        self.operations = Editor.Editor(self.image, self.image_copy, self.pixel, self.new_pixel)
        self.middle_y = 225
        self.pixmap_image = None
        self.pixmap_original = None
        self.previous_image = None
        self.file = None
        self.gray_flag = False
        self.label_original = QtGui.QLabel(self.w)
        self.label_image = QtGui.QLabel(self.w)
        self.original_label = QtGui.QLabel(self.w)
        self.modified_label = QtGui.QLabel(self.w)

    def create_main_window(self):
        
        menu = self.main.menuBar()
        
        load_action = QtGui.QAction("Load image", menu)
        load_action.triggered.connect(self.load_file)
        
        save_action =  QtGui.QAction("Save image", menu)
        save_action.triggered.connect(self.save_file)
        
        file = menu.addMenu("File")
        file.addAction(load_action)
        file.addAction(save_action)
        
        rotation_clockwise_action = QtGui.QAction("Rotate clockwise", menu)
        rotation_clockwise_action.triggered.connect(self._rotate_clockwise)
        
        rotation_counter_clockwise_action = QtGui.QAction("Rotate counter-clockwise", menu)
        rotation_counter_clockwise_action.triggered.connect(self._rotate_counter_clockwise)

        flip_horizontally_action = QtGui.QAction("Flip horizontally", menu)
        flip_horizontally_action.triggered.connect(self._horizontal_flip)
        
        flip_vertically_action = QtGui.QAction("Flip vertically", menu)
        flip_vertically_action.triggered.connect(self._vertical_flip)

        rotation = menu.addMenu("Rotations")
        rotation.addAction(rotation_clockwise_action)
        rotation.addAction(rotation_counter_clockwise_action)
        rotation.addAction(flip_horizontally_action)
        rotation.addAction(flip_vertically_action)
                
        add_custom_filter_action = QtGui.QAction("Add custom filter", menu)
        add_custom_filter_action.triggered.connect(self._add_custom_filter)
        
        negative_action = QtGui.QAction("Negative", menu)
        negative_action.triggered.connect(self._negative)
        
        grayscale_action = QtGui.QAction("Grayscale", menu)
        grayscale_action.triggered.connect(self._grayscale)
        
        quantization_action = QtGui.QAction("Quantization", menu)
        quantization_action.triggered.connect(self._quantization)
        
        adjust_brightness_action = QtGui.QAction("Adjust brightness", menu)
        adjust_brightness_action.triggered.connect(self._adjust_brightness)
        
        adjust_contrast_action = QtGui.QAction("Adjust contrast", menu)
        adjust_contrast_action.triggered.connect(self._adjust_contrast)
        
        transformations = menu.addMenu("Transformations")
        
        add_filter = transformations.addMenu("Add filters")
        
        add_gaussian_action = QtGui.QAction("Gaussian", add_filter)
        add_gaussian_action.triggered.connect(self._gaussian_filter)
        
        add_laplacian_action = QtGui.QAction("Laplacian", add_filter)
        add_laplacian_action.triggered.connect(self._laplacian_filter)
        
        add_generic_highpass_action = QtGui.QAction("Generic Highpass", add_filter)
        add_generic_highpass_action.triggered.connect(self._generic_highpass_filter)
        
        add_prewitt_hx_action = QtGui.QAction("Prewitt Hx", add_filter)
        add_prewitt_hx_action.triggered.connect(self._prewitt_hx_filter)
        
        add_prewitt_hy_action = QtGui.QAction("Prewitt Hy", add_filter)
        add_prewitt_hy_action.triggered.connect(self._prewitt_hy_filter)
        
        add_sobel_hx_action = QtGui.QAction("Sobel Hx", add_filter)
        add_sobel_hx_action.triggered.connect(self._sobel_hx_filter)
        
        add_sobel_hy_action = QtGui.QAction("Sobel Hy", add_filter)
        add_sobel_hy_action.triggered.connect(self._sobel_hy_filter)
        
        add_filter.addAction(add_gaussian_action)
        add_filter.addAction(add_laplacian_action)
        add_filter.addAction(add_generic_highpass_action)
        add_filter.addAction(add_prewitt_hx_action)
        add_filter.addAction(add_prewitt_hy_action)
        add_filter.addAction(add_sobel_hx_action)
        add_filter.addAction(add_sobel_hy_action)

        
        transformations.addAction(add_custom_filter_action)
        transformations.addAction(adjust_brightness_action)
        transformations.addAction(adjust_contrast_action)
        transformations.addAction(negative_action)
        transformations.addAction(grayscale_action)
        transformations.addAction(quantization_action)
        
        show_histogram_action = QtGui.QAction("Show histogram", menu)
        show_histogram_action.triggered.connect(self._histogram)
        
        equalize_histogram_action = QtGui.QAction("Equalize histogram", menu)
        equalize_histogram_action.triggered.connect(self._equalize_histogram)
        
        histogram = menu.addMenu("Histogram operations")
        histogram.addAction(show_histogram_action)
        histogram.addAction(equalize_histogram_action)
        
        zoom_in_action = QtGui.QAction("Zoom in", menu)
        zoom_in_action.triggered.connect(self._zoom_in)
        
        zoom_out_action = QtGui.QAction("Zoom out", menu)
        zoom_out_action.triggered.connect(self._zoom_out)
        
        zooms = menu.addMenu("Zooms")
        zooms.addAction(zoom_in_action)
        zooms.addAction(zoom_out_action)
        
        self.info_label = QtGui.QLabel(self.w)
        self.info_label.setText("Ana Paula Mello - 260723")
        self.info_label.move (360, 470)
      
        self.main.resize(500, 510)
        self.main.move(100, 100)
        self.main.setWindowTitle("Image Operations")
        self.main.show()
            
    def load_file(self):
    
        self.file = QtGui.QFileDialog.getOpenFileName(self.w, "Open file")
        
        if len(self.file) != 0:
       
            self.operations.image = Image.open(str(self.file))
            self.operations.new_image = Image.open(str(self.file))
            self.operations.image_pixels = self.operations.image.load()
            self.operations.new_image_pixels = self.operations.new_image.load()
                            
            self.qim = ImageQt.ImageQt(self.operations.image)
            self.original = ImageQt.ImageQt(self.operations.image)
            self.display_image = Image.open(str(self.file))
            self.display_image_info = ImageQt.ImageQt(self.display_image)
          
            self._show_image(self.qim, self.display_image_info)

    def save_file(self):
        if self.file == None or len(self.file) == 0:
            warning = QtGui.QMessageBox()
            warning.setIcon(QtGui.QMessageBox.Critical)
            warning.setText("You need to load an image first")
            warning.exec_()
        else:
            self.file = QtGui.QFileDialog.getSaveFileName(self.w, "Save file", "image.jpg", filter="jpg (*.jpg *.)")
            self.operations.image.save(str(self.file))
        
    def _show_image(self, image, original):
        
        self.original_label.setText("Original image")
        self.modified_label.setText("Modified image")
   
        self.pixmap_original =  QtGui.QPixmap.fromImage(original)
        self.pixmap_original.detach()

        self.pixmap_image = QtGui.QPixmap.fromImage(image)
        self.pixmap_image.detach()
        self.label_image.clear()

        self.label_original.setPixmap(self.pixmap_original)
        self.label_original.move(30, 30)
        self.label_original.resize(self.display_image.size[0], self.display_image.size[1])
        self.label_original.show()
        
        self.original_label.move(30, 10)
        self.original_label.setMinimumWidth(100)
        self.original_label.show()
        
        self.modified_label.move(self.display_image.size[0] + 60, 10)
        self.modified_label.setMinimumWidth(100)
        self.modified_label.show()

        self.label_image.clear()
        self.label_image.resize(self.operations.new_image.size[0], self.operations.new_image.size[1])
        self.label_image.move(self.display_image.size[0] + 60, 30)
        
        self.label_image.setPixmap(self.pixmap_image)
        self.label_image.show()
        
        if self.display_image.size[1] > self.operations.new_image.size[1]:
            self.main.resize(self.operations.new_image.size[0]+self.display_image.size[0]+90, self.display_image.size[1]+100)
        else:
            self.main.resize(self.operations.new_image.size[0]+self.display_image.size[0]+90, self.operations.new_image.size[1]+100)
        self.main.show()
        
    def _prepare_image(self):
        pass
        
    def _update_image(self):
        pass
      
    def _horizontal_flip(self):
    
        if self.file == None or len(self.file) == 0:
            warning = QtGui.QMessageBox()
            warning.setIcon(QtGui.QMessageBox.Critical)
            warning.setText("You need to load an image first")
            warning.exec_()
        else:
            # New Image objects to be updated
            self.operations.new_image = Image.open(str(self.file))
            self.operations.new_image_pixels = self.operations.new_image.load()

            self.operations.horizontal_flip()
            
            # Updating the Image object with the new data
            self.operations.image = self.operations.new_image
            self.operations.image_pixels = self.operations.new_image_pixels
            new = ImageQt.ImageQt(self.operations.image)
            self._show_image(new, self.original)
        
    def _vertical_flip(self):
    
        if self.file == None or len(self.file) == 0:
            warning = QtGui.QMessageBox()
            warning.setIcon(QtGui.QMessageBox.Critical)
            warning.setText("You need to load an image first")
            warning.exec_()
        else:
            # New Image objects to be updated
            self.operations.new_image = Image.open(str(self.file))
            self.operations.new_image_pixels = self.operations.new_image.load()
            
            self.operations.vertical_flip()

            # Updating the Image object with the new data
            self.operations.image = self.operations.new_image
            self.operations.image_pixels = self.operations.new_image_pixels
            new = ImageQt.ImageQt(self.operations.image)
            self._show_image(new, self.original)

    def _grayscale(self):
    
        if self.file == None or len(self.file) == 0:
            warning = QtGui.QMessageBox()
            warning.setIcon(QtGui.QMessageBox.Critical)
            warning.setText("You need to load an image first first")
            warning.exec_()
        else:
            # New Image objects to be updated
            self.operations.new_image = Image.open(str(self.file))
            self.operations.new_image_pixels = self.operations.new_image.load()

            self.operations.turn_gray()
            
            # Updating the Image object with the new data
            self.operations.image = self.operations.new_image
            self.operations.image_pixels = self.operations.new_image_pixels
            new = ImageQt.ImageQt(self.operations.image)
            self._show_image(new, self.original)
            
            self.gray_flag = True

    def _quantization(self):

        if self.file == None or len(self.file) == 0:
            warning = QtGui.QMessageBox()
            warning.setIcon(QtGui.QMessageBox.Critical)
            warning.setText("You need to load an image first")
            warning.exec_()
        elif not self.gray_flag:
            warning = QtGui.QMessageBox()
            warning.setIcon(QtGui.QMessageBox.Critical)
            warning.setText("You need to have a grayscaled image for this operation")
            warning.exec_()
        else:

            # New Image objects to be updated
            self.operations.new_image = Image.open(str(self.file))
            self.operations.new_image_pixels = self.operations.new_image.load()

            input, ok = QtGui.QInputDialog.getInt(self.w, "Number of shades", "Enter the number of shades you want in this image: ", value = 256, min=1, max=256)
            
            if ok:
                self.operations.quantization(input)
                
                # Updating the Image object with the new data
                self.operations.image = self.operations.new_image
                self.operations.image_pixels = self.operations.new_image_pixels
                new = ImageQt.ImageQt(self.operations.image)
                self._show_image(new, self.original)
        
    def _rotate_clockwise(self):
        if self.file == None or len(self.file) == 0:
            warning = QtGui.QMessageBox()
            warning.setIcon(QtGui.QMessageBox.Critical)
            warning.setText("You need to load an image first")
            warning.exec_()
        else:
            # New Image objects to be updated
            self.operations.new_image = Image.open(str(self.file))
            self.operations.new_image_pixels = self.operations.new_image.load()

            self.operations.right_turn()
            
            # Updating the Image object with the new data
            self.operations.image = self.operations.new_image
            self.operations.image_pixels = self.operations.new_image_pixels
            new = ImageQt.ImageQt(self.operations.image)
            self._show_image(new, self.original)

    def _rotate_counter_clockwise(self):
        if self.file == None or len(self.file) == 0:
            warning = QtGui.QMessageBox()
            warning.setIcon(QtGui.QMessageBox.Critical)
            warning.setText("You need to load an image first")
            warning.exec_()
        else:
            # New Image objects to be updated
            self.operations.new_image = Image.open(str(self.file))
            self.operations.new_image_pixels = self.operations.new_image.load()

            self.operations.left_turn()
            
            # Updating the Image object with the new data
            self.operations.image = self.operations.new_image
            self.operations.image_pixels = self.operations.new_image_pixels
            new = ImageQt.ImageQt(self.operations.image)
            self._show_image(new, self.original)

    def _update_brightness(self):
    
        self.brightness_coefficient = self.slider.value()
        self.operations.adjust_brightness(self.brightness_coefficient)
        new = ImageQt.ImageQt(self.operations.new_image)
        self._show_image(new, self.original)

    def _set_brightness(self):
        self.slider.setParent(None)
        self.done_button.setParent(None)
        self.operations.image = self.operations.new_image
        self.operations.image_pixels = self.operations.new_image_pixels
        new = ImageQt.ImageQt(self.operations.image)
        self._show_image(new, self.original)

    def _adjust_brightness(self):
        if self.file == None or len(self.file) == 0:
            warning = QtGui.QMessageBox()
            warning.setIcon(QtGui.QMessageBox.Critical)
            warning.setText("You need to load an image first")
            warning.exec_()
        else:
            # New Image objects to be updated
            self.operations.new_image = Image.open(str(self.file))
            self.operations.new_image_pixels = self.operations.new_image.load()
                        
            self.slider = QtGui.QSlider(QtCore.Qt.Horizontal, self.w)            
            self.slider.move(50, self.display_image.size[1]+50)
            self.slider.setMinimumWidth(255)
            self.slider.show()
            self.slider.setMinimum(-255)
            self.slider.setMaximum(255)
            self.slider.setTickInterval(1)
            self.slider.valueChanged.connect(self._update_brightness)
 
            self.done_button = QtGui.QPushButton("Done", self.main)
            self.done_button.clicked.connect(self._set_brightness)
            self.done_button.move(310, self.display_image.size[1]+65)
            self.done_button.show()

    def _update_contrast(self):
        self.contrast_coefficient = self.slider.value()
        self.operations.adjust_contrast(self.contrast_coefficient)
        new = ImageQt.ImageQt(self.operations.new_image)
        self._show_image(new, self.original)

    def _set_contrast(self):
        self.slider.setParent(None)
        self.done_button.setParent(None)
        self.operations.image = self.operations.new_image
        self.operations.image_pixels = self.operations.new_image_pixels
        new = ImageQt.ImageQt(self.operations.image)
        self._show_image(new, self.original)

    def _adjust_contrast(self):
        if self.file == None or len(self.file) == 0:
            warning = QtGui.QMessageBox()
            warning.setIcon(QtGui.QMessageBox.Critical)
            warning.setText("You need to load an image first")
            warning.exec_()
        else:
            # New Image objects to be updated
            self.operations.new_image = Image.open(str(self.file))
            self.operations.new_image_pixels = self.operations.new_image.load()
                        
            self.slider = QtGui.QSlider(QtCore.Qt.Horizontal, self.w)            
            self.slider.move(50, self.display_image.size[1]+50)
            self.slider.setMinimumWidth(255)
            self.slider.show()
            self.slider.setMinimum(0)
            self.slider.setMaximum(255)
            self.slider.setTickInterval(1)
            self.slider.valueChanged.connect(self._update_contrast)
 
            self.done_button = QtGui.QPushButton("Done", self.main)
            self.done_button.clicked.connect(self._set_contrast)
            self.done_button.move(310, self.display_image.size[1]+65)
            self.done_button.show()

    def _negative(self):
        if self.file == None or len(self.file) == 0:
            warning = QtGui.QMessageBox()
            warning.setIcon(QtGui.QMessageBox.Critical)
            warning.setText("You need to load an image first")
            warning.exec_()
        else:
            # New Image objects to be updated
            self.operations.new_image = Image.open(str(self.file))
            self.operations.new_image_pixels = self.operations.new_image.load()

            self.operations.negative()
            
            # Updating the Image object with the new data
            self.operations.image = self.operations.new_image
            self.operations.image_pixels = self.operations.new_image_pixels
            new = ImageQt.ImageQt(self.operations.image)
            self._show_image(new, self.original)

    def _add_custom_filter(self):
        if self.file == None or len(self.file) == 0:
            warning = QtGui.QMessageBox()
            warning.setIcon(QtGui.QMessageBox.Critical)
            warning.setText("You need to load an image first")
            warning.exec_()
        else:
            # New Image objects to be updated
            self.operations.new_image = Image.open(str(self.file))
            self.operations.new_image_pixels = self.operations.new_image.load()
    
            new_filter = Kernel()
            new_filter.display_input()
            
            self.operations.convolution(new_filter.kernel)
            
            # Updating the Image object with the new data
            self.operations.image = self.operations.new_image
            self.operations.image_pixels = self.operations.new_image_pixels
            new = ImageQt.ImageQt(self.operations.image)
            self._show_image(new, self.original)

    def _histogram(self):
        if self.file == None or len(self.file) == 0:
            warning = QtGui.QMessageBox()
            warning.setIcon(QtGui.QMessageBox.Critical)
            warning.setText("You need to load an image first")
            warning.exec_()
        else:
            # New Image objects to be updated
            # self.operations.new_image = Image.open(str(self.file))
            # self.operations.new_image_pixels = self.operations.new_image.load()

            self.operations.make_histogram()
            self._show_histogram()
                    
    def _equalize_histogram(self):
        if self.file == None or len(self.file) == 0:
            warning = QtGui.QMessageBox()
            warning.setIcon(QtGui.QMessageBox.Critical)
            warning.setText("You need to load an image first")
            warning.exec_()
        else:
            # New Image objects to be updated
            self.operations.new_image = Image.open(str(self.file))
            self.operations.new_image_pixels = self.operations.new_image.load()

            self.operations.histogram_equalization(self.operations.histogram)
            
            # Updating the Image object with the new data
            self.operations.image = self.operations.new_image
            self.operations.image_pixels = self.operations.new_image_pixels
            new = ImageQt.ImageQt(self.operations.image)
            self._show_image(new, self.original)
            self.operations.make_histogram()
            self._show_histogram()

    def _show_histogram(self):
        teste = HistogramDisplay()
        teste.display_histogram(self.operations.normalized_histogram)
        
    def _zoom_in(self):
        if self.file == None or len(self.file) == 0:
            warning = QtGui.QMessageBox()
            warning.setIcon(QtGui.QMessageBox.Critical)
            warning.setText("You need to load an image first")
            warning.exec_()
        else:
            # New Image objects to be updated
            self.operations.new_image = Image.open(str(self.file))
            self.operations.new_image_pixels = self.operations.new_image.load()

            self.operations.zoom_in()
            
            # Updating the Image object with the new data
            self.operations.image = self.operations.new_image
            self.operations.image_pixels = self.operations.new_image_pixels
            new = ImageQt.ImageQt(self.operations.image)
            self._show_image(new, self.original)

    def _zoom_out(self):
        if self.file == None or len(self.file) == 0:
            warning = QtGui.QMessageBox()
            warning.setIcon(QtGui.QMessageBox.Critical)
            warning.setText("You need to load an image first")
            warning.exec_()
        else:
            # New Image objects to be updated
            self.operations.new_image = Image.open(str(self.file))
            self.operations.new_image_pixels = self.operations.new_image.load()

            self.operations.zoom_out()
            
            # Updating the Image object with the new data
            self.operations.image = self.operations.new_image
            self.operations.image_pixels = self.operations.new_image_pixels
            new = ImageQt.ImageQt(self.operations.image)
            self._show_image(new, self.original)

    def _gaussian_filter(self):
        if self.file == None or len(self.file) == 0:
            warning = QtGui.QMessageBox()
            warning.setIcon(QtGui.QMessageBox.Critical)
            warning.setText("You need to load an image first")
            warning.exec_()
        else:
            # New Image objects to be updated
            self.operations.new_image = Image.open(str(self.file))
            self.operations.new_image_pixels = self.operations.new_image.load()
                
            self.operations.convolution([[0.0625, 0.125, 0.0625], [0.125, 0.25, 0.125], [0.0625, 0.125, 0.0625]])
            
            # Updating the Image object with the new data
            self.operations.image = self.operations.new_image
            self.operations.image_pixels = self.operations.new_image_pixels
            new = ImageQt.ImageQt(self.operations.image)
            self._show_image(new, self.original)

    def _laplacian_filter(self):
        if self.file == None or len(self.file) == 0:
            warning = QtGui.QMessageBox()
            warning.setIcon(QtGui.QMessageBox.Critical)
            warning.setText("You need to load an image first")
            warning.exec_()
        else:
            # New Image objects to be updated
            self.operations.new_image = Image.open(str(self.file))
            self.operations.new_image_pixels = self.operations.new_image.load()
                
            self.operations.convolution([[0, -1, 0], [-1, 4, -1], [0, -1, 0]])
            
            # Updating the Image object with the new data
            self.operations.image = self.operations.new_image
            self.operations.image_pixels = self.operations.new_image_pixels
            new = ImageQt.ImageQt(self.operations.image)
            self._show_image(new, self.original)

    def _generic_highpass_filter(self):
        if self.file == None or len(self.file) == 0:
            warning = QtGui.QMessageBox()
            warning.setIcon(QtGui.QMessageBox.Critical)
            warning.setText("You need to load an image first")
            warning.exec_()
        else:
            # New Image objects to be updated
            self.operations.new_image = Image.open(str(self.file))
            self.operations.new_image_pixels = self.operations.new_image.load()
                
            self.operations.convolution([[-1, -1, -1], [-1, 8, -1], [-1, -1, -1]])
            
            # Updating the Image object with the new data
            self.operations.image = self.operations.new_image
            self.operations.image_pixels = self.operations.new_image_pixels
            new = ImageQt.ImageQt(self.operations.image)
            self._show_image(new, self.original)

    def _prewitt_hx_filter(self):
        if self.file == None or len(self.file) == 0:
            warning = QtGui.QMessageBox()
            warning.setIcon(QtGui.QMessageBox.Critical)
            warning.setText("You need to load an image first")
            warning.exec_()
        else:
            # New Image objects to be updated
            self.operations.new_image = Image.open(str(self.file))
            self.operations.new_image_pixels = self.operations.new_image.load()
                
            self.operations.convolution([[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]])
            
            # Updating the Image object with the new data
            self.operations.image = self.operations.new_image
            self.operations.image_pixels = self.operations.new_image_pixels
            new = ImageQt.ImageQt(self.operations.image)
            self._show_image(new, self.original)

    def _prewitt_hy_filter(self):
        if self.file == None or len(self.file) == 0:
            warning = QtGui.QMessageBox()
            warning.setIcon(QtGui.QMessageBox.Critical)
            warning.setText("You need to load an image first")
            warning.exec_()
        else:
            # New Image objects to be updated
            self.operations.new_image = Image.open(str(self.file))
            self.operations.new_image_pixels = self.operations.new_image.load()
                
            self.operations.convolution([[-1, -1, -1], [0, 0, 0], [1, 1, 1]])
            
            # Updating the Image object with the new data
            self.operations.image = self.operations.new_image
            self.operations.image_pixels = self.operations.new_image_pixels
            new = ImageQt.ImageQt(self.operations.image)
            self._show_image(new, self.original)

    def _sobel_hx_filter(self):
        if self.file == None or len(self.file) == 0:
            warning = QtGui.QMessageBox()
            warning.setIcon(QtGui.QMessageBox.Critical)
            warning.setText("You need to load an image first")
            warning.exec_()
        else:
            # New Image objects to be updated
            self.operations.new_image = Image.open(str(self.file))
            self.operations.new_image_pixels = self.operations.new_image.load()
                
            self.operations.convolution([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])
            
            # Updating the Image object with the new data
            self.operations.image = self.operations.new_image
            self.operations.image_pixels = self.operations.new_image_pixels
            new = ImageQt.ImageQt(self.operations.image)
            self._show_image(new, self.original)

    def _sobel_hy_filter(self):
        if self.file == None or len(self.file) == 0:
            warning = QtGui.QMessageBox()
            warning.setIcon(QtGui.QMessageBox.Critical)
            warning.setText("You need to load an image first")
            warning.exec_()
        else:
            # New Image objects to be updated
            self.operations.new_image = Image.open(str(self.file))
            self.operations.new_image_pixels = self.operations.new_image.load()
                
            self.operations.convolution([[-1, -2, -1], [0, 0, 0], [1, 2, 1]])
            
            # Updating the Image object with the new data
            self.operations.image = self.operations.new_image
            self.operations.image_pixels = self.operations.new_image_pixels
            new = ImageQt.ImageQt(self.operations.image)
            self._show_image(new, self.original)

# class NewWindow:
        # def __init__(self):
        # self.w = QtGui.QDialog()

class HistogramDisplay:
    
    def __init__(self):
        self.w = QtGui.QDialog()
        self.w.resize(256, 256)
        self.w.setWindowTitle("Image histogram")

    def display_histogram(self, histogram):
        actual_label = QtGui.QLabel(self.w)
        label = QtGui.QPixmap(256, 256)
        label.fill()
        histogram_display = QtGui.QPainter(label)
        
        histogram_display.setPen(QtCore.Qt.black)
        
        for i in range(256):
            histogram_display.drawLine(i, 255, i, 256-histogram[i])
            
        actual_label.setPixmap(label)
        histogram_display.end()
        
        actual_label.show()
        self.w.exec_()

class Kernel:

    def __init__(self):
        self.w = QtGui.QDialog()
        self.w.resize(150, 180)
        self.w.setWindowTitle(" ")
        self.kernel = [[None, None, None], [None, None, None], [None, None, None]]
        self.inputs = [[None, None, None], [None, None, None], [None, None, None]]
        
    def display_input(self):
    
        for i in range(3):
            for n in range(3):
                self.inputs[i][n] = QtGui.QLineEdit(self.w)
                self.inputs[i][n].setValidator(QtGui.QIntValidator())
                self.inputs[i][n].move(50*i+10, 30*n+50)
                self.inputs[i][n].setMaximumWidth(30)
            
        label = QtGui.QLabel(self.w)
        label.setText("Set your kernel values:")
        label.move(22, 20)
        
        set_button = QtGui.QPushButton("Set filter", self.w)
        set_button.clicked.connect(self._set_kernel)
        set_button.move(38, 150)
                
        self.w.exec_()

    def _set_kernel(self):
        
        for i in range(3):
            for n in range(3):
                self.kernel[i][n] = int(self.inputs[i][n].text())

        self.w.accept()
        
class Slider:
    def __init__(self):
        pass
    def display_input(self, min_value, max_value):
        self.slider = QtGui.QSlider(QtCore.Qt.Horizontal, self.w)
        self.slider.move(30, 10)
        self.slider.setMinimum(min_value)
        self.slider.setMaximum(max_value)
        self.slider.setTickInterval(1)
        self.slider.valueChanged.connect(self._set_coefficient)
        self.w.exec_()
        
    def _set_coefficient(self):
        self.coefficient = self.slider.value()