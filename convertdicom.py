import pydicom as dicom
import numpy as np
from PIL import Image
import os
##########
def dicom_to_img (path):
    dicom_img = dicom.read_file(path)
    
    rows = dicom_img.get(0x00280010).value
    cols = dicom_img.get(0x00280011).value
    
    instance_number = int (dicom_img.get(0x00200013).value)
    
    window_center = int (dicom_img.get(0x00281050).value)
    window_width =    int (dicom_img.get(0x00281051).value)
    
    
    window_max = int (window_center + window_width / 2)
    window_min = int (window_center - window_width / 2)
    
    
    if (dicom_img.get(0x00281052) is None):
        rescale_intercept = 0
        
    else:
        rescale_intercept = int (dicom_img.get(0x00281052).value)
        
    if (dicom_img.get(0x00281053) is None):
        rescale_slope = 1
        
    else:
        rescale_slope = int (dicom_img.get(0x00281053).value)
        
        
    new_img = np.zeros((rows, cols), np.uint8)
    pixels = dicom_img.pixel_array
    
    
    for i in range (0, rows):
        for j in range (0, cols):
            pix_val = pixels[i][j]
            rescale_pix_val = pix_val * rescale_slope + rescale_intercept
            
            if (rescale_pix_val > window_max):
                new_img [i][j] = 255
                
            elif (rescale_pix_val < window_min):
                new_img[i][j] = 0
                
            else:
                new_img[i][j] = int (((rescale_pix_val - window_min) / (window_max - window_min)) * 255)
                
    return new_img, instance_number