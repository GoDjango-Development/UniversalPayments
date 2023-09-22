# Generated by Django 4.2.2 on 2023-09-22 08:43

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documentation', '0002_squaresdocumentation'),
    ]

    operations = [
        migrations.CreateModel(
            name='BankOfAmericaDocumentation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('documentation', ckeditor.fields.RichTextField(verbose_name='Documentación')),
            ],
            options={
                'verbose_name': 'Documentación',
                'verbose_name_plural': 'Documentación',
                'db_table': 'bankofamerica_documentation',
                'permissions': (('add_bankofamericadocumentation', 'Adicionar documentación de Bank of America'), ('change_bankofamericadocumentation', 'Editar documentación de Bank of America'), ('view_bankofamericadocumentation', 'Ver documentación de Bank of America'), ('delete_bankofamericadocumentation', 'Eliminar documentación de Bank of America')),
                'default_permissions': [],
            },
        ),
    ]
