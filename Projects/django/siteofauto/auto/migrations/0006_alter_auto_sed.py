# Generated by Django 4.2.1 on 2024-11-24 09:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auto', '0005_category_auto_sed'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auto',
            name='sed',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='auto.category'),
        ),
    ]
