# Generated by Django 2.0.4 on 2018-09-01 07:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gs_schdl', '0002_member_team'),
    ]

    operations = [
        migrations.CreateModel(
            name='RhPlan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sort_key', models.IntegerField(default=1, verbose_name='Sort key')),
                ('datetime', models.CharField(max_length=255, verbose_name='Datetime string')),
                ('plan', models.TextField(blank=True, verbose_name='Plan')),
                ('log', models.TextField(blank=True, verbose_name='Log')),
                ('prod_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gs_schdl.Production')),
            ],
        ),
        migrations.AlterField(
            model_name='member',
            name='name',
            field=models.CharField(max_length=255, verbose_name='Name of member'),
        ),
        migrations.AlterField(
            model_name='member',
            name='prod_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gs_schdl.Production'),
        ),
        migrations.AlterField(
            model_name='team',
            name='name',
            field=models.CharField(max_length=255, verbose_name='Name of team'),
        ),
        migrations.AlterField(
            model_name='team',
            name='prod_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gs_schdl.Production'),
        ),
    ]