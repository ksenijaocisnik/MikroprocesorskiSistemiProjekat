import tkinter as tk
from tkinter import filedialog
from PIL import ImageTk, Image
from get_prediction import get_prediction 
from values import IMAGE_HEIGHT, IMAGE_WIDTH
from notifications import trigger_alarm

# Funkcija koja dinamički prikazuje ili skriva polja na osnovu izbora radio butttons-a
def toggle_fields(alarm_type, email_label, email_entry, port_label, port_entry):
    if alarm_type.get() == "email":
        email_label.grid(sticky="w", padx=20, pady=10)  
        email_entry.grid(sticky="w", padx=20, pady=10)  
        port_label.grid_remove()  
        port_entry.grid_remove()
    elif alarm_type.get() == "device":
        port_label.grid(sticky="w", padx=20, pady=10)  
        port_entry.grid(sticky="w", padx=20, pady=10)  
        email_label.grid_remove() 
        email_entry.grid_remove()
    else:
        email_label.grid_remove()  
        email_entry.grid_remove()
        port_label.grid_remove()
        port_entry.grid_remove()


# Funkcija za centriranje prozora na ekranu
def center_window(root, width=600, height=400):
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')

# Funkcija za upload slike i prikaz rezultata
def upload_image(panel, result_label, alarm_type, email, port):
    # Otvaramo prozor za biranje slike i ucitavamo izabranu sliku preko path-a
    file_path = filedialog.askopenfilename() 
    img = Image.open(file_path) 

    # Menjamo velicinu slike kako bismo je prikazali u velicinu u kojoj ce biti i obradjena
    # To ukkljucuje i promenu broj piksela, pa moramo da vrsimo Resmpling
    img = img.resize((IMAGE_HEIGHT, IMAGE_WIDTH), Image.Resampling.LANCZOS)  
    # Vrsinu promenu formata u onaj koji biblioteka moze da podrzi
    img = ImageTk.PhotoImage(img)  
    # Ubacujemo sliku u gui, tacnije u panel de0
    panel.config(image=img) 
    # Zadrzavamo referencu na sliku kako bimo mogli i dalje da je prikazujemo (kako je ne bi pokupio garbage collector)
    panel.image = img  

    # Dobijamo rezultat nase predikcije
    result, probability = get_prediction(file_path)

    # Ažuriramo result_label-a tako sto update-ujemo gui sa potrebnim tekstom i pokrecemo alarm 
    # Alarm se pokrece tako sto pozivamo funkciju trigger_alarm koja ce na osnovu vrednosti alarm_type odrediti koja funkcija se poziva
    print(f"\033[94mresult: {result}\033[0m") 
    if result == 'fire':
        trigger_alarm(alarm_type, email, port)
        result_label.config(text=f"OPASNOST! Požar detektovan!\nVerovatnoća: {probability:.2f}%", fg="red")
    else:
        result_label.config(text=f"BEZBEDNO: Nema požara.\nVerovatnoća: {probability:.2f}%", fg="green")


# Funkcija za kreiranje gui aplikacije
def create_gui():
    # Kreiramo glavni prozor aplikacije i dodeljujemo naziv 
    root = tk.Tk()
    root.title("Detekcija šumskog požara")

    # Definišemo dimenzije naše aplikacije i centriramo aplikaciju na sredinu ekrana
    center_window(root, 600, 800)  

    # Postavljamo svetlo sivu pozadinu
    root.configure(bg="#f0f0f0")  

    # Definišemo prostor kolone i reda
    root.grid_columnconfigure(0, weight=1)  
    root.grid_rowconfigure(1, weight=1)    

    # Naslov aplikacije koji se dodaje u glavni prozor (root)
    # Postavljamo ga u nultu kolonu i nulti red naše mreže (grid)
    title_label = tk.Label(root, text="Detekcija šumskog požara", font=("Arial", 20), bg="#f0f0f0")
    title_label.grid(row=0, column=0, padx=10, pady=20)

    # Definišemo mesto za sliku i njene dimenzije
    panel = tk.Label(root, bg="white", width=300, height=300)
    panel.grid(row=1, column=0, padx=10, pady=20)

    # Definišemo mesto za prikazivanje rezultata
    result_label = tk.Label(root, text="Rezultat će biti prikazan ovde", font=("Arial", 16), bg="#f0f0f0")
    result_label.grid(row=3, column=0, padx=10, pady=30)

    # Opcije za odabir alarma (radio buttons), gde ćemo definisati default vrednost kao sound
    # jer je za email potrebno definisati email posiljaoca i sifru, a za device je potebno da je neki uredjaj povezan za port koji zelimo
    alarm_type = tk.StringVar(value="sound")  

    # Label za odabir tipa alarma
    tk.Label(root, text="Izaberite tip alarma:", font=("Arial", 14), bg="#f0f0f0").grid(row=4, column=0, padx=10, pady=10, sticky="w")

    # Kreiramo labelu i polje za email 
    email_label = tk.Label(root, text="Unesite email adresu:", font=("Arial", 12), bg="#f0f0f0")
    email_entry = tk.Entry(root, font=("Helvetica", 12), width=30)

    # Kreiramo labelu i polje za port
    port_label = tk.Label(root, text="Unesite serijski port (npr. COM3):", font=("Arial", 12), bg="#f0f0f0")
    port_entry = tk.Entry(root, font=("Helvetica", 12), width=30)

    # Definišemo dugme za upload slike
    upload_btn = tk.Button(root, text="Učitaj sliku", font=("Arial", 14), bg="#113163", fg="white", width=20, command=lambda: upload_image(panel, result_label, alarm_type.get(), email_entry.get(), port_entry.get()))
    upload_btn.grid(row=2, column=0, padx=10, pady=10) 

    # Radio dugmići za tip alarma
    tk.Radiobutton(root, text="Reprodukuj Zvuk", variable=alarm_type, value="sound", bg="#f0f0f0", font=("Arial", 12), command=lambda: toggle_fields(alarm_type, email_label, email_entry, port_label, port_entry)).grid(row=5, column=0, sticky="w", padx=20)
    tk.Radiobutton(root, text="Pošalji Email", variable=alarm_type, value="email", bg="#f0f0f0", font=("Arial", 12), command=lambda: toggle_fields(alarm_type, email_label, email_entry, port_label, port_entry)).grid(row=6, column=0, sticky="w", padx=20)
    tk.Radiobutton(root, text="Pošalji Signal na Uređaj", variable=alarm_type, value="device", bg="#f0f0f0", font=("Arial", 12), command=lambda: toggle_fields(alarm_type, email_label, email_entry, port_label, port_entry)).grid(row=7, column=0, sticky="w", padx=20)

    # Prikaži ili sakrij polja za unos na osnovu podrazumevanog izbora
    toggle_fields(alarm_type, email_label, email_entry, port_label, port_entry)

    # Pokrećemo glavnu petlju tkinter gui aplikacije
    root.mainloop()
