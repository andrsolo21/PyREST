from django.db import models

# Create your models here.

class Person(models.Model):

    class Meta:
        unique_together = (('import_id', 'citizen_id'),)

    #person_id = models.AutoField(primary_key=True)
    import_id = models.ForeignKey('Imp', on_delete='CASCADE')
    citizen_id = models.IntegerField()
    town = models.CharField(max_length=50)
    street = models.CharField(max_length=50)
    building = models.CharField(max_length=50)
    appartement = models.IntegerField()
    name = models.CharField(max_length=50)
    birth_date = models.DateField()
    gender = models.CharField(max_length=10)
    #relatives = models.TextField()

class Relatives(models.Model):
    class Meta:
        unique_together = (('import_id', 'citizen_id', 'relative_id'),)

    import_id =  models.ForeignKey('Imp', on_delete='CASCADE')
    citizen_id = models.IntegerField()
    relative_id = models.IntegerField()
    person_id = models.ForeignKey('Person', on_delete = 'CASCADE')


class Imp(models.Model):
    import_id = models.AutoField(primary_key=True)
    num = models.IntegerField()
    #deleted_at =