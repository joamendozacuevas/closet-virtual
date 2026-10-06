import uuid

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Prenda',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=120)),
                ('color', models.CharField(max_length=80)),
                ('estado_limpieza', models.CharField(choices=[('limpio', 'Limpio'), ('sucio', 'Sucio')], max_length=10)),
                ('formalidad_prenda', models.PositiveSmallIntegerField()),
                ('formalidad_ocasion', models.PositiveSmallIntegerField()),
                ('resultado', models.CharField(editable=False, max_length=160)),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
            ],
            options={'ordering': ['-fecha_creacion']},
        ),
    ]
