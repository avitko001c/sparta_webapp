# Generated by Django 2.0.6 on 2018-07-23 23:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Avatar',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, height_field='height', null=True, upload_to='media/avatars/', verbose_name='image', width_field='width')),
                ('height', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='height')),
                ('width', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='width')),
            ],
            options={
                'verbose_name': 'avatar',
                'verbose_name_plural': 'avatars',
            },
        ),
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.ForeignKey(help_text='Set the role for the user', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='role', to='users.Role'),
        ),
        migrations.AddField(
            model_name='user',
            name='avatar',
            field=models.ForeignKey(help_text='Users Avatar to use on site', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='avatar', to='users.Avatar', verbose_name='avatar'),
        ),
    ]