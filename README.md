# 🔐 XONIENCRIPT

**Advertencia:** Este código tiene únicamente fines educativos. El cifrado César es un método antiguo y débil, no debe usarse para proteger información sensible. El autor no se hace responsable del uso indebido.

## 🎯 ¿Qué es XONIENCRIPT?

XONIENCRIPT es una herramienta Python que implementa el cifrado César para archivos de texto, presentada a través de una interfaz web con estética hacker (negro y verde). Consta de dos componentes:

- **start.py** - Lanzador/instalador que verifica dependencias y ejecuta el programa
- **xoniencript.py** - Aplicación web Flask con el cifrador/descifrador César

Características principales:
- ✨ Interfaz web estilo terminal hacker
- 🔒 Cifrado y descifrado de archivos .txt
- ⚙️ Desplazamiento personalizable (0-25)
- 💾 Procesamiento en memoria - nada se guarda en el servidor
- 📥 Descarga directa del archivo procesado

## 📥 Instalación

Clona el repositorio desde GitHub:

```bash
git clone https://github.com/XONIDU/xoniencript.git
cd xoniencript
```

## ✅ Requisitos

- Python 3.8+ instalado
- Dependencias Python: Flask (se instala automáticamente con start.py)

### Dependencias por plataforma:

#### 🐧 Arch Linux

```bash
# Instalar dependencias del sistema (si es necesario)
sudo pacman -S python-pip

# Ejecutar el lanzador (instalará Flask automáticamente)
python start.py
```

#### 🐧 Ubuntu / Debian

```bash
# Actualizar repositorios
sudo apt update

# Instalar Python y pip si no están
sudo apt install python3 python3-pip -y

# Ejecutar el lanzador
python3 start.py
```

#### 🪟 Windows

1. Instala Python 3 desde [python.org](https://python.org)
2. Abre una terminal (cmd o PowerShell) y ejecuta:

```bash
python start.py
```

#### 🍎 MacOS

```bash
# Asegúrate de tener Python instalado
python3 start.py
```

## ⚙️ Uso

1. Ejecuta el lanzador:

```bash
python start.py
```

2. En el menú del lanzador, elige:

```
╔══════════════════════════════════════╗
║         XONIENCRIPT LAUNCHER         ║
╠══════════════════════════════════════╣
║  [0] Instalar dependencias           ║
║  [1] Lanzar XONIENCRIPT              ║
║  [2] Salir                           ║
╚══════════════════════════════════════╝
```

3. Selecciona **Opción 1** para iniciar el servidor web
4. Abre tu navegador y ve a: **http://localhost:5000**
5. En la interfaz web:
   - Selecciona un archivo .txt
   - Elige el desplazamiento (0-25)
   - Selecciona "Cifrar" o "Descifrar"
   - Haz clic en "EJECUTAR PROCESO"
6. El archivo procesado se descargará automáticamente

### Ejemplo de cifrado

**Texto original:** `HOLA MUNDO`
**Desplazamiento:** 3
**Texto cifrado:** `KROD PXQGR`

## 🔒 Consideraciones de seguridad y ética

- ⚠️ **El cifrado César NO es seguro** - es un método histórico fácilmente rompible
- No uses esta herramienta para proteger información realmente confidencial
- Es solo para fines educativos y de aprendizaje de criptografía básica
- Todo el procesamiento ocurre en memoria local, nada se envía a servidores externos

## 🐛 Problemas comunes

- **"El puerto 5000 ya está en uso"**: Cierra otros programas que usen ese puerto o modifica el puerto en xoniencript.py
- **"No se encuentra xoniencript.py"**: Asegúrate de que ambos archivos (.py) están en el mismo directorio
- **Error de permisos en Linux**: Usa `chmod +x start.py` para dar permisos de ejecución
- **Flask no se instala**: En Linux, prueba con `--break-system-packages` (ya lo maneja automáticamente el script)

## 📦 Archivos incluidos

- **start.py** — Lanzador/instalador (verifica e instala Flask según el SO)
- **xoniencript.py** — Aplicación web principal con el cifrador César
- **README.md** — Este archivo de documentación

## 📊 Estadísticas del proyecto

- **Estrellas:** 0
- **Lenguaje principal:** Python 100%
- **Licencia:** Educativo

## ✉️ Contacto y Créditos

- **Proyecto:** XONIENCRIPT
- **Creador:** Darian Alberto Camacho Salas
- **Contacto:** xonidu@gmail.com
- **#Somos XONIDU**

---

*"La criptografía no es solo seguridad, es también arte y matemáticas."*

