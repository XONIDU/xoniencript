from flask import Flask, request, flash, redirect, url_for, make_response, render_template
from werkzeug.utils import secure_filename
import io
import socket
import qrcode
import base64

# Configuración básica de Flask
app = Flask(__name__)
app.secret_key = "XONIDU-Darian_Alberto_Camacho_Salas"  # Clave para mensajes flash

# Tamaño máximo razonable por subida
app.config['MAX_CONTENT_LENGTH'] = 20 * 1024 * 1024  # 20 MB

# ===== FUNCIONES PARA QR =====
def generate_qr_base64(url):
    """Genera un código QR en base64 para mostrar en HTML"""
    try:
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(url)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Convertir a base64
        buffered = io.BytesIO()
        img.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        
        return img_str
    except Exception as e:
        print(f"Error generando QR: {e}")
        return None

def get_server_url():
    """Obtiene la URL del servidor"""
    try:
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        return f"http://{local_ip}:5500"
    except:
        return "http://localhost:5500"

# ===== ALGORITMO DE CIFRADO =====
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

# ===== RUTAS =====
@app.route("/", methods=["GET", "POST"])
def index():
    # Generar QR para la URL del servidor
    server_url = get_server_url()
    qr_base64 = generate_qr_base64(server_url)
    
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

    # Renderizar template HTML con el QR
    return render_template('index.html', qr_code=qr_base64, server_url=server_url)

@app.route("/qr_code")
def qr_code():
    """Endpoint para obtener el código QR como JSON"""
    server_url = get_server_url()
    qr_base64 = generate_qr_base64(server_url)
    
    if qr_base64:
        return {
            "qr_base64": qr_base64,
            "url": server_url
        }
    else:
        return {"error": "No se pudo generar el QR"}, 500

# ===== INICIO =====
if __name__ == "__main__":
    host = "0.0.0.0"
    port = 5500
    server_url = get_server_url()
    
    print("=" * 50)
    print("🔐 XONIENCRIPT by XONIDU")
    print("=" * 50)
    print(f"📡 Servidor: {host}:{port}")
    print(f"🌐 URL local: {server_url}")
    
    # Generar QR para la terminal
    try:
        qr_ascii = qrcode.QRCode()
        qr_ascii.add_data(server_url)
        print("\n📱 Escanea este código QR desde tu teléfono:")
        print("-" * 50)
        qr_ascii.print_ascii()
        print("-" * 50)
        print(f"O accede a: {server_url}/qr_code para ver el QR")
    except Exception as e:
        print(f"\n📱 Accede a: {server_url}/qr_code para ver el QR")
        print("(Instala 'pip install qrcode pillow' para ver QR en terminal)")
    
    print("=" * 50)
    print("✅ Servidor listo")
    print("=" * 50)
    
    # No debug/reloader para mantener comportamiento estable
    app.run(host=host, port=port, debug=False, use_reloader=False)
