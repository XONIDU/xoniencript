import os

# Cuerpo del programa
print(chr(27) + f"[1;31m" + "")
print("""-x_encript-
▒▒▒▄▄▄▄▄▒▒▒
▒▄█▄█▄█▄█▄▒
▒▒▒▒░░░▒▒▒▒
▒▒▒▒░░░▒▒▒▒
▒▒▒▒░░░▒▒▒▒
by: xonidu
""")

# Cifrado César
def caesar_cipher(text, shift):
    encrypted = []
    for char in text:
        if char.isalpha():  # Solo letras
            shift_base = 65 if char.isupper() else 97
            # Asegura valores positivos con módulo 26
            encrypted_char = chr((ord(char) - shift_base + shift) % 26 + shift_base)
            encrypted.append(encrypted_char)
        else:
            encrypted.append(char)
    return ''.join(encrypted)

def encrypt_file(file_name, shift):
    with open(file_name, "r", encoding="utf-8") as file:
        original = file.read()
    encrypted = caesar_cipher(original, shift)
    with open(file_name, "w", encoding="utf-8") as encrypted_file:
        encrypted_file.write(encrypted)

def decrypt_file(file_name, shift):
    with open(file_name, "r", encoding="utf-8") as file:
        encrypted = file.read()
    decrypted = caesar_cipher(encrypted, -shift)
    with open(file_name, "w", encoding="utf-8") as decrypted_file:
        decrypted_file.write(decrypted)

# Interfaz de usuario
def cifrar():
    print("""-cifrar:      [0]
-des cifrar:  [1]""")
    x = input("-Selecciona una opcion: ")

    if x == "0":
        archivo = input("-Nombre del archivo con formato: ")
        shift = int(input("-Clave: "))
        encrypt_file(archivo, shift)
        print("\n[+] Archivo cifrado con éxito. Contenido:\n")
        with open(archivo, "r", encoding="utf-8") as f:
            print(f.read())

    elif x == "1":
        archivo = input("-Nombre del archivo con formato: ")
        shift = int(input("-Clave: "))
        decrypt_file(archivo, shift)
        print("\n[+] Archivo descifrado con éxito. Contenido:\n")
        with open(archivo, "r", encoding="utf-8") as f:
            print(f.read())

    else:
        print("[!] Opción no válida. Intenta de nuevo.\n")
        cifrar()

# Bucle principal
while True:
    cifrar()
