import os
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from values import IMAGE_HEIGHT, IMAGE_WIDTH, BATCH_SIZE
from PIL import ImageFile

ImageFile.LOAD_TRUNCATED_IMAGES = True
# Ucitavanja slika i priprema

base_dir = 'satelite_images/'

def load_data():

    train_dir = os.path.join(base_dir, 'train')
    val_dir = os.path.join(base_dir, 'valid')
    test_dir = os.path.join(base_dir, 'test')

    # Porebno je da izvrsimo pripremu nasih satelitskih slika
    # Moramo da izvrsimo normalizacija piksela na opseg izmedju 0 i 1 radi lakseg treniranja modela 
    #   obzirom da piskeli idu od 0 do 255
    # Kako bismo bolje istrnirali nas model, mozemo da vrsimo i nasumicne izmene slika: 
    #   rotation_range - rotiranje
    #   horizontal_flip - okretanje slika horizontalno 
    #   zoom_range - zumiranje slike
    image_data_generator = ImageDataGenerator(rescale=1./255, rotation_range=20, horizontal_flip=True)

    # Generator za treniranje podataka
    # flow_from_directory -> automatski ucitavmo slike iz direktorijuma i konvertujemo ih u BATCHES (grupe)
    #   kako bimo omogucili da nase citanje slika bude postepeno
    train_generator = image_data_generator.flow_from_directory(
        train_dir,
        target_size=(IMAGE_HEIGHT, IMAGE_WIDTH),
        batch_size=BATCH_SIZE,
        class_mode='binary'
    )

    # Generator za validacione podatke
    val_generator = image_data_generator.flow_from_directory(
        val_dir,
        target_size=(IMAGE_HEIGHT, IMAGE_WIDTH),
        batch_size=BATCH_SIZE,
        class_mode='binary'
    )

    # Generator za testne podatke 
    test_generator = image_data_generator.flow_from_directory(
        test_dir,
        target_size=(IMAGE_HEIGHT, IMAGE_WIDTH),
        batch_size=BATCH_SIZE,
        class_mode='binary'
    )

    return train_generator, val_generator, test_generator
