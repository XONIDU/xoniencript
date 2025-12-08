from flask import Flask, request, flash, redirect, url_for, make_response, render_template_string
from werkzeug.utils import secure_filename
import io

app = Flask(__name__)
app.secret_key = "clave_secreta_para_flask"  # Clave para mensajes flash

# No se guardará nada en disco: todo en memoria
# Tamaño máximo razonable por subida (ajusta si quieres)
app.config['MAX_CONTENT_LENGTH'] = 20 * 1024 * 1024  # 20 MB

# Algoritmo de Cifrado César (trabaja con texto Unicode)
def caesar_cipher(text, shift):
    encrypted = []
    for char in text:
        if char.isalpha():
            # Mantener mayúsculas/minúsculas
            shift_base = ord('A') if char.isupper() else ord('a')
            encrypted.append(chr((ord(char) - shift_base + shift) % 26 + shift_base))
        else:
            encrypted.append(char)
    return ''.join(encrypted)

# Procesar contenido en memoria (no escribe nada en disco)
def process_content(content_text, shift, action):
    if action == "encrypt":
        processed = caesar_cipher(content_text, shift)
    else:
        processed = caesar_cipher(content_text, -shift)
    return processed

# HTML embebido: tema negro con texto blanco, nombre XONIENCRIPT, hecho por XONIDU
HTML_PAGE = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>XONIENCRIPT — XONIDU</title>
    <style>
        :root {
            --bg: #000000;
            --fg: #ffffff;
            --accent: #ffffff;
            --card: #0b0b0b;
            --muted: #ffffff;
        }
        html,body{height:100%;margin:0;}
        body {
            background: var(--bg);
            color: var(--fg);
            font-family: system-ui, -apple-system, "Segoe UI", Roboto, Arial;
            padding: 18px;
            display:flex;
            align-items:flex-start;
            justify-content:center;
        }
        .box {
            width:100%;
            max-width:720px;
            background: linear-gradient(180deg, rgba(255,255,255,0.03), rgba(255,255,255,0.01));
            border: 1px solid rgba(255,255,255,0.06);
            padding:18px;
            border-radius:10px;
            box-shadow: 0 6px 30px rgba(0,0,0,0.6);
        }
        h1 { margin:0 0 8px 0; font-size:1.25rem; color:var(--accent) }
        p.hint { color: var(--muted); margin: 8px 0 16px 0; }
        label { display:block; margin-top:10px; font-weight:600; color:var(--fg) }
        input[type="file"], input[type="number"], button {
            margin-top:8px;
            padding:10px;
            border-radius:8px;
            border:1px solid rgba(255,255,255,0.08);
            background: transparent;
            color: var(--fg);
            width:100%;
            box-sizing:border-box;
        }
        button {
            background: var(--accent);
            color: #000;
            font-weight:700;
            cursor:pointer;
            border:none;
            margin-top:14px;
        }
        .msg { color:#ff6666; margin-top:10px; }
        footer { margin-top:14px; color:var(--muted); font-size:0.85rem; text-align:right; }
        @media(min-width:600px){
            .inputs{display:flex;gap:10px}
            .inputs > *{flex:1}
        }
    </style>
</head>
<body>
    <div class="box">
        <h1>XONIENCRIPT</h1>
        <p class="hint">Hecho por XONIDU — Cifrado César para archivos de texto. Nada se guarda en el servidor; todo se procesa en memoria.</p>

        {% with messages = get_flashed_messages() %}
          {% if messages %}
            <div class="msg">
              {% for m in messages %}
                <div>{{ m }}</div>
              {% endfor %}
            </div>
          {% endif %}
        {% endwith %}

        <form method="POST" enctype="multipart/form-data" novalidate>
            <label for="file">Selecciona un archivo de texto (.txt):</label>
            <input type="file" name="file" id="file" accept=".txt,text/plain" required>

            <label for="shift">Desplazamiento (0–25):</label>
            <input type="number" name="shift" id="shift" min="0" max="25" value="3" required>

            <div style="margin-top:10px;">
                <input type="radio" name="action" value="encrypt" id="encrypt" required>
                <label for="encrypt" style="display:inline; margin-left:8px;">Cifrar</label>
                &nbsp;&nbsp;
                <input type="radio" name="action" value="decrypt" id="decrypt" required>
                <label for="decrypt" style="display:inline; margin-left:8px;">Descifrar</label>
            </div>

            <button type="submit">Procesar y descargar (sin guardar)</button>
        </form>

        <footer>XONIDU</footer>
    </div>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Validar acción
        action = request.form.get("action")
        if action not in ("encrypt", "decrypt"):
            flash("Acción no válida.")
            return redirect(url_for("index"))

        # Validar archivo
        upload = request.files.get("file")
        if not upload or upload.filename == "":
            flash("No se seleccionó ningún archivo.")
            return redirect(url_for("index"))

        # Leer y procesar el archivo en memoria (sin escribir en disco)
        try:
            raw = upload.read()
            # Intentar decodificar UTF-8, si falla usar latin-1 como fallback
            try:
                text = raw.decode("utf-8")
            except Exception:
                text = raw.decode("latin-1")
        except Exception as e:
            flash("Error leyendo el archivo: " + str(e))
            return redirect(url_for("index"))

        # Validar shift
        try:
            shift = int(request.form.get("shift", 0))
            if not (0 <= shift <= 25):
                raise ValueError("Fuera de rango")
        except Exception:
            flash("Desplazamiento inválido. Debe ser un número entre 0 y 25.")
            return redirect(url_for("index"))

        # Procesar
        try:
            processed_text = process_content(text, shift, action)
        except Exception as e:
            flash("Error procesando el archivo: " + str(e))
            return redirect(url_for("index"))

        # Preparar respuesta como descarga (sin guardar en servidor)
        orig_name = secure_filename(upload.filename) or "input.txt"
        out_name = f"processed_{orig_name}"
        data = processed_text.encode("utf-8")
        response = make_response(data)
        response.headers["Content-Type"] = "text/plain; charset=utf-8"
        response.headers["Content-Disposition"] = f"attachment; filename={out_name}"
        return response

    return render_template_string(HTML_PAGE)

if __name__ == "__main__":
    host = "0.0.0.0"
    port = 5500
    print(f"* XONIENCRIPT (by XONIDU) running on {host}:{port}")
    # No debug/reloader to keep comportamiento estable
    app.run(host=host, port=port, debug=False, use_reloader=False)