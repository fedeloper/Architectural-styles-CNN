import os
import numpy as np 
import cv2 
from matplotlib import pyplot as plt
import time
from pathlib import Path


def hsvBounders(rgbTriplet):
    rgb = np.array(rgbTriplet, dtype=np.uint8)
    hsvTriplet = cv2.cvtColor(rgb, cv2.COLOR_RGB2HSV)
    return np.array([hsvTriplet[0][0][0]-30, 50, 50]), np.array([hsvTriplet[0][0][0]+30, 255, 255])


bgr_ = [ [[[255,0,0]]], [[[0,255,0]]], [[[0,0,255]]] ]
low_green, high_green = hsvBounders(bgr_[1])
low_blue, high_blue = hsvBounders(bgr_[2])


def colorMask(pathImages, pathDst):
    bgr_ = [ [[[255,0,0]]], [[[0,255,0]]], [[[0,0,255]]] ]
    low_green, high_green = hsvBounders(bgr_[1])
    low_blue, high_blue = hsvBounders(bgr_[2])


    print("Prendo le immagini da {}.\nSalvo le immagini in: {}".format(pathImages, pathDst))
    with os.scandir(pathImages) as files:
        for imgP in files: # itero per tutte le immagini in una sottocartella
            if os.path.isfile(imgP.path):
                #print(img.name)
                img = cv2.imread(imgP.path)
                img = cv2.resize(img, (300, 300), interpolation=cv2.INTER_CUBIC)
                
                # Denoise Colors
                img = cv2.fastNlMeansDenoisingColored(img, None, 10, 10, 7, 11)

                # reshape the image into a 2D array
                pixel_vals = img.reshape((-1,3))
                # convert to float type
                pixel_vals = np.float32(pixel_vals)
                # define stop criteria
                criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.85)
                # perform k-means clustering with n number of clusters
                k = 6
                retval, labels, centers = cv2.kmeans(pixel_vals, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
                # convert data into 8-bit values
                centers = np.uint8(centers)
                segmented_data = centers[labels.flatten()]
                # reshape data into the original dimensions
                segmented_image = segmented_data.reshape((img.shape))

                # Convert RBG to HSV
                hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
                #hsv = cv2.cvtColor(segmented_image, cv2.COLOR_BGR2HSV)

                # Create the mask for the green 
                mask_g = cv2.inRange(hsv, low_green, high_green)
                # Create the mask for the blue
                mask_b = cv2.inRange(hsv, low_blue, high_blue)

                # Invert the green mask
                inv_mask_g = 255-mask_g
                # Invert the green mask
                inv_mask_b = 255-mask_b

                # Apply the mask to cancel the green and then the blue
                res = cv2.bitwise_and(img, img, mask=inv_mask_g)
                res = cv2.bitwise_and(res, res, mask=inv_mask_b)
                
                
                
                cv2.imwrite(pathDst+"/"+imgP.name, res)




#print("\n",os.getcwd())

pathname = "D:/LaureaMagistrale/Primo_Semestre/Fundations_Data_Science/materiale progetto/archietctural styles/arcDataset_enlarged" # change last name folder accordingly to the dataset
dst = "D:/LaureaMagistrale/Primo_Semestre/Fundations_Data_Science/materiale progetto/archietctural styles/arcDataset_enlarged_mkII" # same here

os.chdir(pathname)
print("Current Working Directory " , os.getcwd())

with os.scandir() as entries:
    for entry in entries: # itero per tutte le sotto cartelle
        if os.path.isdir(entry.path):
            print("\n")
            # Crea la cartella destinazione
            Path(os.path.join(dst, entry.name)).mkdir(parents=False, exist_ok=True)

            # Chiama la funzione direttamente su tutta la cartella
            colorMask(entry.path ,os.path.join(dst,entry.name))
