from PyQt4 import QtGui
from PIL import Image, ImageQt
import sys
from math import floor

## TODO
    # Error messages
        # 0 in quantization X
        # Attempting to quantize a colored image 
        # No performing operations while no image loaded X
    # Bigger images overflow
    

class Editor:

    def __init__(self, image, new_image, image_pixels, new_image_pixels):
        self.image = image
        self.image_pixels = image_pixels
        self.new_image = new_image
        self.new_image_pixels = new_image_pixels
    
    def horizontal_turn(self):
        for i in range (0, self.image.size[0]):
            for n in range (0, self.image.size[1]):
                x = abs(self.image.size[0] -1 - i)          # New x coordinate
                self.new_image_pixels[x,n] = self.image_pixels[i, n]
        
    def vertical_turn(self):
        for i in range (0, self.image.size[0]):
            for n in range (0, self.image.size[1]):
                y = abs(self.image.size[1] -1 - n)          # New y coordinate
                self.new_image_pixels[i,y] = self.image_pixels[i, n]
                
    def turn_gray(self):
        for i in range (0, self.image.size[0]):
            for n in range (0, self.image.size[1]):
                
                # Calculates the proportion of Red, Green and Blue needed in the grayScale shade
                R = self.image_pixels[i, n][0]
                G = self.image_pixels[i, n][1]
                B = self.image_pixels[i, n][2]
                grayScale = int(0.299*R + 0.587*G + 0.114*B)
                self.new_image_pixels[i, n] = (grayScale, grayScale, grayScale)

    def quantization(self, num_levels):
        start = 0
        shades = []
        range_shades = 256/num_levels 
        
        # Gets all the shades to be used
        for i in range(0, 256, range_shades):
            tone = (start + i)/2
            shades.append(tone)
            start = i+1
        
        for i in range (0, self.image.size[0]):
            for n in range (0, self.image.size[1]):
                new_shade = (self.image_pixels[i, n][0]) / range_shades         # Gets the index to locate the appropriate shade of the pixel
                self.new_image_pixels[i, n] = (shades[new_shade], shades[new_shade], shades[new_shade])
                    
    def make_histogram(self):
        self.histogram = [0] * 256
        biggest_column = 0
        
        for i in range (0, self.image.size[0]):
            for n in range (0, self.image.size[1]):
                shade = self.image_pixels[i, n][0]
                self.histogram[shade] += 1

        for i in range(0, 255):
            if self.histogram[i] > biggest_column:
                biggest_column = self.histogram[i]

        for i in range(0, 255):
            self.histogram[i] = int(round(float(self.histogram[i]) / biggest_column * 255))

    def adjust_brightness(self, adjustment_coeficient):
        
        for i in range (0, self.image.size[0]):
            for n in range (0, self.image.size[1]):
                R = self.image_pixels[i,n][0] + adjustment_coeficient
                G = self.image_pixels[i,n][1] + adjustment_coeficient
                B = self.image_pixels[i,n][2] + adjustment_coeficient
                
                if R > 255:
                    R = 255
                elif R < 0:
                    R = 0
                if G > 255:
                    G = 255
                elif G < 0:
                    G = 0
                if B > 255:
                    B = 255
                elif B < 0:
                    B = 0
                self.new_image_pixels[i, n] = (R, G, B)

    def adjust_contrast(self, adjustment_coeficient):
    
        for i in range (0, self.image.size[0]):
            for n in range (0, self.image.size[1]):
                R = self.image_pixels[i,n][0] * adjustment_coeficient
                G = self.image_pixels[i,n][1] * adjustment_coeficient
                B = self.image_pixels[i,n][2] * adjustment_coeficient
                
                if R > 255:
                    R = 255
                elif R < 0:
                    R = 0
                if G > 255:
                    G = 255
                elif G < 0:
                    G = 0
                if B > 255:
                    B = 255
                elif B < 0:
                    B = 0
                    
                self.new_image_pixels[i, n] = (R, G, B)

    def negative(self):
        for i in range (0, self.image.size[0]):
            for n in range (0, self.image.size[1]):
            
                R = 255 - self.image_pixels[i,n][0]
                G = 255 - self.image_pixels[i,n][1] 
                B = 255 - self.image_pixels[i,n][2] 
                
                self.new_image_pixels[i, n] = (R, G, B)

    def histogram_equalization(self, histogram):
        
        cumulative_histogram = [0] * 256
        num_pixels = self.image.size[0] * self.image.size[1]
        
        alpha = 255.0 / num_pixels
        
        cumulative_histogram[0] = int(round(histogram[0] * alpha))
        
        for i in range(1, 255):
            cumulative_histogram[i] = int(round((cumulative_histogram[i-1] + histogram[i] * alpha)/num_pixels * 255))
        
        for i in range (0, self.image.size[0]):
            for n in range (0, self.image.size[1]):
                self.new_image_pixels[i,n] = (cumulative_histogram[self.image_pixels[i,n][0]], 
                                                        cumulative_histogram[self.image_pixels[i,n][0]], 
                                                        cumulative_histogram[self.image_pixels[i,n][0]])
                
    def right_turn(self):
        self.new_image = Image.new("RGBA", (self.image.size[1], self.image.size[0]))
        self.new_image_pixels = self.new_image.load()
        for i in range (0, self.image.size[0]):
            for n in range (0, self.image.size[1]):
                x = abs(self.image.size[1] - 1 - n)
                y = i
                self.new_image_pixels[x,y] = self.image_pixels[i, n]
                
    def left_turn(self):
        self.new_image = Image.new("RGBA", (self.image.size[1], self.image.size[0]))
        self.new_image_pixels = self.new_image.load()
        for i in range (0, self.image.size[0]):
            for n in range (0, self.image.size[1]):
                x = n
                y = abs(self.image.size[0] -1 - i)
                self.new_image_pixels[x,y] = self.image_pixels[i, n]

    def convolution(self):
        conv_matrix = [[0, -1, 0], [-1, 4, -1], [0, -1, 0]]
        
        for i in range(1, self.image.size[0] -1):
            for n in range(1, self.image.size[1]-1):
                A_i = conv_matrix[2][2] * self.image_pixels[i-1,n-1][0]
                B_h = conv_matrix[2][1] * self.image_pixels[i-1, n][0]
                C_g = conv_matrix[2][0] * self.image_pixels[i-1, n+1][0]
                D_f = conv_matrix [1][2] * self.image_pixels[i, n-1][0]
                E_e = conv_matrix[1][1] * self.image_pixels[i, n][0]
                F_d = conv_matrix[1][0] * self.image_pixels[i, n+1][0]
                G_c = conv_matrix[0][2] * self.image_pixels[i+1, n-1][0]
                H_b = conv_matrix[0][1] * self.image_pixels[i+1, n][0]
                I_a = conv_matrix[0][0] * self.image_pixels[i+1, n+1][0]
                conv_result =  A_i + B_h + C_g + D_f + E_e + F_d + G_c + H_b + I_a
                if conv_result < 0:
                    conv_result = 0
                if conv_result > 255:
                    conv_result = 255
                self.new_image_pixels[i,n] = (conv_result, conv_result, conv_result)
                
class ImageDisplay:
    
    def __init__(self):
        self.w = QtGui.QWidget()
        self.b = QtGui.QLabel(self.w)
        self.app = QtGui.QApplication(sys.argv)
    
    def display_image(self, image):
        label = QtGui.QLabel(self.w)
        pixmap = QtGui.QPixmap.fromImage(image)
        pixmap.detach()
        label.setPixmap(pixmap)
        self.w.resize(pixmap.width(), pixmap.height())
        self.w.show()
        sys.exit(self.app.exec_())
 
 
