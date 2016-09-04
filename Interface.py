from PyQt4 import QtGui
from PIL import Image, ImageQt
import Editor

class MainWindow:

    def __init__(self):
        self.w = QtGui.QWidget()
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

    def create_main_window(self):
        
        # Creation and positioning of all the button needed
        self.button_open = QtGui.QPushButton("Open image", self.w)
        self.button_open.clicked.connect(self.load_file)
        self.button_open.move(10, self.middle_y -75)       
        
        self.button_horizontal = QtGui.QPushButton("Horizontal flip", self.w)
        self.button_horizontal.clicked.connect(self.display_horizontal_turn)
        self.button_horizontal.move(10, self.middle_y -45)
        
        self.button_vertical = QtGui.QPushButton("Vertical flip", self.w)
        self.button_vertical.clicked.connect(self.display_vertical_turn)
        self.button_vertical.move(10, self.middle_y -15)
        
        self.button_gray = QtGui.QPushButton("Grayscale", self.w)
        self.button_gray.clicked.connect(self.display_grayed_image)
        self.button_gray.move(10, self.middle_y + 15)
        
        self.button_quantization = QtGui.QPushButton("Quantization", self.w)
        self.button_quantization.clicked.connect(self.display_quantized_image)
        self.button_quantization.move(10, self.middle_y + 45)
                
        self.button_save = QtGui.QPushButton("Save image", self.w)
        self.button_save.clicked.connect(self.save_file)
        self.button_save.move(10, self.middle_y + 75)

        self.info_label = QtGui.QLabel(self.w)
        self.info_label.setText("Ana Paula Mello - 260723")
        self.info_label.move (370, 480)
      
        self.w.resize(500, 500)
        self.w.move(100, 100)
        self.w.setWindowTitle("Image Operations")
        self.w.show()
            
    def load_file(self):
    
        self.file = QtGui.QFileDialog.getOpenFileName(self.w, "Open file")
        
        if len(self.file) != 0:
       
            self.operations.image = Image.open(str(self.file))
            self.operations.image_pixels = self.operations.image.load()
                            
            self.qim = ImageQt.ImageQt(self.operations.image)
            self.original = ImageQt.ImageQt(self.operations.image)
          
            self.show_image(self.qim, self.original)
            
            self.middle_y = ((self.operations.image.size[1] + 60) / 2) - 25
            
            # Updates the buttons location to keep them "in the middle"
            self.button_open.move(10, self.middle_y -75)       
            self.button_horizontal.move(10, self.middle_y -45)
            self.button_vertical.move(10, self.middle_y -15)
            self.button_gray.move(10, self.middle_y + 15)
            self.button_quantization.move(10, self.middle_y + 45)
            self.button_save.move(10, self.middle_y + 75)
            self.info_label.move (2*self.operations.image.size[0]+30, self.operations.image.size[1]+40)
        self.operations.make_histogram()
        print self.operations.histogram
        
    def save_file(self):
        if self.file == None or len(self.file) == 0:
            warning = QtGui.QMessageBox()
            warning.setIcon(QtGui.QMessageBox.Critical)
            warning.setText("You need to load an image first")
            warning.exec_()
        else:
            self.file = QtGui.QFileDialog.getSaveFileName(self.w, "Save file", "image.jpg", filter="jpg (*.jpg *.)")
            self.operations.image.save(str(self.file))
        
    def show_image(self, image, original):
    
        if self.previous_image != None:
            previous = ImageQt.ImageQt(self.previous_image)
            clean_up_label = QtGui.QLabel(self.w)

            clean_up_original = QtGui.QPixmap().fromImage(previous)
            clean_up_original.detach()
            clean_up_original.fill(QtGui.QColor(240, 240, 240))
            
            clean_up_label.setPixmap(clean_up_original)
            clean_up_label.move(100, 30)
            clean_up_label.show()
            
            clean_up_label_changed = QtGui.QLabel(self.w)

            clean_up_image = QtGui.QPixmap().fromImage(previous)
            clean_up_image.detach()
            clean_up_image.fill(QtGui.QColor(240, 240, 240))
            
            clean_up_label_changed.setPixmap(clean_up_image)
            clean_up_label_changed.move(self.previous_image.size[0] + 130, 30)
            clean_up_label_changed.show()


        self.previous_image = self.operations.image
        self.pixmap_original =  QtGui.QPixmap().fromImage(original)
        self.pixmap_original.detach()

        self.pixmap_image = QtGui.QPixmap.fromImage(image)
        self.pixmap_image.detach()

    
        label_original = QtGui.QLabel(self.w)
        label_original.setPixmap(self.pixmap_original)
        label_original.move(100, 30)
        label_original.show()
        

        label_image = QtGui.QLabel(self.w)
        label_image.clear()
        
        self.original_label = QtGui.QLabel(self.w)
        self.original_label.setText("Original image")
        self.original_label.move(130, 10)
        self.original_label.show()
        
        self.modified_label = QtGui.QLabel(self.w)
        self.modified_label.setText("Modified image")
        self.modified_label.move(self.operations.image.size[0] + 160, 10)
        self.modified_label.show()

        
        label_image.move(self.operations.image.size[0] + 130, 30)
        
        label_image.setPixmap(self.pixmap_image)
        label_image.show()
        
        self.w.resize(2*self.operations.image.size[0]+160, self.operations.image.size[1]+60)
        self.w.show()
        
    def display_horizontal_turn(self):
    
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
            self.show_image(new, self.original)
        
    def display_vertical_turn(self):
    
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
            self.show_image(new, self.original)

    def display_grayed_image(self):
    
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
            self.show_image(new, self.original)
            
            self.gray_flag = True

    def display_quantized_image(self):

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
                self.show_image(new, self.original)
        
