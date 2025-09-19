from. import views
from django.urls import path


urlpatterns = [
    path('', views.home, name="home"),
    path('login/', views.user_login, name="login"),
    path("registration/", views.user_registration, name="registration"),
    path("logout/", views.user_logout, name="logout"),
    path("events/", views.event, name="event"),
    path("bookings/", views.book_tickets, name="book_ticket"),
    path("bookings/my/<int:user_id>/", views.view_my_bookings, name="view_my_bookings"),
    path("update/events/<int:user_id>/", views.event_detail, name="event_detail"),
]
