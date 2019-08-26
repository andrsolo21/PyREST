from django.db import models
import datetime
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

    def as_json(self, relatives):

        """
        :param relatives: list of person relatives
        :return: fields in dictionary for JSON
        """

        return dict(
            #import_id = self.import_id.import_id,
            citizen_id = self.citizen_id,
            town = self.town,
            street = self.street,
            building = self.building,
            apartement = self.appartement,
            name = self.name,
            birth_day = self.birth_date,
            gender = self.gender,
            relatives = list(relatives),
        )

    def getAge(self, today = datetime.date.today()):

        """
        function calculate age of person
        :param today: today's date
        :return: age
        """

        return today.year - self.birth_date.year - ((today.month, today.day) < (self.birth_date.month, self.birth_date.day))




    def isError(self):

        """
        It is not error, there fore
        :return: FALSE
        """

        return False



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

    def isError(self):

        """
        It is not error too, there fore
        :return: FALSE
        """

        return False