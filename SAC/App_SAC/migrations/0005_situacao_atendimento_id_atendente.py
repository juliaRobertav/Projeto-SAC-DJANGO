# Generated by Django 4.2.4 on 2023-10-06 19:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('App_SAC', '0004_atendimento_situacao_atendimento'),
    ]

    operations = [
        migrations.AddField(
            model_name='situacao_atendimento',
            name='id_atendente',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='App_SAC.atendente'),
        ),
    ]