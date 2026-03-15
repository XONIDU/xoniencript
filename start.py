#!/usr/bin/env python3
# Creditos: XONIDU
# start.py - Instalador de dependencias y lanzador de XONIENCRIPT

import os
import sys
import subprocess
import platform
from time import sleep

# Colores para terminal
GREEN = '\033[92m'
RED = '\033[91m'
RESET = '\033[0m'
BOLD = '\033[1m'

def clear_screen():
    """Limpia la pantalla según el sistema operativo"""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_banner():
    """Muestra el banner de XONIDU"""
    clear_screen()
    print(GREEN + BOLD)
    print("╔══════════════════════════════════════╗")
    print("║         XONIENCRIPT v1.0             ║")
    print("║         by XONIDU                     ║")
    print("╚══════════════════════════════════════╝")
    print(RESET)

def check_and_install_dependencies():
    """Verifica e instala Flask (única dependencia necesaria)"""
    print(GREEN + "[*] Verificando dependencias..." + RESET)
    
    try:
        __import__('flask')
        print(GREEN + "[✓] Flask ya está instalado" + RESET)
        return True
    except ImportError:
        print(RED + "[!] Flask no está instalado. Instalando..." + RESET)
        try:
            # Detectar sistema operativo para el flag adecuado
            if platform.system() == "Linux":
                subprocess.check_call([sys.executable, "-m", "pip", "install", "flask", "--break-system-packages"])
            else:
                subprocess.check_call([sys.executable, "-m", "pip", "install", "flask"])
            
            print(GREEN + "[✓] Flask instalado correctamente" + RESET)
            return True
        except subprocess.CalledProcessError as e:
            print(RED + f"[✗] Error instalando Flask: {e}" + RESET)
            return False

def launch_xoniencript():
    """Lanza el archivo xoniencript.py"""
    if not os.path.exists('xoniencript.py'):
        print(RED + "[✗] Error: No se encuentra xoniencript.py en el directorio actual" + RESET)
        print(GREEN + "[*] Asegúrate de tener el archivo xoniencript.py en la misma carpeta" + RESET)
        return False
    
    print(GREEN + "[*] Iniciando XONIENCRIPT..." + RESET)
    print(GREEN + "[*] Servidor web en: http://localhost:5000" + RESET)
    print(GREEN + "[*] Presiona CTRL+C para detener el servidor" + RESET)
    sleep(2)
    
    try:
        # Ejecutar xoniencript.py
        subprocess.run([sys.executable, 'xoniencript.py'])
    except KeyboardInterrupt:
        print(GREEN + "\n[*] Servidor detenido" + RESET)
    except Exception as e:
        print(RED + f"[✗] Error al ejecutar xoniencript.py: {e}" + RESET)
        return False
    
    return True

def show_menu():
    """Muestra el menú principal"""
    print(GREEN + BOLD)
    print("╔══════════════════════════════════════╗")
    print("║           XONIENCRIPT LAUNCHER       ║")
    print("╠══════════════════════════════════════╣")
    print("║  [0] Instalar dependencias           ║")
    print("║  [1] Lanzar XONIENCRIPT              ║")
    print("║  [2] Salir                            ║")
    print("╚══════════════════════════════════════╝")
    print(RESET)

def main():
    """Función principal"""
    while True:
        print_banner()
        show_menu()
        
        opt = input(GREEN + "> Opción: " + RESET)
        
        if opt == "0":
            print(GREEN + "[*] Instalando dependencias..." + RESET)
            if check_and_install_dependencies():
                print(GREEN + "[✓] Proceso completado" + RESET)
            else:
                print(RED + "[✗] Error en la instalación" + RESET)
            sleep(2)
            
        elif opt == "1":
            # Verificar dependencias antes de lanzar
            if check_and_install_dependencies():
                launch_xoniencript()
            else:
                print(RED + "[✗] No se pueden instalar las dependencias necesarias" + RESET)
                sleep(2)
            
            input(GREEN + "\nPresiona Enter para volver al menú..." + RESET)
            
        elif opt == "2":
            print(GREEN + "\n[*] Saliendo...")
            print("[*] Créditos: XONIDU")
            print(RESET)
            sleep(1)
            clear_screen()
            break
            
        else:
            print(RED + "[!] Opción inválida" + RESET)
            sleep(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(GREEN + "\n\n[*] Hasta pronto!" + RESET)
        sys.exit(0)
