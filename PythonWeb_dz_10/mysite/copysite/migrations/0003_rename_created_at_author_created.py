# Generated by Django 4.2.6 on 2023-10-07 20:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('copysite', '0002_alter_author_location_alter_tag_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='author',
            old_name='created_at',
            new_name='created',
        ),
    ]