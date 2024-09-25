import tkinter as tk
from tkinter import filedialog
import pygame
import smtplib
import serial  # Za serijsku komunikaciju

# Funkcija za slanje email-a
def send_email_alert(email):
    # Uneti mejl (potreban je mejl koji nema omogucenu 2FA)
    sender_email = "..."
    # Unesti lozinku 
    password = "..."

    msg = f"Subject: ALARM: Požar Detektovan!\n\nPožar je detektovan na satelitskom snimku."
    try:
        # Kreiramo SMTP objekat za komunikaciju sa serverom
        server = smtplib.SMTP('smtp.gmail.com', 587)
        # Zapocinjemo Transport Layer Security sesije za sifrovanje
        server.starttls()
        # Logujemo se
        server.login(sender_email, password)
        # Saljemo email na unetu adresu sa porukom koju smo definisali kao msg
        server.sendmail(sender_email, email, msg)
        # Zatvaramo konekciju sa serverom
        server.quit()
        print(f"Email je poslat na adresu: {email}!")
    except Exception as e:
        print(f"Error: slanje email-a: {e}")

# Funkcija za reprodukciju zvuka
def play_alarm_sound():
   pygame.mixer.init()
   pygame.mixer.music.load('./alarm_sounds/strange-notification.mp3')  
   pygame.mixer.music.play()


# Funkcija za slanje signala na uređaj preko serijskog porta i primanje povratne poruke
def send_signal_to_device(port):
    try:
        # Port i brzina prenosa podataka, standardno 9600
        # Dodajemo timeout za čitanje
        ser = serial.Serial(port, 9600, timeout=1)  
        # Saljemo broj 1 kao signal uređaju, u binarnom formatu
        ser.write(b'1')  
        print(f"Poslat signal na {port}.")
        # Čitanje povratne poruke sa uređaja i dekodiranje u string
        response = ser.readline().decode('utf-8').strip()  
        print(f"Povratna poruka sa uređaja: {response}")
        
        # Zatvaramo serijski port
        ser.close()
        print(f"Povratna poruka sa uređaja: {response}")
    except serial.SerialException as e:
        print(f"Error : otvaranje porta: {e}")
    except Exception as e:
        print(f"Error: {e}")

# Funkcija koja se poziva na osnovu izabira radio button-a
def trigger_alarm(alarm_type, email, port):
    if alarm_type == "email":
        if email:
            send_email_alert(email)
        else:
            print("Nije uneta email adresa.")
    elif alarm_type == "sound":
        play_alarm_sound()
    elif alarm_type == "device":
        if port:
            send_signal_to_device(port)
        else:
            print("Nije unet port za slanje signala.")