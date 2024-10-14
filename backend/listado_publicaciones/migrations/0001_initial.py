# Generated by Django 5.1.1 on 2024-10-14 03:06

import cloudinary.models
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DepartamentoMunicipal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('descripcion', models.CharField(blank=True, max_length=300, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='JuntaVecinal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_calle', models.CharField(max_length=60)),
                ('numero_calle', models.IntegerField()),
                ('departamento', models.CharField(blank=True, max_length=40, null=True)),
                ('villa', models.CharField(blank=True, max_length=40, null=True)),
                ('comuna', models.CharField(blank=True, max_length=40, null=True)),
                ('latitud', models.DecimalField(decimal_places=6, max_digits=9)),
                ('longitud', models.DecimalField(decimal_places=6, max_digits=9)),
            ],
        ),
        migrations.CreateModel(
            name='SituacionPublicacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('descripcion', models.CharField(blank=True, max_length=300, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('rut', models.CharField(max_length=12, primary_key=True, serialize=False)),
                ('numero_telefonico_movil', models.CharField(blank=True, max_length=9, null=True)),
                ('nombre', models.CharField(max_length=120)),
                ('contrasena', models.CharField(max_length=30)),
                ('es_administrador', models.BooleanField()),
                ('email', models.EmailField(max_length=200)),
                ('fecha_registro', models.DateTimeField()),
                ('esta_activo', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=80)),
                ('descripcion', models.CharField(blank=True, max_length=300, null=True)),
                ('departamento', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='listado_publicaciones.departamentomunicipal')),
            ],
        ),
        migrations.CreateModel(
            name='Publicacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcion', models.TextField()),
                ('fecha_publicacion', models.DateTimeField()),
                ('titulo', models.CharField(max_length=100)),
                ('latitud', models.DecimalField(decimal_places=6, max_digits=9)),
                ('longitud', models.DecimalField(decimal_places=6, max_digits=9)),
                ('categoria', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='listado_publicaciones.categoria')),
                ('departamento', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='listado_publicaciones.departamentomunicipal')),
                ('junta_vecinal', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='listado_publicaciones.juntavecinal')),
                ('situacion', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, to='listado_publicaciones.situacionpublicacion')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='listado_publicaciones.usuario')),
            ],
        ),
        migrations.CreateModel(
            name='Evidencia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('archivo', cloudinary.models.CloudinaryField(max_length=255, verbose_name='archivo')),
                ('fecha', models.DateTimeField()),
                ('extension', models.CharField(max_length=30)),
                ('publicacion', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='listado_publicaciones.publicacion')),
            ],
        ),
        migrations.CreateModel(
            name='RespuestaMunicipal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateTimeField()),
                ('descripcion', models.TextField()),
                ('acciones', models.CharField(max_length=400)),
                ('situacion_inicial', models.CharField(max_length=100)),
                ('situacion_posterior', models.CharField(max_length=100)),
                ('publicacion', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='listado_publicaciones.publicacion')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='listado_publicaciones.usuario')),
            ],
        ),
        migrations.CreateModel(
            name='AnuncioMunicipal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=100)),
                ('descripcion', models.TextField()),
                ('fecha', models.DateTimeField()),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='listado_publicaciones.usuario')),
            ],
        ),
    ]
