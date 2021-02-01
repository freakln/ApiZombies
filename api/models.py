from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _


class Survivor(models.Model):
    class Gender(models.TextChoices):
        MAN = 'M', _('Man')
        WOMAN = 'W', _('Woman')

    name = models.CharField(max_length=100, null=False, blank=False)
    age = models.IntegerField()
    gender = models.CharField(
        max_length=1,
        choices=Gender.choices,
    )
    isInfected = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Inventory(models.Model):
    water = models.PositiveSmallIntegerField(default=0)
    food = models.PositiveSmallIntegerField(default=0)
    medication = models.PositiveSmallIntegerField(default=0)
    ammunition = models.PositiveSmallIntegerField(default=0)
    survivor = models.OneToOneField(Survivor, on_delete=models.CASCADE, null=True)


class Location(models.Model):
    latitude = models.FloatField(default=0)
    longitude = models.FloatField(default=0)
    survivor = models.OneToOneField(Survivor, on_delete=models.CASCADE, null=True)


class ReportInfect(models.Model):
    survivor = models.ForeignKey(Survivor, on_delete=models.CASCADE, related_name='reports')
    motive = models.TextField()


@receiver(post_save, sender=ReportInfect, dispatch_uid="update_report_count")
def update_report(sender, instance, **kwargs):
    if instance.survivor.reports.all().count() > 2:
        instance.survivor.isInfected = True
        instance.survivor.save()
