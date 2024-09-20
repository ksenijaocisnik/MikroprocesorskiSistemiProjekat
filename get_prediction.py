from tensorflow.keras.models import load_model
from preprocess_image import preprocess_image  

# Funkcija koja ucitava nas model i za odredjenu sliku vrsi predikciju 

def get_prediction(image_path):
    # Ucitavamo model
    model = load_model('fire_detection.h5')

    # Obradjujemo sliku i dobijamo nas niz vrednosti (bathc_size, img_height, img_width, color_count)
    img_array = preprocess_image(image_path)

    # Pravimp predikciju
    # Uzimamo samo prvi element jer nam model vraca niz predikcija za velicinu naseg batch-a jer je naucio da radi na grupama slika,
    #   zatim uzimamo samo prvu vrednost tog niza jer imamo binarnu klasifikaciju -> pa u nizu imamo samo jedan broj
    prediction = model.predict(img_array)[0][0]

    print(f"\033[94mprediction: {prediction:.4f}\033[0m") 

    
    # Vracamo rezultat
    # Ovakva raspodela vrednosti binarne klasifikacije je ishod redosleda trening skupova (prvo fire, zatim no_fire)
    if prediction < 0.5:
        result = 'fire'
        probability = (1 - prediction) * 100
    else:
        result = 'no_fire'
        probability = prediction * 100
    
    return result, probability