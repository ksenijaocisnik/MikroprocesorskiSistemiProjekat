from tensorflow.keras.preprocessing.image import img_to_array, load_img
import numpy as np
from values import IMAGE_WIDTH, IMAGE_HEIGHT

# Funkcija za obradu slike kakvu nas model moze da prepozna
def preprocess_image(image_path):
    # Manjmo sirinu i visinu
    img = load_img(image_path, target_size=(IMAGE_HEIGHT, IMAGE_WIDTH))  

    # Normalizujemo piksele na opseg izmedju 0 i 1
    img_array = img_to_array(img) / 255.0 

    # Potrebno je da dodamo batch dimenziju, sto je u nasem slusaju 1 (grupa koja se sastoji od jedne slike)
    # axis = 0 -> batch dimenzija se dodaje na pocetak
    # nas niz izgleda ovako : (1, 224, 224, 3) : grupa od jedne slike, visina, sirina, broj boja
    img_array = np.expand_dims(img_array, axis=0)  
    
    return img_array
