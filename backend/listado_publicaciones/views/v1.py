from ..models import (
    Publicacion,
    Usuario,
    Categoria,
    DepartamentoMunicipal,
    Evidencia,
    JuntaVecinal,
    RespuestaMunicipal,
    SituacionPublicacion,
)
from ..serializers.v1 import (
    PublicacionSerializer,
    UsuarioSerializer,
    CategoriaSerializer,
    DepartamentoMunicipalSerializer,
    EvidenciaSerializer,
    JuntaVecinalSerializer,
    RespuestaMunicipalSerializer,
    SituacionPublicacionSerializer,
)
from rest_framework import viewsets
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from ..pagination import DynamicPageNumberPagination
from ..filters import PublicacionFilter
import pandas as pd


# Create your views here.
class PublicacionViewSet(viewsets.ModelViewSet):
    queryset = Publicacion.objects.all()
    serializer_class = PublicacionSerializer
    pagination_class = DynamicPageNumberPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = PublicacionFilter
    ordering_fields = ["fecha_publicacion"]


def export_to_excel(request):
    # Usa Django Filters para obtener los filtros
    publicaciones = PublicacionFilter(
        request.GET, queryset=Publicacion.objects.all()
    ).qs

    # Crear un DataFrame con los datos filtrados
    data = list(
        publicaciones.values()
    )  # Puedes especificar los campos que deseas incluir
    df = pd.DataFrame(data)

    if "fecha_publicacion" in df.columns:
        df["fecha_publicacion"] = pd.to_datetime(df["fecha_publicacion"])
        df["fecha_publicacion"] = df["fecha_publicacion"].dt.strftime("%d-%m-%Y %H:%M")

    # Generar el archivo Excel
    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response["Content-Disposition"] = 'attachment; filename="publicaciones.xlsx"'

    # Guardar el DataFrame como un archivo Excel
    df.to_excel(response, index=False)

    return response


class UsuariosViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer


class CategoriasViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer


class DepartamentosMunicipalesViewSet(viewsets.ModelViewSet):
    queryset = DepartamentoMunicipal.objects.all()
    serializer_class = DepartamentoMunicipalSerializer


class EvidenciasViewSet(viewsets.ModelViewSet):
    queryset = Evidencia.objects.all()
    serializer_class = EvidenciaSerializer


class JuntasVecinalesViewSet(viewsets.ModelViewSet):
    queryset = JuntaVecinal.objects.all()
    serializer_class = JuntaVecinalSerializer


class RespuestasMunicipalesViewSet(viewsets.ModelViewSet):
    queryset = RespuestaMunicipal.objects.all()
    serializer_class = RespuestaMunicipalSerializer


class SituacionesPublicacionesViewSet(viewsets.ModelViewSet):
    queryset = SituacionPublicacion.objects.all()
    serializer_class = SituacionPublicacionSerializer
