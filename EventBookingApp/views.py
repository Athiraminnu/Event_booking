from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.hashers import make_password, check_password
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from EventBookingApp.models import Users
from rest_framework_simplejwt.tokens import RefreshToken


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


# @api_view(['GET'])
# def booking(request):
#     booking_records = AppointmentDetails.objects.all()
#     serializer = AppointmentDetailsSerializers(booking_records, many=True)
#     return Response(serializer.data)



