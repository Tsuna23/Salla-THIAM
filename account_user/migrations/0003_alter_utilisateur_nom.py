# Generated by Django 5.1.5 on 2025-03-09 18:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account_user', '0002_utilisateur_is_active_utilisateur_is_staff_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='utilisateur',
            name='nom',
            field=models.CharField(max_length=150),
        ),
    ]
