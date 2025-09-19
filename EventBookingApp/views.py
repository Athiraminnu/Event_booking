from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password, check_password
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from EventBookingApp.models import Users, Events, Bookings
from rest_framework_simplejwt.tokens import RefreshToken
from EventBookingApp.serializer import EventsSerializer, BookingSerializer


# Create your views here.
@api_view(['GET'])
def home(request):
    return Response({"message": "API is running"})


@api_view(['POST'])
def user_registration(request):
    data = request.data
    required_fields = ["name", "email", "password"]

    for field in required_fields:
        if field not in data or not data[field]:
            return Response({"error": f"{field} is required"}, status=status.HTTP_400_BAD_REQUEST)

    name = data["name"]
    email = data["email"]
    password = data["password"]
    role = data.get("role", "customer")  # default to customer if not provided

    if Users.objects.filter(email=email).exists():
        return Response({"error": "Email already registered"}, status=status.HTTP_400_BAD_REQUEST)

    user = Users.objects.create(
        name=name,
        email=email,
        password=make_password(password),
        role=role
    )

    return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def user_login(request):
    data = request.data
    email = data.get("email")
    password = data.get("password")

    try:
        user = Users.objects.get(email=email)
    except Users.DoesNotExist:
        return Response({"error": "Invalid email or password"}, status=status.HTTP_401_UNAUTHORIZED)

    if not check_password(password, user.password):
        return Response({"error": "Invalid email or password"}, status=status.HTTP_401_UNAUTHORIZED)

    refresh = RefreshToken.for_user(user)

    return Response({
        "message": "Login successful",
        "user": {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "role": user.role,
        },
        "tokens": {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }
    }, status=status.HTTP_200_OK)


@api_view(['POST'])
def user_logout(request):
    logout(request)
    return Response({'message': 'Logged out successfully'}, status=200)


@api_view(['GET'])
def event(request):
    booking_records = Events.objects.all()
    serializer = EventsSerializer(booking_records, many=True)
    return Response(serializer.data)


@api_view(['GET', 'POST'])
def book_tickets(request):
    if request.method == 'GET':
        title = request.GET.get('title')
        if not title:
            return Response({"error": "Title parameter is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            event = Events.objects.get(title=title)
        except Events.DoesNotExist:
            return Response({"error": "Event not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = EventsSerializer(event)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        user_id = request.data.get('user_id')
        event_id = request.data.get('event_id')
        seats_requested = int(request.data.get('seats', 1))

        try:
            user = Users.objects.get(id=user_id)
            event = Events.objects.get(id=event_id)
        except (Users.DoesNotExist, Events.DoesNotExist):
            return Response({'error': 'Invalid user or event'}, status=status.HTTP_400_BAD_REQUEST)

        if event.available_seats < seats_requested:
            return Response({'error': 'Not enough seats available'}, status=status.HTTP_400_BAD_REQUEST)

        booking = Bookings.objects.create(
            user=user,
            event=event,
            seats_booked=seats_requested,
            status="Confirmed"
        )
        event.available_seats -= seats_requested
        event.save()

        return Response({'message': 'Booking successful', 'booking_id': booking.id}, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def view_my_bookings(request, user_id):
    try:
        event = Bookings.objects.filter(user_id=user_id)
    except Bookings.DoesNotExist:
        return Response({"message": "No Events Found!"}, status=404)

    if not event.exists():
        return Response({"message": "No Events Found!"}, status=404)

    serialized_data = BookingSerializer(event, many=True).data
    return Response(serialized_data, status=200)


def is_admin(user):
    return user.role.lower() == "admin"


@api_view(["GET", "PUT", "PATCH", "DELETE"])
def event_detail(request, pk):
    event = get_object_or_404(Events, pk=pk)

    if request.method == "GET":
        serializer = EventsSerializer(event)
        return Response(serializer.data)

    elif request.method in ["PUT", "PATCH"]:
        if not is_admin(request.user):
            return Response({"detail": "Only admins can update events."},
                            status=status.HTTP_403_FORBIDDEN)
        serializer = EventsSerializer(event, data=request.data, partial=(request.method == "PATCH"))
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        if not is_admin(request.user):
            return Response({"detail": "Only admins can delete events."},
                            status=status.HTTP_403_FORBIDDEN)
        event.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

