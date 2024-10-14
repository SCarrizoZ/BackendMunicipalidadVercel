from django.db import models
from cloudinary.models import CloudinaryField


# Create your models here.
class Usuario(models.Model):
    rut = models.CharField(max_length=12, primary_key=True)
    numero_telefonico_movil = models.CharField(max_length=9, null=True, blank=True)
    nombre = models.CharField(max_length=120)
    contrasena = models.CharField(max_length=30)
    es_administrador = models.BooleanField()
    email = models.EmailField(max_length=200)
    fecha_registro = models.DateTimeField()
    esta_activo = models.BooleanField()

    def __str__(self):
        return self.nombre


class DepartamentoMunicipal(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=300, null=True, blank=True)

    def __str__(self):
        return self.nombre


class Categoria(models.Model):
    departamento = models.ForeignKey(DepartamentoMunicipal, on_delete=models.RESTRICT)
    nombre = models.CharField(max_length=80)
    descripcion = models.CharField(max_length=300, null=True, blank=True)

    def __str__(self):
        return self.nombre


class SituacionPublicacion(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=300, null=True, blank=True)

    def __str__(self):
        return self.nombre


class JuntaVecinal(models.Model):
    nombre_calle = models.CharField(max_length=60)
    numero_calle = models.IntegerField()
    departamento = models.CharField(max_length=40, null=True, blank=True)
    villa = models.CharField(max_length=40, null=True, blank=True)
    comuna = models.CharField(max_length=40, null=True, blank=True)
    latitud = models.DecimalField(max_digits=9, decimal_places=6)
    longitud = models.DecimalField(max_digits=9, decimal_places=6)

    def __str__(self):
        return f"{self.nombre_calle} {self.numero_calle}"


class Publicacion(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.RESTRICT)
    junta_vecinal = models.ForeignKey(JuntaVecinal, on_delete=models.RESTRICT)
    categoria = models.ForeignKey(Categoria, on_delete=models.RESTRICT)
    situacion = models.ForeignKey(
        SituacionPublicacion, on_delete=models.RESTRICT, null=True, blank=True
    )
    departamento = models.ForeignKey(DepartamentoMunicipal, on_delete=models.RESTRICT)
    descripcion = models.TextField()
    fecha_publicacion = models.DateTimeField()
    titulo = models.CharField(max_length=100)
    latitud = models.DecimalField(max_digits=9, decimal_places=6)
    longitud = models.DecimalField(max_digits=9, decimal_places=6)

    def __str__(self):
        return self.titulo


class Evidencia(models.Model):
    publicacion = models.ForeignKey(Publicacion, on_delete=models.RESTRICT)
    archivo = CloudinaryField("archivo")
    fecha = models.DateTimeField()
    extension = models.CharField(max_length=30)

    def __str__(self):
        return f"Evidencia para: {self.publicacion.titulo}"


class AnuncioMunicipal(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.RESTRICT)
    titulo = models.CharField(max_length=100)
    descripcion = models.TextField()
    fecha = models.DateTimeField()

    def __str__(self):
        return self.titulo


class RespuestaMunicipal(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.RESTRICT)
    publicacion = models.ForeignKey(Publicacion, on_delete=models.RESTRICT)
    fecha = models.DateTimeField()
    descripcion = models.TextField()
    acciones = models.CharField(max_length=400)
    situacion_inicial = models.CharField(max_length=100)
    situacion_posterior = models.CharField(max_length=100)

    def __str__(self):
        return f"Respuesta para: {self.publicacion.titulo}"
