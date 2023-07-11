# Generated by Django 3.2.19 on 2023-07-10 16:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('judge', '0147_auto_20230612_0623'),
        ('funix', '0004_probleminitialsource'),
    ]

    operations = [
        migrations.AddField(
            model_name='probleminitialsource',
            name='language',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='initial_codes', to='judge.language', verbose_name='Initial Source Language'),
        ),
        migrations.AlterField(
            model_name='probleminitialsource',
            name='problem',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='initial_codes', to='judge.problem'),
        ),
        migrations.AlterField(
            model_name='probleminitialsource',
            name='source',
            field=models.TextField(blank=True, default='', max_length=65536, verbose_name='Problem Initial Source'),
        ),
    ]
