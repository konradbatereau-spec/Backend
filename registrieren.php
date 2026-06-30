
<?php
$datenbank = new SQLite3("datenbank.db");

$datenbank->exec("CREATE TABLE IF NOT EXISTS nutzer (name, passwort)");
if($_SERVER["REQUEST_METHOD"]=="POST") {
    $name = $_POST["name"];
    $passwort = $_POST["passwort"];
    $anzahl=$datenbank->querySingle("SELECT COUNT(*) FROM nutzer WHere name = '$name'");
    echo("$anzahl");
    if ($anzahl == 0){
        $datenbank->exec("insert into nutzer values ('$name', '$passwort')");
    } else {
        echo "Nutzername bereits vergeben!";
    }
}
?>



<!DOCTYPE html>

<html>

<head>
    <meta charset="UTF-8">
    <link rel="stylesheet" href="styles.css">
    <title>Registrieren | Chat</title>
</head>

<body>
    <div class="text-links">
        <a class="text-weiß" href="index.html">
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor"
                class="bi bi-arrow-left-circle" viewBox="0 0 16 16">
                <path fill-rule="evenodd"
                    d="M1 8a7 7 0 1 0 14 0A7 7 0 0 0 1 8m15 0A8 8 0 1 1 0 8a8 8 0 0 1 16 0m-4.5-.5a.5.5 0 0 1 0 1H5.707l2.147 2.146a.5.5 0 0 1-.708.708l-3-3a.5.5 0 0 1 0-.708l3-3a.5.5 0 1 1 .708.708L5.707 7.5z" />
            </svg>
            Zurück
        </a>
    </div>
    <div class="mitte">
        <div class="text-links">
            <h1>Registrieren</h1>
            <p>Hier kannst du dich mit Namen und Passwort registrieren.</p>
            <form method="POST">
                <div class="m-t-15 m-b-15">
                    <label>Name:</label>
                    <input id="name" name="name" type="text">
                </div>
                <div class="m-t-15 m-b-15">
                    <label>Passwort:</label>
                    <input id="passwort" name="passwort" type="password">
                </div>
                <div>
                    <button class="button hintergrund-blau" onclick="registrieren()" type="submit">Registrieren</button>
                    <span id="meldung"></span>
                </div>
            </form>
        </div>
    </div>
    <audio autoplay>
        <source src="musik.mp3" type="audio/mpeg">
    </audio>
    <script>
        const meldungSpan = document.getElementById("meldung");

        function registrieren() {
            const name = document.getElementById("name").value;
            const passwort = document.getElementById("passwort").value;

            if (name in localStorage) {
                meldungSpan.style.color = "#F17A7C";
                meldungSpan.innerText = "Name schon vergeben!";
            } else {
                localStorage.setItem(name, passwort);
                meldungSpan.style.color = "#6AFBCF";
                meldungSpan.innerText = "Erfolgreich registriert!";
            }
        }
    </script>
</body>

</html>