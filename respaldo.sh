#!/bin/bash

fecha=`date +%F`

#cd /home/ceic/SistemaVentas/sistema-ventas-ceic/
python manage.py dumpdata > $fecha.json
