# Generated by Django 4.2.6 on 2023-10-12 15:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('copysite', '0005_alter_author_born'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='born',
            field=models.CharField(max_length=30),
        ),
    ]
