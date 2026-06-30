import requests
import json  # Oder 'import ujson as json' für noch mehr Speed (muss per pip installiert werden)

# Definition der Daten vorab, um Zeit während der Requests zu sparen
url_start = 'https://www.app.farning.de/api/labyrinth/minigame/start'
url_score = 'https://www.app.farning.de/api/labyrinth/minigame/highscore'

headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc2ODMxNjE2MCwianRpIjoiNWQ2MjM1YmEtNzQ4MC00MWJlLWI5MzktNjU0MjY3NmJlMzk5IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6ImtvbnJhZGJhdGVyZWF1IiwibmJmIjoxNzY4MzE2MTYwLCJjc3JmIjoiOWFlODEwZjAtODkxZS00MjU1LWI1ODYtY2NjNTMzZGU2OWNjIiwiZXhwIjoxNzk5ODUyMTYwfQ.V9Qi5lZYmEZxTC6sNRw0rWTt8l7-f88BcN4Vgit7eV0'
}

# Eine Session erstellen, um die TCP/TLS-Verbindung wiederzuverwenden
with requests.Session() as session:
    session.headers.update(headers)
    
    # 1. Start-Request abfeuern
    r1 = session.post(url_start)
    
    # 2. Token blitzschnell extrahieren
    # .json() direkt aufrufen und den Key ziehen (Konstruktion als Dict spart String-Verkettung)
    payload = {"runToken": r1.json()["runToken"]}
    
    # 3. Highscore-Request sofort hinterher senden
    r2 = session.put(url_score, json=payload)

# Erst ganz am Ende ausgeben, um die Zeit dazwischen nicht zu verfälschen
print(f"Start-Status: {r1.status_code}")
print(f"Highscore-Antwort: {r2.text}")