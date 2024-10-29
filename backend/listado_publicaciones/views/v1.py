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
from rest_framework.decorators import api_view
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from ..pagination import DynamicPageNumberPagination
from ..filters import PublicacionFilter
import pandas as pd
from datetime import datetime


# Create your views here.
class PublicacionViewSet(viewsets.ModelViewSet):
    queryset = Publicacion.objects.all()
    serializer_class = PublicacionSerializer
    pagination_class = DynamicPageNumberPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = PublicacionFilter
    ordering_fields = ["fecha_publicacion"]


@api_view(["GET"])
def export_to_excel(request):
    # Aplicar filtros de Django Filters a las publicaciones
    publicaciones = PublicacionFilter(
        request.GET, queryset=Publicacion.objects.all()
    ).qs

    # Crear un DataFrame para las publicaciones
    data = list(publicaciones.values())
    df_publicaciones = pd.DataFrame(data)

    if "fecha_publicacion" in df_publicaciones.columns:
        df_publicaciones["fecha_publicacion"] = pd.to_datetime(
            df_publicaciones["fecha_publicacion"]
        ).dt.tz_localize(None)

    # Obtener datos relacionados y crear DataFrames para cada relación
    categorias = Categoria.objects.all()
    departamentos = DepartamentoMunicipal.objects.all()
    juntas_vecinales = JuntaVecinal.objects.all()
    situaciones = SituacionPublicacion.objects.all()

    usuarios = Usuario.objects.all().values(
        "rut",
        "nombre",
        "email",
        "numero_telefonico_movil",
        "fecha_registro",
        "esta_activo",
    )
    df_usuarios = pd.DataFrame(list(usuarios))

    if "fecha_registro" in df_usuarios.columns:
        df_usuarios["fecha_registro"] = pd.to_datetime(
            df_usuarios["fecha_registro"]
        ).dt.tz_localize(None)

    evidencias = Evidencia.objects.all()
    df_evidencias = pd.DataFrame(evidencias.values())

    if "fecha" in df_evidencias.columns:
        df_evidencias["fecha"] = pd.to_datetime(df_evidencias["fecha"]).dt.tz_localize(
            None
        )

    df_categorias = pd.DataFrame(list(categorias.values()))
    df_juntas_vecinales = pd.DataFrame(list(juntas_vecinales.values()))
    df_situaciones = pd.DataFrame(list(situaciones.values()))
    df_departamentos = pd.DataFrame(list(departamentos.values()))
    # Generar la respuesta HTTP para la descarga
    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response["Content-Disposition"] = (
        f'attachment; filename="publicaciones_{datetime.now().strftime("%d-%m-%Y_%H:%M")}.xlsx"'
    )

    # Escribir los DataFrames en múltiples hojas de Excel
    with pd.ExcelWriter(response, engine="openpyxl") as writer:
        # Hoja principal: Publicaciones
        df_publicaciones.to_excel(writer, sheet_name="Publicaciones", index=False)

        # Hojas adicionales con relaciones
        df_usuarios.to_excel(writer, sheet_name="Usuarios", index=False)
        df_categorias.to_excel(writer, sheet_name="Categorías", index=False)
        df_departamentos.to_excel(writer, sheet_name="Departamentos", index=False)
        df_juntas_vecinales.to_excel(writer, sheet_name="Juntas Vecinales", index=False)
        df_situaciones.to_excel(writer, sheet_name="Situaciones", index=False)
        df_evidencias.to_excel(writer, sheet_name="Evidencias", index=False)

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
