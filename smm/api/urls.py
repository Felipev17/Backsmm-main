from django.urls import path
from smm.api.viewgestion import CargarArchivoExcelView
from smm.api.viewpagos import CargarArchivoCvsView
from smm.api.cruzararchivos import DescargarCsv

urlpatterns = [
    path('cargar-archivo-excel/', CargarArchivoExcelView.as_view(), name='cargar-archivo-excel'),
    path('cargar-pagos/', CargarArchivoCvsView.as_view(), name='cargar-pagos'),
    path('descargar-csv', DescargarCsv.as_view(), name='descargar-cvs')
]
