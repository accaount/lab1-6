# Generated by Django 4.2.1 on 2024-11-23 21:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auto', '0003_alter_auto_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auto',
            name='is_published',
            field=models.BooleanField(choices=[(0, 'Черновик'), (1, 'Опубликовано')], default=0),
        ),
        migrations.AlterField(
            model_name='auto',
            name='title',
            field=models.CharField(max_length=255),
        ),
    ]
