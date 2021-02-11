from django.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from django.contrib.postgres.fields import HStoreField

values = {'water': 4,
          'food': 3,
          'medication': 2,
          'ammunition': 1}


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

    def calculated_trade_points(self, items):
        inventory_errors = []
        has_item = True
        for item in items:
            if items[item] > (getattr(self, item)):
                inventory_errors.append(
                    '{} does not have the amount of {} informed'.format(self.survivor.name, item))
                has_item = False
        return inventory_errors, has_item


class Location(models.Model):
    latitude = models.FloatField(default=0)
    longitude = models.FloatField(default=0)
    survivor = models.OneToOneField(Survivor, on_delete=models.CASCADE, null=True)


class ReportInfect(models.Model):
    survivor = models.ForeignKey(Survivor, on_delete=models.CASCADE, related_name='reports')
    motive = models.TextField()


class Trade(models.Model):
    survivor_one = models.ForeignKey(Survivor, on_delete=models.CASCADE, related_name='survivorone')
    survivor_one_items = HStoreField(blank=False)
    survivor_two = models.ForeignKey(Survivor, on_delete=models.CASCADE, related_name='survivortwo')
    survivor_two_items = HStoreField(blank=False)


@receiver(post_save, sender=ReportInfect, dispatch_uid="update_report_count")
def update_report(sender, instance, **kwargs):
    if instance.survivor.reports.all().count() > 2:
        instance.survivor.isInfected = True
        instance.survivor.save()
