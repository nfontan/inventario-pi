#!/bin/bash
#Este script es igual que la version 1 pero mantiene solo 3 copias en disco y envia 1 vez por semana una copia a gdrive utilizando rclone
#https://rclone.org/drive/#making-your-own-client-id

# Configuración
ORIGEN="/root/inventario/instance/inventario.db"
DESTINO="/root/backups_inventario"
FECHA=$(date +"%Y-%m-%d_%H%M%S")
DIA_SEMANA=$(date +"%u") # 1=Lunes, 7=Domingo

# 1. Crear el backup local con la fecha
cp "$ORIGEN" "$DESTINO/inventario_$FECHA.db"

# 2. Rotación local: Mantener solo los 3 archivos más recientes y borrar el resto
cd "$DESTINO" || exit
ls -t inventario_*.db | tail -n +4 | xargs -I {} rm -- {}

# 3. Backup Externo: Si es domingo (día 7), subir a Google Drive
if [ "$DIA_SEMANA" -eq 7 ]; then
    echo "Iniciando copia semanal externa a Google Drive..."
    # Sube el backup recién creado a una carpeta llamada 'BackupsInventario' en tu Drive
    rclone copy "$DESTINO/inventario_$FECHA.db" gdrive:BackupsInventario
fi

echo "Backup local completado. Copias actuales: $(ls -1 *.db | wc -l)"
