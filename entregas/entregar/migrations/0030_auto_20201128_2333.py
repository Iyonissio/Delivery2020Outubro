# Generated by Django 3.0.7 on 2020-11-29 07:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('entregar', '0029_funcionarios_cargo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='funcionarios',
            name='contacto',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
