from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('room/<int:id>/', views.room_detail, name='room_detail'),
    path('book/<int:id>/', views.book_room, name='book_room'),
    path('contact/', views.contact, name='contact'),
    path('success/', views.success, name='success'),
    path('gallery/', views.gallery, name='gallery'),
    path('about/', views.about, name='about'),
]