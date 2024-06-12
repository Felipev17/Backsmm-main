import pandas as pd
from smm.api.serializer import PagosSerializer
from smm.models import Pagos
from django.utils import timezone

def handle_file_Pagos(file):
    chunk_size = 5000
    
    for chunk in pd.read_csv(file, chunksize=chunk_size, sep=";"):
        # Convertimos las columnas para eliminar espacios adicionales
        chunk.columns = [col.strip() for col in chunk.columns]
        
        batch = []
        
        for index, row in chunk.iterrows():
            try:
                # Verifica los nombres de las columnas
                if 'CEDULA' not in row or 'Vr Recaudo Real' not in row or 'FP' not in row:
                    print(f"Columnas faltantes en la fila {index}: {row}")
                    continue
                
                # print(f"Procesando fila {index}: {row.to_dict()}")
                
                # Convertir y validar la fecha
                fecha_pago = pd.to_datetime(row['FP'], format='%d/%m/%Y', errors='coerce')
                if pd.isna(fecha_pago):
                    print(f"Fecha inválida en la fila {index}: {row['FP']}")
                    continue
                
                registro_data = {
                    'cedula': row['CEDULA'],
                    'valorRecaudo': row['Vr Recaudo Real'],
                    'fechaPago': fecha_pago,
                }
                
                serializer = PagosSerializer(data=registro_data)
                if serializer.is_valid():
                    batch.append(Pagos(**serializer.validated_data))
                else:
                    print(f"Errores de validación en la fila {index}: {serializer.errors}")
            except KeyError as e:
                print({"error": f"Falta la columna {str(e)} en la fila {index}"})

        if batch:
            Pagos.objects.bulk_create(batch)
    
    print("Carga completada")
