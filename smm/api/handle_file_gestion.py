import pandas as pd
from smm.models import Gestion
from smm.api.serializer import GestionSerializer

def handle_file(file):
    chunk_size = 5000
    for chunk in pd.read_csv(file, chunksize=chunk_size, sep=';'):
        batch = []
        # chunk['Fecha Compromiso'] = pd.to_datetime(chunk['Fecha Compromiso'], format='%Y/%m/%d', errors='coerce')
        for row in chunk.to_dict(orient='records'):
            try:
                fecha_compromiso = row['Fecha Compromiso']      
                # if pd.isna(row['Fecha Compromiso']) else None
                registro_data = { 
                    'consecutivoObligacion': row['Consecutivo obligación'],
                    'nitDeudor': row['Nit Deudor'],
                    'fechaCompromiso': fecha_compromiso,
                    'estado': row['Estado'],
                    'descripcionCodigoCobro': row['Descripcion Codigo Cobro'],
                    'grabador': row['Grabador'],
                    'valorPactado': row['Valor Pactado'],
                }
                # print(registro_data)
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
