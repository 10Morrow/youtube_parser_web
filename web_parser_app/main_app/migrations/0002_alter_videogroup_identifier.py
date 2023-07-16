# Generated by Django 4.2.2 on 2023-07-14 15:31

from django.db import migrations, models
import main_app.models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='videogroup',
            name='identifier',
            field=models.CharField(default=main_app.models.generate_unique_identifier, max_length=7, unique=True),
        ),
    ]
