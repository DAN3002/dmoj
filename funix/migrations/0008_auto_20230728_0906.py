# Generated by Django 3.2.19 on 2023-07-28 09:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('judge', '0147_auto_20230612_0623'),
        ('funix', '0007_course_coursecategory_coursecomment_courseproblem_courserating_coursesection_funixprofile'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='courses', to='funix.coursecategory'),
        ),
        migrations.AlterField(
            model_name='course',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='courses', to='judge.profile', verbose_name='Author'),
        ),
    ]
