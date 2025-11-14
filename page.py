from flask import Flask, request, flash, redirect, url_for, make_response
import os

# Configuración básica de Flask
app = Flask(__name__)
app.secret_key = "clave_secreta_para_flask"  # Clave para mensajes flash
UPLOAD_FOLDER = "./uploads"
RESULT_FOLDER = "./results"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["RESULT_FOLDER"] = RESULT_FOLDER

# Algoritmo de Cifrado César
def caesar_cipher(text, shift):
    encrypted = []
    for char in text:
        if char.isalpha():  # Solo letras
            shift_base = 65 if char.isupper() else 97
            encrypted.append(chr((ord(char) - shift_base + shift) % 26 + shift_base))
        else:
            encrypted.append(char)
    return ''.join(encrypted)

# Procesar archivo
def process_file(file_path, shift, action):
    # Leer el contenido del archivo original
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()

    # Determinar si se cifra o descifra
    if action == "encrypt":
        processed_content = caesar_cipher(content, shift)
    else:
        processed_content = caesar_cipher(content, -shift)

    # Guardar el resultado en otro archivo
    result_file_path = os.path.join(app.config["RESULT_FOLDER"], f"processed_{os.path.basename(file_path)}")
    with open(result_file_path, "w", encoding="utf-8") as result_file:
        result_file.write(processed_content)

    return result_file_path

# Ruta principal con Html embebido
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Validar acción seleccionada
        action = request.form.get("action")
        if action not in ["encrypt", "decrypt"]:
            flash("Acción no válida seleccionada.")
            return redirect(url_for("index"))

        # Validar archivo subido
        if "file" not in request.files:
            flash("No se seleccionó ningún archivo.")
            return redirect(url_for("index"))

        file = request.files["file"]
        if file.filename == "":
            flash("No se seleccionó ningún archivo.")
            return redirect(url_for("index"))

        # Guardar archivo subido
        file_path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
        file.save(file_path)

        # Validar desplazamiento (clave)
        try:
            shift = int(request.form.get("shift"))
        except ValueError:
            flash("Introduce un número válido para el desplazamiento.")
            return redirect(url_for("index"))

        # Procesar el archivo
        result_file = process_file(file_path, shift, action)

        # Devolver archivo procesado al usuario
        with open(result_file, "r", encoding="utf-8") as file:
            processed_content = file.read()

        response = make_response(processed_content)
        response.headers["Content-Disposition"] = f"attachment; filename={os.path.basename(result_file)}"
        response.mimetype = "text/plain"
        return response

    # HTML embebido junto con el formulario
    return """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Cifrado César</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                text-align: center;
                background-color: #f4f4f9;
                padding: 2em;
                color: #333;
            }
            .container {
                background: #fff;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 0 10px rgba(0,0,0,0.1);
                display: inline-block;
            }
            input[type="file"], input[type="number"], button {
                margin: 10px 0;
                padding: 10px;
                width: 80%;
            }
            button {
                background-color: #007BFF;
                color: white;
                border: none;
                border-radius: 5px;
                cursor: pointer;
            }
            button:hover {
                background-color: #0056b3;
            }
            .error {
                color: red;
                font-size: 0.9em;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Cifrado César</h1>
            <p>Sube un archivo y elige si deseas cifrar o descifrar el contenido.</p>
            <form method="POST" enctype="multipart/form-data">
                <label for="file">Sube tu archivo de texto:</label><br>
                <input type="file" name="file" required><br>
                <label for="shift">Desplazamiento (clave):</label><br>
                <input type="number" name="shift" min="0" max="25" required><br>
                <input type="radio" name="action" value="encrypt" id="encrypt" required>
                <label for="encrypt">Cifrar</label><br>
                <input type="radio" name="action" value="decrypt" id="decrypt" required>
                <label for="decrypt">Descifrar</label><br>
                <button type="submit">Procesar Archivo</button>
            </form>
        </div>
    </body>
    </html>
    """

# Ejecutar aplicación
if __name__ == "__main__":
    app.run(debug=True)
