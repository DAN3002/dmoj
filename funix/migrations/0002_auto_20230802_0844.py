# Generated by Django 3.2.19 on 2023-08-02 08:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('judge', '0147_auto_20230612_0623'),
        ('funix', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='courserating',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterUniqueTogether(
            name='courseproblem',
            unique_together={('problem', 'course', 'number')},
        ),
    ]
