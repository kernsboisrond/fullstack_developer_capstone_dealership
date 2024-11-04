from django.contrib import admin
# from .models import related models
from .models import CarMake, CarModel


# Inline model for CarModel to display within CarMake
class CarModelInline(admin.TabularInline):
    model = CarModel
    extra = 1  # Show one extra blank CarModel by default

# Admin configuration for CarMake, using CarModelInline
class CarMakeAdmin(admin.ModelAdmin):
    inlines = [CarModelInline]

# Register CarMake with its custom admin configuration
admin.site.register(CarMake, CarMakeAdmin)

# Register CarModel independently so it can be managed separately if needed
admin.site.register(CarModel)