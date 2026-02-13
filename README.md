# 📦 Sistema de Inventario Hogareño para Raspberry Pi

Un sistema ligero y eficiente basado en **Flask** y **SQLite** para organizar cajas y artículos del hogar. Diseñado específicamente para correr en una Raspberry Pi y ser accesible desde cualquier dispositivo de tu red WiFi.

## 🚀 Características
- **ABM Completo:** Interfaz simple para agregar, editar y eliminar artículos.
- **Búsqueda Inteligente:** Buscador rápido que filtra por nombre del artículo, descripción o caja.
- **Filtro por Cajas:** Al hacer clic en el nombre de una caja, el sistema muestra instantáneamente todo su contenido.
- **Diseño Responsive:** Optimizado para usar con el celular mientras ordenas tus cajas físicamente.
- **Backups Automáticos:** Configuración preparada para respaldar la base de datos diariamente.
<img width="1442" height="589" alt="image" src="https://github.com/user-attachments/assets/c0e4b8ab-d9ca-43fc-bf2f-2138edb087ec" />

## 🛠️ Instalación en Raspberry Pi

1. **Preparar la carpeta y clonar:**
```bash
mkdir ~/inventario
cd ~/inventario
git clone https://github.com/nfontan/inventario-pi.git
```

2. **Crear y activar el entorno virtual (PEP 668):**
```bash
python3 -m venv env
source env/bin/activate

```


3. **Instalar dependencias:**
```bash
pip install flask flask-sqlalchemy

```


4. **Ejecutar la aplicación:**
```bash
python app.py

```


Luego, abre en tu navegador: `http://<IP_DE_TU_PI>:5000`

## 💾 Configuración de Backups

Para evitar pérdida de datos, el sistema utiliza un script de Bash (`backup_db.sh`) programado en el sistema:

1. **Dar permisos al script:**
```bash
chmod +x backup_db.sh

```


2. **Programar en Crontab (`crontab -e`):**
Añadir la siguiente línea para ejecutar el backup todos los días a las 03:00 AM:
```cron
00 03 * * * /bin/bash /root/inventario/backup_db.sh

```



## 📋 Estructura del Proyecto

* `app.py`: Servidor Flask y lógica de base de datos.
* `templates/`:
* `index.html`: Panel principal y lista de artículos.
* `editar.html`: Formulario dedicado para modificar registros.


* `backup_db.sh`: Script automatizado de respaldo.
* `instance/`: Carpeta donde se aloja `inventario.db` (SQLite).

## 🛡️ Notas de Seguridad

El archivo `.gitignore` está configurado para evitar subir el entorno virtual (`env/`) y la base de datos local (`*.db`) al repositorio público, protegiendo tu privacidad y manteniendo el repositorio ligero.

