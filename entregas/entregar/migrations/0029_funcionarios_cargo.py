# Generated by Django 3.0.7 on 2020-10-30 07:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('entregar', '0028_funcionarios'),
    ]

    operations = [
        migrations.AddField(
            model_name='funcionarios',
            name='cargo',
            field=models.CharField(max_length=200, null=True),
        ),
    ]