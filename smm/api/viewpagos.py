from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from smm.api.serializer import PagosSerializer
from rest_framework import status
from smm.models import Pagos
from smm.api.handle_file_pago import handle_file_Pagos


class CargarArchivoCvsView(APIView):
     parser_classes = (MultiPartParser, FormParser)
     
     def post(self, request, *args, **kwargs):
        archivo_cvs = request.FILES.get('file')
        Pagos.objects.all().delete()
        
        if not archivo_cvs:
            return Response({"error": "No se ha proporcionado ningún archivo"}, status=status.HTTP_400_BAD_REQUEST)
    
        handle_file_Pagos(archivo_cvs)
        return Response({"status": "success"}, status=status.HTTP_201_CREATED)
       

     def get(self, request):
        pago = Pagos.objects.all()
        serializer = PagosSerializer(pago, many=True)
        data = [{'Nit_cliente': item['Nit_cliente'], "Fecha_pago": item['Fecha_pago']} for item in serializer.data]
        return Response(data)
       

   