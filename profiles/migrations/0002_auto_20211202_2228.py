# Generated by Django 3.2.8 on 2021-12-03 01:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='cpf',
            field=models.CharField(max_length=11, verbose_name='cpf'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='date',
            field=models.DateField(verbose_name='Nascimento'),
        ),
    ]
