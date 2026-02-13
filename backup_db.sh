#!/bin/bash

# Configuración
ORIGEN="/root/inventario/instance/inventario.db"
DESTINO="/root/backups_inventario"
FECHA=$(date +"%Y-%m-%d_%H%M%S")

# Crear el backup con la fecha en el nombre
cp "$ORIGEN" "$DESTINO/inventario_$FECHA.db"

# (Opcional) Borrar backups viejos de más de 30 días para no llenar la SD
find "$DESTINO" -type f -name "*.db" -mtime +30 -delete

echo "Backup realizado con éxito: inventario_$FECHA.db"
