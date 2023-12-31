# Generated by Django 4.2.6 on 2023-12-07 20:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('story', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ingredient',
            options={'ordering': ('name',)},
        ),
        migrations.AddField(
            model_name='ingredient',
            name='unit',
            field=models.PositiveSmallIntegerField(choices=[(1, 'ml'), (2, 'g')], default=1),
        ),
    ]
