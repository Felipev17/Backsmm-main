import pandas as pd
from smm.api.serializer import PagosSerializer
from smm.models import Pagos


def handle_file_Pagos(file):
    chunk_size = 5000
    
   

    for chunk in pd.read_csv(file, chunksize=chunk_size, sep=";"):
        
        for col in ['fechapago', 'FECHA SENCILLA']:
            try:
                chunk[col] = pd.to_datetime(chunk[col], format='%d/%m/%Y', errors='coerce')
            except pd.errors.ParserError:
                print(f"Fallo al ingresar  {col}.")
        
        chunk.replace(to_replace=pd.NA, value=None, inplace=True)
        
        batch = []
        
        for row in chunk.to_dict(orient='records'):
            try:
                
                if row['APLICACIÓN FINAL'] == 'NO APLICA':
                    continue
                
                registro_data = {
                    'Nit_cliente' : row['nitcliente'],
                    'Cod_cliente' : row['codcliente'],
                    'Numero_obligacion' : row['numobligacion'],
                    'Fecha_pago' : row['fechapago'],
                    'Valor_pago' :row[' valorpago '],
                    'Aplicacion_final' : row['APLICACIÓN FINAL'],
                    'Fecha_sencilla' : row['FECHA SENCILLA'],
                    
                }
                
                serializer = PagosSerializer(data=registro_data)
                if serializer.is_valid():
                    batch.append(Pagos(**serializer.validated_data))
                else:
                    print("Errores de validación:", serializer.errors)
            except KeyError as e:
                print({"error": f"Falta la columna {str(e)} en la fila {row}"})

        if batch:
            Pagos.objects.bulk_create(batch)
    
    print("Carga completada")   
    
    
    
    