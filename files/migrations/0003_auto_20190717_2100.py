# Generated by Django 2.2.3 on 2019-07-17 21:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('files', '0002_document_file_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='uploaded_at',
            field=models.DateTimeField(),
        ),
    ]
