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
@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['guest_name', 'room', 'check_in', 'check_out', 'total_price']
    list_filter = ['room', 'check_in', 'check_out']