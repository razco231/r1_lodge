from django.contrib import admin
from .models import Room, Booking, RoomImage

# 👇 This is the inline part
class RoomImageInline(admin.StackedInline):   # or StackedInline
    model = RoomImage
    extra = 1   # how many empty fields to show

# 👇 Attach inline to Room
@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ['name', 'price']
    inlines = [RoomImageInline]

# Booking admin (keep this)
from .models import Booking

class BookingAdmin(admin.ModelAdmin):
    list_display = ('room', 'guest_name', 'check_in', 'check_out', 'total_price', 'status')
    list_filter = ('status', 'room')
    search_fields = ('guest_name', 'guest_email')

admin.site.register(Booking, BookingAdmin)