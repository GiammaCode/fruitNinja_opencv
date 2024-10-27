import os

image_path = "C:/Users/giamm/Desktop/fruitNinja_opencv/assets/images/apple.png"

# Controlla se il file esiste
if os.path.exists(image_path):
    print("Il file esiste.")

    # Controlla se è leggibile
    if os.access(image_path, os.R_OK):
        print("Il file è leggibile.")
    else:
        print("Errore: Il file non è leggibile. Verifica i permessi.")
else:
    print("Errore: Il file non esiste nel percorso specificato.")
