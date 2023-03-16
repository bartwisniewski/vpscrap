from django.db import models
from django.utils.translation import gettext_lazy as _


# class Job(models.Model):
#     class JobStatus(models.IntegerChoices):
#         INCOMING = 0, _("Incoming")
#         RUNNING = 1, _("Running")
#         COMPLETE = 2, _("Complete")
#         SENT = 3, _("Sent")
#
#     status = models.IntegerField(
#         choices=JobStatus.choices, default=JobStatus.INCOMING
#     )
#
#
# class Query:
#     job = models.OneToOneField(on_delete=models.CASCADE)
#     place = models.CharField(max_length=30)
#     adults = models.IntegerField(default=1)
#     children = models.IntegerField(default=0)
#     infants = models.IntegerField(default=0)
#     start_date = models.DateTimeField()
#     end_date = models.DateTimeField()
#
#
# class Place(models.Model):
#     job = models.ForeignKey(on_delete=models.CASCADE)
#     name = models.CharField(max_length=30)
#     url = models.URLField()
#     description = models.TextField()
#     address = models.CharField(max_length=255)
#     city = models.CharField(max_length=100)
#     country = models.CharField(max_length=30)
#     region = models.CharField(max_length=100)
#     place_type = models.CharField(max_length=100)
#     owner_name = models.CharField(max_length=30)
#     owner_phone = models.CharField(max_length=20)
#     owner_email = models.EmailField()
#     adults = models.IntegerField(default=1)
#     children = models.IntegerField(default=0)
#     infants = models.IntegerField(default=0)
#     bedrooms = models.IntegerField(default=1)
#     bathrooms = models.IntegerField(default=1)
#     living_rooms = models.IntegerField(default=0)
#     kitchens = models.IntegerField(default=0)
#     price = models.FloatField(default=0.0)
