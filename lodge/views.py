from django.shortcuts import render, get_object_or_404,redirect
from django.core.mail import send_mail
from .models import Room, Booking, RoomImage
from datetime import datetime
from django.contrib.admin.views.decorators import staff_member_required


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


@staff_member_required
def manager_dashboard(request):
    bookings = Booking.objects.all().order_by('-check_in')

    total_bookings = bookings.count()
    pending_bookings = bookings.filter(status='pending').count()
    confirmed_bookings = bookings.filter(status='confirmed').count()
    cancelled_bookings = bookings.filter(status='cancelled').count()

    context = {
        'bookings': bookings,
        'total_bookings': total_bookings,
        'pending_bookings': pending_bookings,
        'confirmed_bookings': confirmed_bookings,
        'cancelled_bookings': cancelled_bookings,
    }

    return render(request, 'manager_dashboard.html', context)

@staff_member_required
def confirm_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    booking.status = 'confirmed'
    booking.save()
    return redirect('manager_dashboard')


@staff_member_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    booking.status = 'cancelled'
    booking.save()
    return redirect('manager_dashboard')
