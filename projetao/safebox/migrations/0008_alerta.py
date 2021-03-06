# Generated by Django 4.0.3 on 2022-05-05 01:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('safebox', '0007_alter_camera_ip_boundingbox'),
    ]

    operations = [
        migrations.CreateModel(
            name='Alerta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.DateField()),
                ('hora', models.TimeField()),
                ('tipo', models.TextField()),
                ('bounding_box_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='safebox.boundingbox')),
            ],
        ),
    ]
