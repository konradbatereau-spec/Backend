<!DOCTYPE html>

<html>

<head>
    <meta charset="UTF-8">
    <link rel="stylesheet" href="styles.css">
    <title>Login | Chat</title>
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
            <h1>Login</h1>
            <p>Hier kannst du dich mit Namen und Passwort einloggen.</p>
            <div class="m-t-15 m-b-15">
                <label>Name:</label>
                <input id="name" type="text">
            </div>
            <div class="m-t-15 m-b-15">
                <label>Passwort:</label>
                <input id="passwort" type="password">
            </div>
            <div>
                <button class="button hintergrund-grün" onclick="login()">Login</button>
                <span id="meldung"></span>
            </div>
        </div>
    </div>
    <audio autoplay>
        <source src="musik.mp3" type="audio/mpeg">
    </audio>
    <script>
        const meldungSpan = document.getElementById("meldung");

        function login() {
            const name = document.getElementById("name").value;
            const passwort = document.getElementById("passwort").value;
            if (passwort == localStorage.getItem(name)) {
                window.location.href = "intern.html";
                localStorage.setItem("eingelogt",name)
            } else {
                meldungSpan.style.color = "#F17A7C";
                meldungSpan.innerText = "Name oder Passwort falsch!";
            }
        }
    </script>
</body>

</html>