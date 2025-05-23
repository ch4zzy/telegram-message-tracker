# Generated by Django 5.1.2 on 2024-11-30 17:57

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0002_targetchannel_sourcechannel_post'),
    ]

    operations = [
        migrations.AddField(
            model_name='targetchannel',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='target_channels', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='sourcechannel',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='source_channels', to=settings.AUTH_USER_MODEL),
        ),
    ]
