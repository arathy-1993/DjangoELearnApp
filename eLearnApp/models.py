from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
import datetime
from django.contrib.auth.models import User
from django.utils import timezone


# Create your models here.


class Topic(models.Model):
    name = models.CharField(max_length=200)
    CATEGORY_CHOICES = [('Web Development', 'Development'),
                        ('Management', 'Business'),
                        ('Economics', 'Finance & Accounting'),
                        ('IT Certification', 'IT & Software'),
                        ('Sports', 'Health & Fitness')]
    category = models.CharField(max_length=300, choices=CATEGORY_CHOICES, default='Management', blank=False)

    # here i changed 1 default value to 'Management'

    def __str__(self):
        return self.name


class Course(models.Model):
    topic = models.ForeignKey(Topic, related_name='courses', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2,
                                validators=[MinValueValidator(50), MaxValueValidator(500)])
    for_everyone = models.BooleanField(default=True)
    description = models.TextField(max_length=300, null=True, blank=True)
    interested = models.PositiveIntegerField(default=0)  # newly added
    stages = models.PositiveIntegerField(default=3)  # newly added

    def __str__(self):
        return self.name

    def discount(self):
        discount_amt = (10 * self.price) / 100
        discounted_price = self.price - discount_amt
        return discounted_price
    # def discount(self):  # newly added
    #   discount_amt = (10 * self.price) / 100
    #  discounted_price = self.price - discount_amt
    # return discounted_price


class Student(User):
    CITY_CHOICES = [('WS', 'Windsor'),
                    ('CG', 'Calgery'),
                    ('MR', 'Montreal'),
                    ('VC', 'Vancouver')]
    school = models.CharField(max_length=50, null=True, blank=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    city = models.CharField(max_length=2, choices=CITY_CHOICES, default='WS')
    interested_in = models.ManyToManyField(Topic)
    image = models.ImageField(upload_to=None, height_field=None, width_field=None, blank=True, null=True, default=None)

    def __str__(self):
        return '%s %s' % (self.first_name, self.last_name)


class Order(models.Model):
    course = models.ForeignKey(Course, related_name='orders', on_delete=models.CASCADE, default=1)
    student = models.ForeignKey(Student, related_name='students', on_delete=models.CASCADE)
    levels = models.PositiveIntegerField()
    ORDER_CHOICES = [(0, 'Cancelled'),
                     (1, 'Order Confirmed')]
    order_status = models.IntegerField(choices=ORDER_CHOICES, default=1)
    order_date = models.DateField()

    def __str__(self):
        return self.student.first_name + " " + self.student.last_name
        # return str(self.id) + "_" + self.student.first_name + "_" + self.student.last_name

    def total_cost(self):
        sum = 0
        for course in self.course:
            sum += course.price
        return sum
