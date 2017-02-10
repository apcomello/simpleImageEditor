#!/usr/bin/env python
# -*- coding: utf-8 -*-

#===============================================
# Author: Ana Paula Mello       apcomello@gmail.com
# Date: September 2016
# Project for INF1046 - Fundamentos de Processamento de Imagens
# UFRGS - Departamento de Informática
# Version 1.2
#===============================================

__author__ = "Ana Paula Mello"
__email__ = "apcomello@gmail.com"
__version__ = "1.2"

from PyQt4 import QtGui, QtCore
from PIL import Image, ImageQt
import Editor

class MainWindow:

    def __init__(self):
        # Interface
        self.main = QtGui.QMainWindow()
        self.main_widget = QtGui.QWidget()
        self.main.setCentralWidget(self.main_widget)
        self.middle_y = 225
        self.pixmap_image = None
        self.pixmap_original = None
        self.previous_image = None
        self.label_original = QtGui.QLabel(self.main_widget)
        self.label_image = QtGui.QLabel(self.main_widget)
        self.original_label = QtGui.QLabel(self.main_widget)
        self.modified_label = QtGui.QLabel(self.main_widget)

        # Image
        self.original = None
        self.display_image = None       # Copy to be used in the display
        self.image = None
        self.pixel= None
        self.new_pixel = None
        self.image_copy = None      # Copy to be modified
        self.operations = Editor.Editor(self.image, self.image_copy, self.pixel, self.new_pixel)
        
        self.file = None
        self.gray_flag = False

    def create_main_window(self):
        '''
            Creates the basic layout of the interface
        '''
        
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
        
        self.info_label = QtGui.QLabel(self.main_widget)
        self.info_label.setText("Ana Paula Mello - 260723")
        self.info_label.move (360, 470)
      
        self.main.setFixedSize(500, 510)
        self.main.move(100, 100)
        self.main.setWindowTitle("Image Operations")
        self.main.show()
            
    def load_file(self):
    
        self.file = QtGui.QFileDialog.getOpenFileName(self.main_widget, "Open file", filter="jpg (*.jpg *.)")
        
        if len(self.file) != 0:     # Doesn't do anything if no file was selected
       
            # Loads the image into the Editor
            self.operations.original_image = Image.open(str(self.file))
            self.operations.new_image = Image.open(str(self.file))
            self.operations.original_image_pixels = self.operations.original_image.load()
            self.operations.new_image_pixels = self.operations.new_image.load()
                            
            # Turns the PIL object into a PyQt object in order to display it
            self.qim = ImageQt.ImageQt(self.operations.original_image)
            self.original = ImageQt.ImageQt(self.operations.original_image)
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
            self.file = QtGui.QFileDialog.getSaveFileName(self.main_widget, "Save file", "image.jpg", filter="jpg (*.jpg *.)")
            self.operations.original_image.save(str(self.file))
        
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
        
        if self.operations.new_image.size[0]+self.display_image.size[0]+90 >= 1000 and self.operations.new_image.size[1]+100 >= 900:
            scroll = QtGui.QScrollArea(self.main_widget)
            scroll.move(self.display_image.size[0] + 60, 30)
            scroll.setWidget(self.label_image)
            scroll.show()
            self.main.setFixedSize(900, 400)
            self.info_label.move(760, 350)
        elif self.display_image.size[1] > self.operations.new_image.size[1]:
            self.main.setFixedSize(self.operations.new_image.size[0]+self.display_image.size[0]+90, self.display_image.size[1]+100)
            self.info_label.move(self.operations.new_image.size[0]+self.display_image.size[0]-50, self.display_image.size[1] + 50)
        else:
            self.main.setFixedSize(self.operations.new_image.size[0]+self.display_image.size[0]+90, self.operations.new_image.size[1]+100)
            self.info_label.move(self.operations.new_image.size[0]+self.display_image.size[0]-50, self.operations.new_image.size[1]+50)

        self.info_label.show()
        self.main.show()
        
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
            self.operations.original_image = self.operations.new_image
            self.operations.original_image_pixels = self.operations.new_image_pixels
            new = ImageQt.ImageQt(self.operations.original_image)
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
            self.operations.original_image = self.operations.new_image
            self.operations.original_image_pixels = self.operations.new_image_pixels
            new = ImageQt.ImageQt(self.operations.original_image)
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
            self.operations.original_image = self.operations.new_image
            self.operations.original_image_pixels = self.operations.new_image_pixels
            new = ImageQt.ImageQt(self.operations.original_image)
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

            input, ok = QtGui.QInputDialog.getInt(self.main_widget, "Number of shades", "Enter the number of shades you want in this image: ", value = 256, min=1, max=256)
            
            if ok:
                self.operations.quantization(input)
                
                # Updating the Image object with the new data
                self.operations.original_image = self.operations.new_image
                self.operations.original_image_pixels = self.operations.new_image_pixels
                new = ImageQt.ImageQt(self.operations.original_image)
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
            self.operations.original_image = self.operations.new_image
            self.operations.original_image_pixels = self.operations.new_image_pixels
            new = ImageQt.ImageQt(self.operations.original_image)
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
            self.operations.original_image = self.operations.new_image
            self.operations.original_image_pixels = self.operations.new_image_pixels
            new = ImageQt.ImageQt(self.operations.original_image)
            self._show_image(new, self.original)

    def _update_brightness(self):
        
        # Uses the value from the slider to apply the transformations
        self.brightness_coefficient = self.slider.value()
        self.operations.adjust_brightness(self.brightness_coefficient)
        new = ImageQt.ImageQt(self.operations.new_image)
        self._show_image(new, self.original)

    def _set_brightness(self):
    
        # Sets a permanent value for the image
        self.slider.setParent(None)
        self.done_button.setParent(None)
        self.operations.original_image = self.operations.new_image
        self.operations.original_image_pixels = self.operations.new_image_pixels
        new = ImageQt.ImageQt(self.operations.original_image)
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
                        
            self.slider = QtGui.QSlider(QtCore.Qt.Horizontal, self.main_widget)            
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
    
        # Uses the value from the slider to apply the transformations
        self.contrast_coefficient = self.slider.value()
        self.operations.adjust_contrast(self.contrast_coefficient)
        new = ImageQt.ImageQt(self.operations.new_image)
        self._show_image(new, self.original)

    def _set_contrast(self):
    
        # Sets a permanent value for the image
        self.slider.setParent(None)
        self.done_button.setParent(None)
        self.operations.original_image = self.operations.new_image
        self.operations.original_image_pixels = self.operations.new_image_pixels
        new = ImageQt.ImageQt(self.operations.original_image)
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
                        
            self.slider = QtGui.QSlider(QtCore.Qt.Horizontal, self.main_widget)            
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
            self.operations.original_image = self.operations.new_image
            self.operations.original_image_pixels = self.operations.new_image_pixels
            new = ImageQt.ImageQt(self.operations.original_image)
            self._show_image(new, self.original)

    def _histogram(self):
        
        if self.file == None or len(self.file) == 0:
            warning = QtGui.QMessageBox()
            warning.setIcon(QtGui.QMessageBox.Critical)
            warning.setText("You need to load an image first")
            warning.exec_()
        else:
            # New Image objects to be updated
            self.operations.new_image = Image.open(str(self.file))
            self.operations.new_image_pixels = self.operations.new_image.load()
            current = self.operations.make_histogram()
            self._show_histogram(current)
                    
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
            previous_histogram =  self.operations.make_histogram()

            self.operations.histogram_equalization(self.operations.histogram)
            
            # Updating the Image object with the new data
            self.operations.original_image = self.operations.new_image
            self.operations.original_image_pixels = self.operations.new_image_pixels
            new = ImageQt.ImageQt(self.operations.original_image)
            self._show_image(new, self.original)
            current_histogram = self.operations.make_histogram()
            self._show_histogram(previous_histogram, current_histogram)

    def _show_histogram(self, histogram, new_histogram=None):
        teste = HistogramDisplay()
        teste.display_histogram(histogram, new_histogram)
        
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
            self.operations.original_image = self.operations.new_image
            self.operations.original_image_pixels = self.operations.new_image_pixels
            new = ImageQt.ImageQt(self.operations.original_image)
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
            
            factors = ZoomFactor()
            factors.display_input()

            if factors.zoom_factors[0] == None:     # If no value was inputed
                pass
            elif factors.zoom_factors[0] <= 0 or factors.zoom_factors[1] <= 0:
                warning = QtGui.QMessageBox()
                warning.setIcon(QtGui.QMessageBox.Critical)
                warning.setText("Your factors need to be bigger than 0")
                warning.exec_()
            else:
                self.operations.zoom_out(factors.zoom_factors[0], factors.zoom_factors[1])
                # Updating the Image object with the new data
                self.operations.original_image = self.operations.new_image
                self.operations.original_image_pixels = self.operations.new_image_pixels
                new = ImageQt.ImageQt(self.operations.original_image)
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
            self.operations.turn_gray()
            new_filter = Kernel()
            new_filter.display_input()
            
            if new_filter.kernel[0][0] == None:     # If no input was added
                pass
            else:
                self.operations.convolution(new_filter.kernel)
                
                # Updating the Image object with the new data
                self.operations.original_image = self.operations.new_image
                self.operations.original_image_pixels = self.operations.new_image_pixels
                new = ImageQt.ImageQt(self.operations.original_image)
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
            self.operations.original_image = self.operations.new_image
            self.operations.original_image_pixels = self.operations.new_image_pixels
            new = ImageQt.ImageQt(self.operations.original_image)
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
            self.operations.original_image = self.operations.new_image
            self.operations.original_image_pixels = self.operations.new_image_pixels
            new = ImageQt.ImageQt(self.operations.original_image)
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
            self.operations.original_image = self.operations.new_image
            self.operations.original_image_pixels = self.operations.new_image_pixels
            new = ImageQt.ImageQt(self.operations.original_image)
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
            self.operations.original_image = self.operations.new_image
            self.operations.original_image_pixels = self.operations.new_image_pixels
            new = ImageQt.ImageQt(self.operations.original_image)
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
            self.operations.original_image = self.operations.new_image
            self.operations.original_image_pixels = self.operations.new_image_pixels
            new = ImageQt.ImageQt(self.operations.original_image)
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
            self.operations.original_image = self.operations.new_image
            self.operations.original_image_pixels = self.operations.new_image_pixels
            new = ImageQt.ImageQt(self.operations.original_image)
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
            self.operations.original_image = self.operations.new_image
            self.operations.original_image_pixels = self.operations.new_image_pixels
            new = ImageQt.ImageQt(self.operations.original_image)
            self._show_image(new, self.original)

class HistogramDisplay:
    
    '''
        Opens a new window and creates histograms from the given info
    '''
    def __init__(self):
        self.main_widget = QtGui.QDialog()
        self.main_widget.resize(256, 256)
        self.main_widget.setWindowTitle("Image histogram")

    def display_histogram(self, histogram, equalized_histogram=None):
    
        if equalized_histogram == None:     # Only one histogram to be displayed
            current_histogram = QtGui.QLabel(self.main_widget)
            current_histogram_pixmap = QtGui.QPixmap(256, 256)
            current_histogram_pixmap.fill()
            histogram_display = QtGui.QPainter(current_histogram_pixmap)
            
            histogram_display.setPen(QtCore.Qt.black)
            
            # Draws the histogram
            for i in range(256):
                histogram_display.drawLine(i, 255, i, 256-histogram[i])
                
            current_histogram.setPixmap(current_histogram_pixmap)
            histogram_display.end()
            
            current_histogram.show()
            self.main_widget.exec_()
            
        else:       # Two histograms to be displayes
            self.main_widget.resize(532, 276)
            
            current_histogram_label = QtGui.QLabel(self.main_widget)
            previous_histogram_label = QtGui.QLabel(self.main_widget)
            
            current_histogram_label.setText("Equalized histogram")
            previous_histogram_label.setText("Original histogram")
            
            current_histogram_label.move(286, 260)
            previous_histogram_label.move(10, 260)
            current_histogram_label.show()
            previous_histogram_label.show()
            
            current_histogram = QtGui.QLabel(self.main_widget)
            current_histogram_pixmap = QtGui.QPixmap(256, 256)
            current_histogram_pixmap.fill()
            current_histogram_display = QtGui.QPainter(current_histogram_pixmap)
            
            current_histogram_display.setPen(QtCore.Qt.black)
            
            # Draws the histogram
            for i in range(256):
                current_histogram_display.drawLine(i, 255, i, 256-histogram[i])
                
            current_histogram.setPixmap(current_histogram_pixmap)
            current_histogram_display.end()
            
            new_histogram = QtGui.QLabel(self.main_widget)
            new_histogram_pixmap = QtGui.QPixmap(256, 256)
            new_histogram_pixmap.fill()
            new_histogram_display = QtGui.QPainter(new_histogram_pixmap)
            
            new_histogram_display.setPen(QtCore.Qt.black)
            
            # Draws the histogram
            for i in range(256):
                new_histogram_display.drawLine(i, 255, i, 256-equalized_histogram[i])
                
            new_histogram.setPixmap(new_histogram_pixmap)
            new_histogram_display.end()
            
            new_histogram.move(276, 0)
            current_histogram.show()
            new_histogram.show()
            self.main_widget.exec_()

class Kernel:

    '''
        Opens a window to get the input to set a new kernel  to use in the convolution operation
    '''
    def __init__(self):
        self.main_widget = QtGui.QDialog()
        self.main_widget.resize(150, 180)
        self.main_widget.setWindowTitle(" ")
        self.kernel = [[None, None, None], [None, None, None], [None, None, None]]
        self.inputs = [[None, None, None], [None, None, None], [None, None, None]]
        
    def display_input(self):
    
        # Creates input forms
        for i in range(3):
            for n in range(3):
                self.inputs[i][n] = QtGui.QLineEdit(self.main_widget)
                self.inputs[i][n].setValidator(QtGui.QDoubleValidator(-0.001, 99.999, 3))
                self.inputs[i][n].move(50*i+10, 30*n+50)
                self.inputs[i][n].setMaximumWidth(30)
            
        label = QtGui.QLabel(self.main_widget)
        label.setText("Set your kernel values:")
        label.move(22, 20)
        
        set_button = QtGui.QPushButton("Set filter", self.main_widget)
        set_button.clicked.connect(self._set_kernel)
        set_button.move(38, 150)
                
        self.main_widget.exec_()

    def _set_kernel(self):
        
        for i in range(3):
            for n in range(3):
                if len(self.inputs[i][n].text()) == 0: # No input was added
                    self.kernel[i][n] = 0.
                else:
                    self.kernel[i][n] = float(self.inputs[i][n].text())

        self.main_widget.accept()
        
class ZoomFactor:
    
    '''
        Opens a window to get the input to set the zoom out factors
    '''

    def __init__(self):
        self.main_widget = QtGui.QDialog()
        self.main_widget.resize(150, 120)
        self.main_widget.setWindowTitle(" ")
        self.zoom_factors = [None, None]
        self.inputs = [None, None]
        
    def display_input(self):
    
        # Creates input forms
        for i in range(2):
                self.inputs[i] = QtGui.QLineEdit(self.main_widget)
                self.inputs[i].setValidator(QtGui.QIntValidator(1, 100))
                self.inputs[i].setMaximumWidth(30)
                self.inputs[i].move(10, 30*i+10)
            
        horizontal_label = QtGui.QLabel(self.main_widget)
        horizontal_label.move(50, 10)
        horizontal_label.setText("Horizontal factor")
        horizontal_label.show()
        
        vertical_label = QtGui.QLabel(self.main_widget)
        vertical_label.move(50, 40)
        vertical_label.setText("Vertical factor")
        vertical_label.show()

        
        set_button = QtGui.QPushButton("Set zoom factors", self.main_widget)
        set_button.clicked.connect(self._set_factors)
        set_button.move(10, 90)
                
        self.main_widget.exec_()

    def _set_factors(self):
        for n in range(2):
            self.zoom_factors[n] = int(self.inputs[n].text())
        self.main_widget.accept()
