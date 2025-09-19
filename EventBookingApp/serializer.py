from rest_framework import serializers
from EventBookingApp.models import Users, Events, Bookings


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['name', 'email', 'password', 'role']
        extra_kwargs = {'password': {'write_only': True}}


class EventsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Events
        fields = ['title', 'location', 'date', 'total_seats', 'available_seats']


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bookings
        fields = ['user', 'event', 'seats_booked', 'status']