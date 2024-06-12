import pandas as pd
from django.http import HttpResponse
from smm.api.serializer import PagosSerializer, GestionSerializer
from smm.models import Pagos, Gestion
from rest_framework.views import APIView

class DescargarCsv(APIView):
    def get(self, request):
        # Obtén todos los datos de Gestion y Pagos
        Gestions = Gestion.objects.all()
        Pago = Pagos.objects.all()
        
        # Serializa los datos
        serializerGestion = GestionSerializer(Gestions, many=True)
        serializerPagos = PagosSerializer(Pago, many=True)
        
        # Convierte los datos serializados a listas de diccionarios
        dataGestion = [
            {
                'Codigo_Gestión': item['Codigo_gestion'],
                'Nombre_Asesor': item['Nombre_asesor'],
                'Numero_documento': item['Numero_documento'],
                'Fecha_gestion': item['Fecha_gestion'],
                'Resultado': item['Resultado']
            } 
            for item in serializerGestion.data
        ]

        # Solo proceder si hay datos de gestión
        if dataGestion:
            dfGestion = pd.DataFrame(dataGestion)
            dfGestion['Fecha_gestion'] = pd.to_datetime(dfGestion['Fecha_gestion'])

            # Extraer el mes de la primera fecha de gestión
            mes_inicial = dfGestion['Fecha_gestion'].iloc[0].month

            # Convertir los datos de pagos a DataFrame
            dataPagos = [
                {
                    'Cedula': itemP['Nit_cliente'],
                    'Fecha_pago': itemP['Fecha_pago'],
                    'Valor_pago': itemP['Valor_pago'],
                }
                for itemP in serializerPagos.data
            ]
            dfPagos = pd.DataFrame(dataPagos)
            dfPagos['Fecha_pago'] = pd.to_datetime(dfPagos['Fecha_pago'])

            # Filtrar los pagos que coinciden con el mes de la fecha de gestión inicial
            dfPagos = dfPagos[dfPagos['Fecha_pago'].dt.month == mes_inicial]

            # Realizar la unión de los DataFrames con la validación de fechas
            dfJuntada = pd.merge(dfGestion, dfPagos, left_on='Numero_documento', right_on='Cedula', how='inner')
            dfJuntada = dfJuntada[dfJuntada['Fecha_pago'] >= dfJuntada['Fecha_gestion']]
        
        else:
            dfJuntada = pd.DataFrame()

        # Crear una respuesta HTTP con el archivo CSV
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="Cruce_registro.csv"'
        
        # Exportar el DataFrame a CSV en la respuesta
        dfJuntada.to_csv(path_or_buf=response, index=False)
        
        return response