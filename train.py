from resnet50 import create_model
from data_loader import load_data
from values import EPOCHS
from tensorflow.keras.callbacks import EarlyStopping


# Treniranje mdoela 

model_save_path = 'fire_detection.h5'

def train_model():

    # Kreiramo model
    model = create_model()
    # Potreni su nam generatori 
    train_generator, val_generator, test_generator = load_data()

    # Treniramo model koristeći učitane podatke
    # Koristmo early stopping, gde stedimo vreme, jer ako se za 3 uzastopne epohne (patience) tacnost modela ne popravi, mozemo da zaustavimo treniranje

    early_stopping = EarlyStopping(monitor='val_loss', patience=3, restore_best_weights=True)
    model.fit(train_generator, epochs=EPOCHS, validation_data=val_generator, callbacks=[early_stopping])

    # Cuvamo istrenirani model
    model.save(model_save_path)
    print(f"\033[92mModel je sačuvan: {model_save_path}\033[0m")

if __name__ == '__main__':
    train_model()
