# Generated by Django 4.1.2 on 2023-01-11 19:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_alter_containers_id_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='container',
            old_name='author',
            new_name='student',
        ),
        migrations.RenameField(
            model_name='containers_id',
            old_name='name',
            new_name='cid',
        ),
    ]
