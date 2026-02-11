from flask import Flask, request, flash, redirect, url_for, make_response, render_template
from werkzeug.utils import secure_filename
import io

# Configuración básica de Flask
app = Flask(__name__)
app.secret_key = "clave_secreta_para_flask"  # Clave para mensajes flash

# Tamaño máximo razonable por subida
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

# Ruta principal con template
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

    # Renderizar template HTML
    return render_template('index.html')

# Ejecutar aplicación
if __name__ == "__main__":
    host = "0.0.0.0"
    port = 5500
    print(f"* XONIENCRIPT (by XONIDU) running on {host}:{port}")
    # No debug/reloader para mantener comportamiento estable
    app.run(host=host, port=port, debug=False, use_reloader=False)
