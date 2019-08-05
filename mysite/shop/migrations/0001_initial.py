# Generated by Django 2.2.3 on 2019-08-01 17:33

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Imp',
            fields=[
                ('import_id', models.AutoField(primary_key=True, serialize=False)),
                ('num', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Relatives',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('citizen_id', models.IntegerField()),
                ('relative_id', models.IntegerField()),
                ('import_id', models.ForeignKey(on_delete='CASCADE', to='shop.Imp')),
            ],
            options={
                'unique_together': {('import_id', 'citizen_id', 'relative_id')},
            },
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('citizen_id', models.IntegerField()),
                ('town', models.CharField(max_length=50)),
                ('street', models.CharField(max_length=50)),
                ('building', models.CharField(max_length=50)),
                ('appartement', models.IntegerField()),
                ('name', models.CharField(max_length=50)),
                ('birth_date', models.DateField()),
                ('gender', models.CharField(max_length=10)),
                ('import_id', models.ForeignKey(on_delete='CASCADE', to='shop.Imp')),
            ],
            options={
                'unique_together': {('import_id', 'citizen_id')},
            },
        ),
    ]