from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from smm.api.serializer import GestionSerializer
from smm.api.serializer import PagosSerializer
from rest_framework import status
from smm.models import Gestion
from smm.models import Pagos
from smm.api.handle_file_gestion import handle_file


class CargarArchivoExcelView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    def post(self, request, *args, **kwargs):
        archivo_excel = request.FILES.get('file')
        Gestion.objects.all().delete()  
            
        if not archivo_excel:
            return Response({"error": "No se ha proporcionado ningún archivo"}, status=status.HTTP_400_BAD_REQUEST)
       
        handle_file(archivo_excel)
        return Response({"status": "success"}, status=status.HTTP_201_CREATED)
    

    def get(self, request):
        Gestions = Gestion.objects.all()
        serializer = GestionSerializer(Gestions, many=True)
        data = [{'Id_gestion_campaña': item['Id_gestion_campaña'],'Nombre' : item['Nombre']}for item in serializer.data]
        return Response(data)
    
    


    