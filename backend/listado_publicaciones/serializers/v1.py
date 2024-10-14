from rest_framework import serializers
from ..models import (
    Usuario,
    Categoria,
    DepartamentoMunicipal,
    Evidencia,
    JuntaVecinal,
    Publicacion,
    RespuestaMunicipal,
    SituacionPublicacion,
)
import cloudinary


# Serializer para Usuario
class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = [
            "rut",
            "numero_telefonico_movil",
            "nombre",
            "es_administrador",
            "email",
            "fecha_registro",
            "esta_activo",
        ]


# Serializer para Departamento Municipal
class DepartamentoMunicipalSerializer(serializers.ModelSerializer):
    class Meta:
        model = DepartamentoMunicipal
        fields = ["id", "nombre", "descripcion"]


# Serializer para Categoria
class CategoriaSerializer(serializers.ModelSerializer):
    departamento = DepartamentoMunicipalSerializer()

    class Meta:
        model = Categoria
        fields = ["id", "departamento", "nombre", "descripcion"]


# Serializer para Junta Vecinal
class JuntaVecinalSerializer(serializers.ModelSerializer):
    class Meta:
        model = JuntaVecinal
        fields = [
            "id",
            "nombre_calle",
            "numero_calle",
            "departamento",
            "villa",
            "comuna",
            "latitud",
            "longitud",
        ]


# Serializer para Situacion de Publicacion
class SituacionPublicacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SituacionPublicacion
        fields = ["id", "nombre", "descripcion"]


# Serializer para Evidencia
class EvidenciaSerializer(serializers.ModelSerializer):
    publicacion_id = serializers.PrimaryKeyRelatedField(
        queryset=Publicacion.objects.all()
    )

    class Meta:
        model = Evidencia
        fields = [
            "id",
            "publicacion",
            "archivo",
            "fecha",
            "extension",
            "publicacion_id",
        ]

    def create(self, validated_data):
        archivo = validated_data.pop("archivo")
        upload_data = cloudinary.uploader.upload(archivo)
        validated_data["archivo"] = upload_data["url"]
        return Evidencia.objects.create(**validated_data)


# Serializer para Publicacion
class PublicacionSerializer(serializers.ModelSerializer):
    usuario = UsuarioSerializer()
    junta_vecinal = JuntaVecinalSerializer()
    categoria = CategoriaSerializer()
    departamento = DepartamentoMunicipalSerializer()
    situacion = SituacionPublicacionSerializer()
    evidencias = EvidenciaSerializer(many=True, read_only=True, source="evidencia_set")

    class Meta:
        model = Publicacion
        fields = [
            "id",
            "usuario",
            "junta_vecinal",
            "categoria",
            "departamento",
            "descripcion",
            "situacion",
            "fecha_publicacion",
            "titulo",
            "latitud",
            "longitud",
            "evidencias",
        ]


# Serializer para Respuesta Municipal
class RespuestaMunicipalSerializer(serializers.ModelSerializer):
    usuario = UsuarioSerializer()
    publicacion = PublicacionSerializer()

    class Meta:
        model = RespuestaMunicipal
        fields = [
            "id",
            "usuario",
            "publicacion",
            "fecha",
            "descripcion",
            "acciones",
            "situacion_inicial",
            "situacion_posterior",
        ]
