import pandas as pd
from smm.models import Gestion
from smm.api.serializer import GestionSerializer

def handle_file(file):
    chunk_size = 5000
    registros = []
    compared_id_gestion = set()
    resultados_invalidos = {"No contestan", "Mensaje con terceros", "Nro. inhabilitado", "Conmutador", "Equivocado", "Fallecido", "Ocupado", "Caso Especial", "Entrega Comunicado", "No Localizado", "Nuevos Datos"}
    
   
    
    for chunk in pd.read_csv(file, chunksize=chunk_size, sep=';'):
        batch = []
        chunk['Fecha gestión'] = pd.to_datetime(chunk['Fecha gestión'], format='%d/%m/%Y %H:%M', errors='coerce')
        chunk['Fecha Compromiso'] = pd.to_datetime(chunk['Fecha Compromiso'], format='%d/%m/%Y %H:%M', errors='coerce')
        for row in chunk.to_dict(orient='records'):
            try:
                if row['Resultado'] in resultados_invalidos:
                    continue
                
                fecha_compromiso = row['Fecha Compromiso'] if not pd.isna(row['Fecha Compromiso']) else None
                
                if row["Código gestión"] in compared_id_gestion:
                    continue
                compared_id_gestion.add(row["Código gestión"])
                
                registro_data = {
                    'Id_gestion_campaña': row['Id Gestion Campaña'],
                    'Tipo_documento': row['Tipo documento'],
                    'Numero_documento': row['Número documento'],
                    'Nombre': row['Nombre'],
                    'Fecha_gestion': row['Fecha gestión'],
                    'Tipo_llamada': row['Tipo llamada'],
                    'Codigo_gestion': row['Código gestión'],
                    'Resultado': row['Resultado'],
                    'Fecha_compromiso': fecha_compromiso ,
                    'Nombre_asesor': row['Nombre Asesor'],
                    'Campaña': row['Campaña'],
                    'Telefono': row['Teléfono'],
                    'Obligacion': row['Obligación'],
                    'Nro_comparendo': row['Nro. Comparendo'],
                    'Valor': row['Valor'],
                }
                
                serializer = GestionSerializer(data=registro_data)
                if serializer.is_valid():
                    batch.append(Gestion(**serializer.validated_data))
                else:
                    print("Errores de validación:", serializer.errors)
            except KeyError as e:
                print({"error": f"Falta la columna {str(e)} en la fila {row}"})

        if batch:
            Gestion.objects.bulk_create(batch)
    
    print("Carga completada")
