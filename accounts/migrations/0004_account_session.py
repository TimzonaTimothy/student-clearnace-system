# Generated by Django 3.2 on 2023-10-11 14:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_session'),
        ('accounts', '0003_account_matric_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='session',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main.session'),
        ),
    ]