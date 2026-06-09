import time
import subprocess
from pynput.mouse import Button, Controller

# Maus-Controller initialisieren
mouse = Controller()

def bot_aktion():
    print("Bot startet in 3 Sekunden... Wechsel jetzt zum Zielfenster!")
    time.sleep(3)
    
    # 1. Maus an eine bestimmte Position bewegen (X, Y Pixelkoordinaten)
    # Beispiel: In die Mitte des Bildschirms (z.B. X=500, Y=400)
    ziel_x = 500
    ziel_y = 400
    mouse.position = (ziel_x, ziel_y)
    print(f"Maus bewegt zu: {mouse.position}")
    time.sleep(0.5) # Kurze Pause, damit es natürlicher wirkt
    
    # 2. Linksklick ausführen
    mouse.click(Button.left, 1)
    print("Klick ausgeführt!")
    
    # Kurz warten, bis das Programm reagiert
    time.sleep(1)
    
    # 3. Automatisch ein Bildschirmfoto machen
    # Wir nutzen das Mac-eigene Werkzeug und speichern es als 'bot_screenshot.png'
    output_datei = "bot_screenshot.png"
    subprocess.run(["screencapture", "-x", output_datei]) 
    # Das '-x' sorgt dafür, dass das Foto lautlos (ohne Kamera-Geräusch) gemacht wird
    
    print(f"Bildschirmfoto gespeichert unter: {output_datei}")

if __name__ == "__main__":
    bot_aktion()