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
        dataGestion =[
            {
                'nitDeudor': item['nitDeudor'],
                'fechaGestion': item['fechaGestion'],
                'grabador': item['grabador'],
            } 
            for item in serializerGestion.data
            ]

        # Solo proceder si hay datos de gestión
        dfGestion = pd.DataFrame(dataGestion)
        dfGestion['fechaGestion'] = pd.to_datetime(dfGestion['fechaGestion'])

            # Convertir los datos de pagos a DataFrame
        dataPagos = [
            {
                'cedula': itemP['cedula'],
                'valorRecaudo': itemP['valorRecaudo'],
                'fechaPago': itemP['fechaPago'],
            }
            for itemP in serializerPagos.data
        ]

        dfPagos = pd.DataFrame(dataPagos)            
        
        dfPagos['fechaPago'] = pd.to_datetime(dfPagos['fechaPago'])

        # Realizar la unión de los DataFrames con la validación de fechas
        dfunion = pd.merge(dfGestion, dfPagos, left_on='nitDeudor', right_on='cedula', how='inner')
        print(dfunion)

        dfunion = dfunion[dfunion['fechaGestion'] <= dfunion['fechaPago']]

        dfunion = dfunion.sort_values(by='fechaGestion', ascending=False)

        # Eliminar duplicados manteniendo la última fecha de pago para cada 'fechaCompromiso'
        dfunion = dfunion.drop_duplicates(subset=['nitDeudor'], keep='first')
        
        # Crear una respuesta HTTP con el archivo CSV
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="Cruce_registro.csv"'
        
        # Exportar el DataFrame a CSV en la respuesta
        dfunion.to_csv(path_or_buf=response, index=False)
        
        return response