from django.contrib import admin
from django.db import models
from .models import Topic, Course, Student, Order
from math import ceil
from decimal import Decimal


class CourseInline(admin.TabularInline):  # newly added
    model = Course


class TopicAdmin(admin.ModelAdmin):  # newly added
    list_display = ('name', 'category')
    inlines = [
        CourseInline,
    ]


class CourseAdmin(admin.ModelAdmin):
    # newly added starts here
    list_display = ('name', 'price')
    actions = ['discount_10']

    def discount_10(self, request, queryset):
        discount = 10  # percentage

        for product in queryset:
            multiplier = discount / 100  # discount / 100 in python 3
            old_price = ceil(product.price)
            new_price = ceil(old_price - (old_price * multiplier))
            product.price = new_price
            product.save(update_fields=['price'])

    discount_10.short_description = 'Set 10%% discount'


# newly added ends here


class StudentAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'address')


admin.site.register(Topic, TopicAdmin)  # newly added
admin.site.register(Course, CourseAdmin)  # newly added
admin.site.register(Student, StudentAdmin)  # newly added
# admin.site.register(Topic) #newly removed
# admin.site.register(Course)  # newly removed
# admin.site.register(Student) # newly removed
admin.site.register(Order)
