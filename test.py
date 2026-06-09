import subprocess
import io
import sys
from PIL import Image

def analyze_labyrinth(image_bytes):
    """Analysiert das Labyrinth direkt aus den Bild-Bytes im Arbeitsspeicher."""
    try:
        img = Image.open(io.BytesIO(image_bytes)).convert('RGB')
    except Exception:
        return "Fehler: Die Daten in der Zwischenablage konnten nicht als Bild geladen werden."
        
    width, height = img.size
    
    # 2. Automatisches Zuschneiden (Weißen Rand entfernen)
    left, top, right, bottom = width, height, 0, 0
    for y in range(height):
        for x in range(width):
            r, g, b = img.getpixel((x, y))
            if not (r > 240 and g > 240 and b > 240):
                if x < left: left = x
                if x > right: right = x
                if y < top: top = y
                if y > bottom: bottom = y
                
    if right <= left or bottom <= top:
        return "Fehler: Labyrinth konnte im Bild nicht isoliert werden."
        
    cropped_img = img.crop((left, top, right + 1, bottom + 1))
    c_width, c_height = cropped_img.size
    
    # 3. 15x15 Raster berechnen
    grid_size = (15, 15)
    cell_w = c_width / grid_size[1]
    cell_h = c_height / grid_size[0]
    
    grid_matrix = [[" " for _ in range(grid_size[1])] for _ in range(grid_size[0])]
    
    # 4. Jedes Feld analysieren
    for y in range(grid_size[0]):
        for x in range(grid_size[1]):
            center_x = int(x * cell_w + cell_w / 2)
            center_y = int(y * cell_h + cell_h / 2)
            
            r, g, b = cropped_img.getpixel((center_x, center_y))
            
            if b > r + 40 and b > g + 40:
                grid_matrix[y][x] = "S"  # Start
            elif g > r + 40 and g > b + 40:
                grid_matrix[y][x] = "E"  # Ende
            elif r < 100 and g < 100 and b < 100:
                grid_matrix[y][x] = "1"  # Wand
            else:
                grid_matrix[y][x] = "0"  # Weg
                
    return grid_matrix


def find_path_bfs(matrix):
    """Findet den kürzesten Weg mithilfe von Breitensuche (BFS)."""
    start, end = None, None
    for y in range(len(matrix)):
        for x in range(len(matrix[0])):
            if matrix[y][x] == 'S':
                start = (y, x)
            elif matrix[y][x] == 'E':
                end = (y, x)

    if not start or not end:
        return "Fehler: Start oder Ziel wurde in der Matrix nicht gefunden."

    queue = [[start]]
    visited = {start}
    directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]

    while queue:
        path = queue.pop(0)
        curr_y, curr_x = path[-1]

        if (curr_y, curr_x) == end:
            return path

        for dy, dx in directions:
            ny, nx = curr_y + dy, curr_x + dx

            if 0 <= ny < len(matrix) and 0 <= nx < len(matrix[0]):
                if matrix[ny][nx] != '1' and (ny, nx) not in visited:
                    visited.add((ny, nx))
                    new_path = list(path)
                    new_path.append((ny, nx))
                    queue.append(new_path)

    return "Fehler: Kein gültiger Weg zum Ziel gefunden."


def generate_movement_commands(path):
    """Generiert die Steuerbefehle basierend auf dem berechneten Pfad."""
    if not path or isinstance(path, str):
        return path

    dir_vectors = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    current_dir_idx = 2  # Startblickrichtung: Süden (nach unten)
    commands = []

    for i in range(len(path) - 1):
        curr = path[i]
        nxt = path[i+1]

        move_vec = (nxt[0] - curr[0], nxt[1] - curr[1])
        target_dir_idx = dir_vectors.index(move_vec)
        turn_diff = (target_dir_idx - current_dir_idx) % 4

        if turn_diff == 1:
            commands.append("rt()")
        elif turn_diff == 2:
            commands.append("rt()")
            commands.append("rt()")
        elif turn_diff == 3:
            commands.append("lt()")

        commands.append("fd()")
        current_dir_idx = target_dir_idx

    return commands


if __name__ == "__main__":
    print("⏳ Lese Bildschirmfoto aus der Mac-Zwischenablage...")
    
    try:
        # AppleScript-Befehl ausführen, um rohe PNG-Daten aus der Zwischenablage abzufragen
        script = "osascript -e 'get the clipboard as «class PNGf»'"
        result = subprocess.check_output(script, shell=True).decode('utf-8').strip()
        
        # Säubere die hexadezimale Rückgabe von AppleScript
        if result.startswith("«data PNGf"):
            hex_data = result.replace("«data PNGf", "").replace("»", "")
        else:
            # Falls AppleScript das Format leicht anders ausgibt
            hex_data = result.split()[-1].replace("»", "")
            
        image_bytes = bytes.fromhex(hex_data)
        
    except Exception:
        print("❌ Fehler: Es befindet sich kein valides Bild in der Zwischenablage.")
        print("💡 Tipp: Drücke erst Cmd+Shift+Ctrl+4 und ziehe den Rahmen um das Labyrinth!")
        sys.exit(1)
        
    # --- Verarbeitung starten ---
    matrix = analyze_labyrinth(image_bytes)
    
    if isinstance(matrix, str):
        print(matrix)
        sys.exit(1)
        
    # Konsolen-Ausgabe der erkannten Matrix
    print("\nErkanntes Labyrinth:")
    for row in matrix:
        print("[" + ", ".join(f"'{cell}'" for cell in row) + "]")
        
    print("\nBerechne Pfad...")
    path = find_path_bfs(matrix)
    
    if isinstance(path, list):
        # Befehle generieren
        befehle = generate_movement_commands(path)
        befehle_text = "\n".join(befehle)
        
        # Befehle direkt zurück in die Mac-Zwischenablage kopieren (überschreibt das Bild)
        process = subprocess.Popen('pbcopy', stdin=subprocess.PIPE, text=True)
        process.communicate(befehle_text)
        
        print(f"\n🎉 Pfad erfolgreich berechnet ({len(path) - 1} Schritte)!")
        print("📋 Die Steuerbefehle wurden direkt in deine Zwischenablage kopiert.")
        print("👉 Du kannst sie jetzt mit Cmd+V im Zielprogramm einfügen.")
    else:
        print(path)