# Projekat - Detekcija šumskog požara sa satelitskih slika



Napomena:
Korišćen dataset je https://www.kaggle.com/datasets/abdelghaniaaba/wildfire-prediction-dataset. 

Projekat u ovom repozitorijumu sadrži samo mali deo skupa zbog limita samog git-a, obzirom na količinu od preko 40 000 slika koje je potrebno lokalno organizovati radi obučavanja generalizovanog modela.

Sva potrebna dokumentacija se nalazi u folderu Organizacija projketa.




Neophodni koraci za instalaciju i pokretanje projekta :


## 1. Kloniranje repozitorijuma
```bash
git clone https://github.com/ksenijaocisnik/MS_PROJEKAT.git
cd MS_PROJEKAT
```

## 2. Kreiranje virtuelnog okruzenja
   
   - ### Windows
```
python -m venv venv
venv\Scripts\activate
```

   - #### macOS/Linux
```
python3 -m venv venv
source venv/bin/activate
```

## 3. Instalacija potrebnih paketa
```
pip install -r requirements.txt
```

## 4. Pokretanje projekta
```
python main.py
```
