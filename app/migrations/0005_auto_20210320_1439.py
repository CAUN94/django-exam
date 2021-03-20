# Generated by Django 2.2.4 on 2021-03-20 14:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_remove_like_like'),
    ]

    operations = [
        migrations.AlterField(
            model_name='like',
            name='thought',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='Like', to='app.Thought'),
        ),
        migrations.AlterField(
            model_name='like',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Like', to='app.User'),
        ),
    ]