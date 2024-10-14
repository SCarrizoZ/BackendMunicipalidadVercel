import django_filters
from .models import Publicacion


class PublicacionFilter(django_filters.FilterSet):
    junta_vecinal = django_filters.CharFilter(
        field_name="junta_vecinal__nombre_calle", lookup_expr="icontains"
    )
    departamento = django_filters.CharFilter(
        field_name="departamento__nombre", lookup_expr="icontains"
    )
    categoria = django_filters.CharFilter(
        field_name="categoria__nombre", lookup_expr="icontains"
    )
    situacion = django_filters.CharFilter(
        field_name="situacion__nombre", lookup_expr="icontains"
    )
    fecha_publicacion = (
        django_filters.DateFromToRangeFilter()
    )  # Filtro de rango de fechas

    class Meta:
        model = Publicacion
        fields = [
            "junta_vecinal",
            "departamento",
            "categoria",
            "situacion",
            "fecha_publicacion",
        ]
