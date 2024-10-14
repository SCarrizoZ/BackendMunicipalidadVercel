from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views.v1 import (
    PublicacionViewSet,
    UsuariosViewSet,
    CategoriasViewSet,
    DepartamentosMunicipalesViewSet,
    EvidenciasViewSet,
    JuntasVecinalesViewSet,
    RespuestasMunicipalesViewSet,
    SituacionesPublicacionesViewSet,
)
from .views.v1 import export_to_excel

router = DefaultRouter()
router.register(r"publicaciones", PublicacionViewSet, basename="publicaciones")
router.register(r"usuarios", UsuariosViewSet, basename="usuarios")
router.register(r"categorias", CategoriasViewSet, basename="categorias")
router.register(
    r"departamentos-municipales",
    DepartamentosMunicipalesViewSet,
    basename="departamentos-municipales",
)
router.register(r"evidencias", EvidenciasViewSet, basename="evidencias")
router.register(
    r"juntas-vecinales", JuntasVecinalesViewSet, basename="juntas-vecinales"
)
router.register(
    r"respuestas-municipales",
    RespuestasMunicipalesViewSet,
    basename="respuestas-municipales",
)
router.register(
    r"situaciones-publicaciones",
    SituacionesPublicacionesViewSet,
    basename="situaciones-publicaciones",
)

urlpatterns = [
    path("v1/", include(router.urls)),
    path("export-to-excel/", export_to_excel),
]
