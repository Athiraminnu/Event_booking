from django.db import models


# Create your models here.
class Users(models.Model):
    name = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    role = models.CharField(max_length=10)

    def __str__(self):
        return {self.name}


class Events(models.Model):
    title = models.CharField(max_length=30)
    location = models.CharField(max_length=30)
    date = models.DateField()
    total_seats = models.IntegerField()
    available_seats = models.IntegerField()

    def __str__(self):
        return {self.title}


class Bookings(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    event = models.ForeignKey(Events, on_delete=models.CASCADE)
    seats_booked = models.IntegerField()
    status = models.CharField(max_length=15)


    def __str__(self):
        return f"{self.user.name} booked {self.event.title}"
