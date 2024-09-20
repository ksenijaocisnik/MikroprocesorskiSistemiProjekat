from tensorflow.keras.models import load_model
from data_loader import load_data 

# Provera tacnosti modela nad testnim podacim/satelitskim slikama

if __name__ == '__main__':
    # Potrebno je da ucitam kreirani model
    fire_detection_model = load_model('fire_detection.h5')
    # Potreban je generator slika za test folder
    _, _, test_generator = load_data()

    # Evalucaija modela: 
    test_loss, test_accuracy = fire_detection_model.evaluate(test_generator)

    # Loss -> gubitak 
    # Pokazuje nam koliko nas model gresi na datom skupu podataka
    print(f"\033[94mTest loss: {test_loss:.4f}\033[0m") 
    # Accuracy -> Tacnost
    # Pokazuje nam procenat ispravnih predikcija 
    print(f"\033[94mTest accuracy: {test_accuracy:.4f}\033[0m") 
    
    # Dobijene vrednosti: 
    # Test loss: 0.0952 
    #   mera greska u predikciji je < 0.1, tako da mozemo smatrati da nas model retko gresi
    # Test accuracy: 0.9651
    #   mera tacnosti je 96.51% sto je dosta visoko, tako da mozemo da smatramo
    #   da nas model moze da generalizuje i tacno predvidja klasifikaciju novih podataka/satelitskih slika


