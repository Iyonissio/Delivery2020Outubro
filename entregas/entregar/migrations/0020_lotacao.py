# Generated by Django 3.0.7 on 2020-10-21 05:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('entregar', '0019_auto_20201019_1635'),
    ]

    operations = [
        migrations.CreateModel(
            name='Lotacao',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero_de_clientes', models.TextField(blank=True, max_length=5000, null=True)),
            ],
        ),
    ]
