from django.shortcuts import render, get_object_or_404
from django.core.mail import send_mail
from .models import Room, Booking, RoomImage
from datetime import datetime


def home(request):
    rooms = Room.objects.all()
    return render(request, 'home.html', {'rooms': rooms})


def room_detail(request, id):
    room = get_object_or_404(Room, id=id)
    return render(request, 'room_detail.html', {'room': room})


def book_room(request, id):
    room = get_object_or_404(Room, id=id)

    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        check_in = request.POST.get('check_in')
        check_out = request.POST.get('check_out')

        if not name or not email or not check_in or not check_out:
            return render(request, 'book_room.html', {
                'room': room,
                'error': 'All fields are required'
            })

        check_in_date = datetime.strptime(check_in, '%Y-%m-%d').date()
        check_out_date = datetime.strptime(check_out, '%Y-%m-%d').date()

        if check_out_date <= check_in_date:
            return render(request, 'book_room.html', {
                'room': room,
                'error': 'Check-out date must be after check-in date'
            })

        overlapping_booking = Booking.objects.filter(
            room=room
        ).filter(
            check_in__lt=check_out_date,
            check_out__gt=check_in_date
        ).exists()

        if overlapping_booking:
            return render(request, 'book_room.html', {
                'room': room,
                'error': 'Sorry, this room is already booked for those dates.'
            })

        number_of_days = (check_out_date - check_in_date).days
        total_price = number_of_days * room.price

        booking = Booking.objects.create(
            room=room,
            guest_name=name,
            guest_email=email,
            check_in=check_in_date,
            check_out=check_out_date,
            total_price=total_price
        )

        send_mail(
            subject='New Room Booking Request',
            message=f'''
A new booking has been submitted.

Room: {room.name}
Guest Name: {name}
Guest Email: {email}
Check-in Date: {check_in_date}
Check-out Date: {check_out_date}
Number of Nights: {number_of_days}
Estimated Cost: ₦{total_price}
''',
            from_email=None,
            recipient_list=['abdussalamrazco@gmail.com'],
            fail_silently=True,
        )

        return render(request, 'success.html', {
            'booking': booking,
            'days': number_of_days
        })

    return render(request, 'book_room.html', {'room': room})


def contact(request):
    return render(request, 'contact.html')


def success(request):
    return render(request, 'success.html')


def gallery(request):
    rooms = Room.objects.all()
    return render(request, 'gallery.html', {'rooms': rooms})


def about(request):
    return render(request, 'about.html')