# Generated by Django 3.2 on 2023-10-12 05:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_auto_20231011_1658'),
    ]

    operations = [
        migrations.AddField(
            model_name='userhistory',
            name='service',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
    ]
