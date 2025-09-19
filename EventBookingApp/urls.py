from. import views
from django.urls import path


urlpatterns = [
    path('', views.home, name="home"),
    path('login/', views.user_login, name="login"),
    path("registration/", views.user_registration, name="registration"),
    path("logout/", views.user_logout, name="logout"),
    path("events/", views.event, name="event"),
    path("bookings/", views.book_tickets, name="book_ticket"),
]
