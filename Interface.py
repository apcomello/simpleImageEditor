from PyQt4 import QtGui
from PIL import Image, ImageQt
import Editor
import sys

class MainWindow:

    def __init__(self):
        self.main = QtGui.QMainWindow()
        self.w = QtGui.QWidget()
        self.main.setCentralWidget(self.w)
        self.b = QtGui.QLabel(self.w)
        self.original = None
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
        self.original_label.setText("Original image")
        self.modified_label.setText("Modified image")


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
        
        add_filter_action = QtGui.QAction("Add filter", menu)
        add_filter_action.triggered.connect(self._add_filter)
        
        negative_action = QtGui.QAction("Negative", menu)
        negative_action.triggered.connect(self._negative)
        
        grayscale_action = QtGui.QAction("Grayscale", menu)
        grayscale_action.triggered.connect(self._grayscale)
        
        quantization_action = QtGui.QAction("Quantization", menu)
        quantization_action.triggered.connect(self._quantization)
        
        transformations = menu.addMenu("Transformations")
        transformations.addAction(add_filter_action)
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
        
        # Creation and positioning of all the button needed
        # self.button_open = QtGui.QPushButton("Open image", self.w)
        # self.button_open.clicked.connect(self.load_file)
        # self.button_open.move(10, self.middle_y -75)       
        
        # self.button_horizontal = QtGui.QPushButton("Horizontal flip", self.w)
        # self.button_horizontal.clicked.connect(self.display_horizontal_turn)
        # self.button_horizontal.move(10, self.middle_y -45)
        
        # self.button_vertical = QtGui.QPushButton("Vertical flip", self.w)
        # self.button_vertical.clicked.connect(self.display_vertical_turn)
        # self.button_vertical.move(10, self.middle_y -15)
        
        # self.button_gray = QtGui.QPushButton("Grayscale", self.w)
        # self.button_gray.clicked.connect(self.display_grayed_image)
        # self.button_gray.move(10, self.middle_y + 15)
        
        # self.button_quantization = QtGui.QPushButton("Quantization", self.w)
        # self.button_quantization.clicked.connect(self.display_quantized_image)
        # self.button_quantization.move(10, self.middle_y + 45)
                
        # self.button_save = QtGui.QPushButton("Save image", self.w)
        # self.button_save.clicked.connect(self.save_file)
        # self.button_save.move(10, self.middle_y + 75)

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
          
            self._show_image(self.qim, self.original)
            
            
            # # Updates the buttons location to keep them "in the middle"
            # self.button_open.move(10, self.middle_y -75)       
            # self.button_horizontal.move(10, self.middle_y -45)
            # self.button_vertical.move(10, self.middle_y -15)
            # self.button_gray.move(10, self.middle_y + 15)
            # self.button_quantization.move(10, self.middle_y + 45)
            # self.button_save.move(10, self.middle_y + 75)
            # self.info_label.move (2*self.operations.image.size[0]+30, self.operations.image.size[1]+40)
        # self.operations.make_histogram()
        # print self.operations.histogram
        

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
    
        self.pixmap_original =  QtGui.QPixmap.fromImage(original)
        self.pixmap_original.detach()

        self.pixmap_image = QtGui.QPixmap.fromImage(image)
        self.pixmap_image.detach()
        self.label_image.clear()

        self.label_original.setPixmap(self.pixmap_original)
        self.label_original.move(30, 30)
        self.label_original.resize(self.operations.image.size[0], self.operations.image.size[1])
        self.label_original.show()
        
        self.original_label.move(30, 10)
        self.original_label.show()
        
        self.modified_label.move(self.operations.image.size[0] + 60, 10)
        self.modified_label.show()

        self.label_image.clear()
        self.label_image.resize(self.operations.new_image.size[0], self.operations.new_image.size[1])
        self.label_image.move(self.operations.image.size[0] + 60, 30)
        
        self.label_image.setPixmap(self.pixmap_image)
        self.label_image.show()
        
        self.main.resize(2*self.operations.image.size[0]+90, self.operations.image.size[1]+80)
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

            self.operations.horizontal_turn()
            
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
            
            self.operations.vertical_turn()

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

            self.operations.adjust_brightness()
            
            # Updating the Image object with the new data
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

            self.operations.adjust_contrast()
            
            # Updating the Image object with the new data
            self.operations.image = self.operations.new_image
            self.operations.image_pixels = self.operations.new_image_pixels
            new = ImageQt.ImageQt(self.operations.image)
            self._show_image(new, self.original)

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

    def _add_filter(self):
        if self.file == None or len(self.file) == 0:
            warning = QtGui.QMessageBox()
            warning.setIcon(QtGui.QMessageBox.Critical)
            warning.setText("You need to load an image first")
            warning.exec_()
        else:
            # New Image objects to be updated
            self.operations.new_image = Image.open(str(self.file))
            self.operations.new_image_pixels = self.operations.new_image.load()

            self.operations.convolution()
            
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
            self.operations.new_image = Image.open(str(self.file))
            self.operations.new_image_pixels = self.operations.new_image.load()

            self.operations.make_histogram()
            
            # Updating the Image object with the new data
            self.operations.image = self.operations.new_image
            self.operations.image_pixels = self.operations.new_image_pixels
            new = ImageQt.ImageQt(self.operations.image)
            self._show_image(new, self.original)

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

    
class ImageDisplay:
    
    def __init__(self):
        self.w = QtGui.QDialog()
        self.b = QtGui.QLabel(self.w)
    
    def display_image(self):
        label = QtGui.QLabel(self.w)
        label.setText("Hello, world")
        # pixmap = QtGui.QPixmap.fromImage(image)
        # pixmap.detach()
        # label.setPixmap(pixmap)
        # self.w.resize(pixmap.width(), pixmap.height())
        self.w.resize(100, 100)
        self.w.exec_()
