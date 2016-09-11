from PyQt4 import QtGui
from PIL import Image, ImageQt
import sys
from math import floor    

class Editor:

    def __init__(self, image, new_image, image_pixels, new_image_pixels):
        self.image = image
        self.image_pixels = image_pixels
        self.new_image = new_image
        self.new_image_pixels = new_image_pixels
    
    def horizontal_flip(self):
        for x in range (0, self.image.size[0]):
            for y in range (0, self.image.size[1]):
                new_x = abs(self.image.size[0] -1 - x)          # New x coordinate
                self.new_image_pixels[new_x, y] = self.image_pixels[x, y]
        
    def vertical_flip(self):
        for x in range (0, self.image.size[0]):
            for y in range (0, self.image.size[1]):
                new_y = abs(self.image.size[1] -1 - y)          # New y coordinate
                self.new_image_pixels[x,new_y] = self.image_pixels[x, y]
                
    def turn_gray(self):
    
        for x in range (0, self.image.size[0]):
            for y in range (0, self.image.size[1]):
                
                # Calculates the proportion of Red, Green and Blue needed in the grayScale shade
                R = self.image_pixels[x, y][0]
                G = self.image_pixels[x, y][1]
                B = self.image_pixels[x, y][2]
                gray_shade = int(0.299*R + 0.587*G + 0.114*B)
                self.new_image_pixels[x, y] = (gray_shade, gray_shade, gray_shade)

    def quantization(self, num_levels):
        start = 0
        shades = []
        range_shades = 256/num_levels 
        
        # Gets all the shades to be used
        for i in range(0, 256, range_shades):
            tone = (start + i)/2
            shades.append(tone)
            start = i+1
        
        for x in range (0, self.image.size[0]):
            for y in range (0, self.image.size[1]):
                new_shade = (self.image_pixels[x, y][0]) / range_shades         # Gets the index to locate the appropriate shade of the pixel
                self.new_image_pixels[x, y] = (shades[new_shade], shades[new_shade], shades[new_shade])
                    
    def make_histogram(self):
        self.histogram = [0] * 256
        self.normalized_histogram = [0] * 256
        biggest_column = 0

        self.turn_gray()
                
        for x in range (0, self.image.size[0]):
            for y in range (0, self.image.size[1]):
                shade = self.image_pixels[x, y][1]
                self.histogram[shade] += 1
                if self.histogram[shade] > biggest_column:
                    biggest_column = self.histogram[shade]
                    
                    
        for i in range(0, 255):
            self.normalized_histogram[i] = int(round( float(self.histogram[i]) / biggest_column * 255))
            
        return self.normalized_histogram
        
    def adjust_brightness(self, adjustment_coeficient):
        
        for x in range (0, self.image.size[0]):
            for y in range (0, self.image.size[1]):
                R = self.image_pixels[x,y][0] + adjustment_coeficient
                G = self.image_pixels[x,y][1] + adjustment_coeficient
                B = self.image_pixels[x,y][2] + adjustment_coeficient
                
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
                    
                self.new_image_pixels[x, y] = (R, G, B)

    def adjust_contrast(self, adjustment_coeficient):
    
        for x in range (0, self.image.size[0]):
            for y in range (0, self.image.size[1]):
                R = self.image_pixels[x,y][0] * adjustment_coeficient
                G = self.image_pixels[x,y][1] * adjustment_coeficient
                B = self.image_pixels[x,y][2] * adjustment_coeficient
                
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
                    
                self.new_image_pixels[x, y] = (R, G, B)

    def negative(self):
        for x in range (0, self.image.size[0]):
            for y in range (0, self.image.size[1]):
            
                R = 255 - self.image_pixels[x,y][0]
                G = 255 - self.image_pixels[x,y][1] 
                B = 255 - self.image_pixels[x,y][2] 
                
                self.new_image_pixels[x, y] = (R, G, B)

    def histogram_equalization(self, histogram):
        
        self.cumulative_histogram = [0] * 256
        num_pixels = self.image.size[0] * self.image.size[1]
        
        alpha = 255.0 / num_pixels
        
        self.cumulative_histogram[0] = (histogram[0] * alpha)
                
        for i in range(1, 256):
            self.cumulative_histogram[i] = (self.cumulative_histogram[i-1] + histogram[i] * alpha)
                        
        for x in range (0, self.image.size[0]):
            for y in range (0, self.image.size[1]):
                self.new_image_pixels[x, y] = (int(round(self.cumulative_histogram[self.image_pixels[x,y][0]])), 
                                                        int(round(self.cumulative_histogram[self.image_pixels[x,y][1]])), 
                                                        int(round(self.cumulative_histogram[self.image_pixels[x,y][2]])))
                
    def right_turn(self):
        self.new_image = Image.new("RGBA", (self.image.size[1], self.image.size[0]))
        self.new_image_pixels = self.new_image.load()
        for x in range (0, self.image.size[0]):
            for y in range (0, self.image.size[1]):
                new_x = abs(self.image.size[1] - 1 - y)
                new_y = x
                self.new_image_pixels[new_x,new_y] = self.image_pixels[x, y]
                
    def left_turn(self):
        self.new_image = Image.new("RGBA", (self.image.size[1], self.image.size[0]))
        self.new_image_pixels = self.new_image.load()
        for x in range (0, self.image.size[0]):
            for y in range (0, self.image.size[1]):
                new_x = y
                new_y = abs(self.image.size[0] -1 - x)
                self.new_image_pixels[new_x, new_y] = self.image_pixels[x, y]

    def convolution(self, conv_matrix):        
        for x in range(1, self.image.size[0] -1):
            for y in range(1, self.image.size[1]-1):
                A_i = conv_matrix[2][2] * self.image_pixels[x-1, y-1][0]
                B_h = conv_matrix[2][1] * self.image_pixels[x-1, y][0]
                C_g = conv_matrix[2][0] * self.image_pixels[x-1, y+1][0]
                D_f = conv_matrix [1][2] * self.image_pixels[x, y-1][0]
                E_e = conv_matrix[1][1] * self.image_pixels[x, y][0]
                F_d = conv_matrix[1][0] * self.image_pixels[x, y+1][0]
                G_c = conv_matrix[0][2] * self.image_pixels[x+1, y-1][0]
                H_b = conv_matrix[0][1] * self.image_pixels[x+1, y][0]
                I_a = conv_matrix[0][0] * self.image_pixels[x+1, y+1][0]
                conv_result =  A_i + B_h + C_g + D_f + E_e + F_d + G_c + H_b + I_a
                if conv_result < 0:
                    conv_result = 0
                if conv_result > 255:
                    conv_result = 255
                self.new_image_pixels[x,y] = (int(round(conv_result)), int(round(conv_result)), int(round(conv_result)))
                 
    def zoom_in(self):
        self.new_image = Image.new("RGBA", (2*self.image.size[0], 2*self.image.size[1]))
        self.new_image_pixels = self.new_image.load()

        for x in range(0, self.image.size[0]-1):
            for y in range(0, self.image.size[1]-1):
                
                self.new_image_pixels[2*x, 2*y] = self.image_pixels[x, y]
                    
                # if i % 2 == 0 and n % 2 != 0:
                R_new_shade = int(round((self.image_pixels[x, y][0] + self.image_pixels[x+1,y][0])/2))
                G_new_shade = int(round((self.image_pixels[x, y][1] + self.image_pixels[x+1,y][1])/2))
                B_new_shade = int(round((self.image_pixels[x, y][2] + self.image_pixels[x+1,y][2])/2))
                self.new_image_pixels[(2*x)+1,2*y] = (R_new_shade, G_new_shade, B_new_shade)
                
                # elif i % 2 != 0 and n % 2 == 0:
                R_new_shade = int(round((self.image_pixels[x, y][0] + self.image_pixels[x, y+1][0])/2))
                G_new_shade = int(round((self.image_pixels[x, y][1] + self.image_pixels[x, y+1][1])/2))
                B_new_shade = int(round((self.image_pixels[x, y][2] + self.image_pixels[x, y+1][2])/2))
                self.new_image_pixels[2*x,(2*y)+1] = (R_new_shade, G_new_shade, B_new_shade)

                # elif i % 2 != 0 and n % 2 != 0:
                R_new_shade = int(round((self.image_pixels[x, y][0] + self.image_pixels[x+1, y][0] + self.image_pixels[x, y+1][0] + self.image_pixels[x+1, y+1][0])/4))
                G_new_shade = int(round((self.image_pixels[x, y][1] + self.image_pixels[x+1, y][1] + self.image_pixels[x, y+1][1] + self.image_pixels[x+1, y+1][1])/4))
                B_new_shade = int(round((self.image_pixels[x, y][2] + self.image_pixels[x+1, y][2] + self.image_pixels[x, y+1][2] + self.image_pixels[x+1, y+1][2])/4))
                self.new_image_pixels[(2*x)+1,(2*y)+1] = (R_new_shade, G_new_shade, B_new_shade)
                    
    def zoom_out(self):
        zoom_factor_x = 2
        zoom_factor_y = 2
        
        self.new_image = Image.new("RGBA", (self.image.size[0]/zoom_factor_x, self.image.size[1]/zoom_factor_y))
        self.new_image_pixels = self.new_image.load()
        
        for x in range(0, self.image.size[0], zoom_factor_x):
            for y in range(0, self.image.size[1], zoom_factor_y):
                R_new_shade = 0
                G_new_shade = 0
                B_new_shade = 0
                for j in range(0, zoom_factor_y):
                    for k in range(0, zoom_factor_x):
                        try:
                            R_new_shade += self.image_pixels[x+zoom_factor_y, y+zoom_factor_x][0]
                            G_new_shade += self.image_pixels[x+zoom_factor_y, y+zoom_factor_x][1]
                            B_new_shade += self.image_pixels[x+zoom_factor_y, y+zoom_factor_x][2]
                        except:
                            pass
                        
                R_new_shade = int(round(R_new_shade/(zoom_factor_y*zoom_factor_x)))
                G_new_shade = int(round(G_new_shade/(zoom_factor_y*zoom_factor_x)))
                B_new_shade = int(round(B_new_shade/(zoom_factor_y*zoom_factor_x)))
                self.new_image_pixels[x/zoom_factor_x, y/zoom_factor_y] = (R_new_shade, G_new_shade, B_new_shade)
