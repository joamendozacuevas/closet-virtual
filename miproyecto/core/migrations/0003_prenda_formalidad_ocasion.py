# Generated manually to preserve existing inventory rows.
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('core', '0002_prenda_delete_registro'),
    ]

    operations = [
        migrations.AddField(
            model_name='prenda',
            name='formalidad_ocasion',
            field=models.IntegerField(
                default=1,
                validators=[
                    django.core.validators.MinValueValidator(1),
                    django.core.validators.MaxValueValidator(10),
                ],
            ),
            preserve_default=False,
        ),
    ]
