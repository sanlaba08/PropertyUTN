from django.contrib import admin
from .models import City, Property, RentalDate, Reservation

# Register your models here.
admin.site.register(City)
admin.site.register(Reservation)


class RentalDate_inLine(admin.TabularInline):
    model = RentalDate
    fk_name = 'property'
    max_num = 7


class PropertyAdmin(admin.ModelAdmin):
    inlines = [RentalDate_inLine, ]


admin.site.register(Property, PropertyAdmin)
