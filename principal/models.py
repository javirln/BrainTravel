# -*- coding: latin-1 -*-
import datetime
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils import timezone
from django.template.defaultfilters import default


# --------------------------- CUSTOMS VALIDATORS  ----------------------------------
def PastValidator(value):
    if value > timezone.now():
        raise ValidationError(u'' + str(value) + ' Is a future date!')


# -----------------------------------------------------------------------------------

# Create your models here.
class Administrator(User):
    class Meta:
        permissions = (
            ('administrator', 'Administrator'),
        )
        db_table = 'administrator'


class Category(models.Model):
    id_foursquare = models.CharField(max_length=30, unique=True)
    name = models.CharField(max_length=50)


    class Meta:
        db_table = 'category'

    def __unicode__(self):
        return self.name


        # Conceptually it's abstract, but Django not implement in BD abstract classes


class Scorable(models.Model):
    name = models.CharField(max_length=255)

    # ----------- Derivates -------------------------------#
    rating = models.FloatField(null=True, validators=[MinValueValidator(0), MaxValueValidator(10)])

    class Meta:
        db_table = 'scorable'


class Venue(Scorable):
    id_foursquare = models.CharField(max_length=30, unique=True)
    latitude = models.CharField(max_length=50)
    longitude = models.CharField(max_length=50)
    photo = models.CharField(max_length=256, null=True, blank=True)
    is_food = models.BooleanField(default=False)

    # ------------- Relationships --------------#
    categories = models.ManyToManyField(Category)

    class Meta:
        db_table = 'venue'

    def __unicode__(self):
        return self.name


class Feedback(models.Model):
    description = models.CharField(max_length=255, null=True)
    leadTime = models.IntegerField(validators=[MinValueValidator(1)])
    duration = models.IntegerField(validators=[MinValueValidator(1)])

    # ---------- Derivate ---------------#
    usefulCount = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)])

    # ------------- Relationships --------------#
    traveller = models.ForeignKey('principal.Traveller')
    venues = models.ForeignKey(Venue)

    class Meta:
        db_table = 'feedback'


# class City(models.Model):
# name = models.CharField(max_length=50)
# country = models.CharField(max_length=50)
# description = models.TextField()
# 
#     class Meta:
#         db_table = 'city'
# 
#     def __unicode__(self):
#         return self.name


class Trip(Scorable):
    State = (
        ('ap', 'Approved'),
        ('re', 'Rejected'),
        ('pe', 'Pending'),
        ('df', 'Draft')
    )
    publishedDescription = models.TextField(null=True)
    startDate = models.DateField(null=True)
    endDate = models.DateField(null=True)
    planified = models.BooleanField(default=False)
    coins = models.IntegerField(validators=[MinValueValidator(0)])
    state = models.CharField(max_length=2, choices=State, default='pe')

    # ------------- Derivates -----------------------------#
    likes = models.IntegerField(validators=[MinValueValidator(0)], default=0)
    dislikes = models.IntegerField(validators=[MinValueValidator(0)], default=0)

    # ------------- Relationships --------------#
    traveller = models.ForeignKey('principal.Traveller')
    # city = models.ForeignKey(City)
    city = models.CharField(max_length=50, null=False)
    country = models.CharField(max_length=50, null=False)
    possible_venues = models.ManyToManyField(Venue)
    

    class Meta:
        db_table = 'trip'

    def __unicode__(self):
        return 'Ini: ' + str(self.startDate) + 'End: ' + str(self.endDate)


class Traveller(User):
    Genre = (
        ('MA', 'MALE'),
        ('FE', 'FEMALE')
    )

    genre = models.CharField(max_length=2, choices=Genre, null=True)
    photo = models.ImageField(upload_to='static/user_folder/', null=True, default='static/user_folder/default.jpg')

    # ----------- Derivates -------------------#
    reputation = models.FloatField(null=True, blank=True,
                                   validators=[MinValueValidator(0), MaxValueValidator(10)], default=0)
    coins = models.IntegerField(validators=[MinValueValidator(0)], default=0)
    recommendations = models.IntegerField(validators=[MinValueValidator(0)], default=0)
    
    # ------------- Relationships --------------#
    likedFeedback = models.ManyToManyField(Feedback, through='Likes', related_name='traveller_likes')
    jugedTrips = models.ManyToManyField(Trip, through='Judges', related_name='judges')
    commentedTrips = models.ManyToManyField(Trip, through='Comment', related_name='commenters')
    assessedScorables = models.ManyToManyField(Scorable, through='Assessment')
    
    
    class Meta:
        db_table = 'traveller'
        permissions = (
            ('traveller', 'Traveller'),
        )
    
    
    def __unicode__(self):
        return self.first_name
    
    
    def save(self, *args, **kwargs):
        # delete old file when replacing by updating the file
        try:
            this = Traveller.objects.get(id=self.id)
            if this.photo != self.photo and this.photo.name != 'static/user_folder/default.jpg':
                this.photo.delete(save=False)
        except:
            # when new photo then we do nothing, normal case
            pass
        super(Traveller, self).save(*args, **kwargs)


class Notification(models.Model):
    text = models.CharField(max_length=255)
    viewed = models.BooleanField(default=False)
    # ------------- Relationships --------------#
    user = models.ForeignKey(Traveller)

    class Meta:
        db_table = 'notification'


class Likes(models.Model):
    useful = models.BooleanField(default=False)
    comment = models.CharField(max_length=255, null=True)

    # -------------- Relationships -------------------
    traveller = models.ForeignKey(Traveller)
    feedback = models.ForeignKey(Feedback)

    class Meta:
        db_table = 'likes'


class Day(models.Model):
    numberDay = models.IntegerField(validators=[MinValueValidator(1)])
    date = models.DateField(null=True)

    # ------------- Relationships --------------#
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    venues = models.ManyToManyField(Venue, through='VenueDay')

    class Meta:
        db_table = 'day'

    def clean(self):
        if self in self.trip.day_set:
            raise ValidationError('The trip already contains this day!')

    def __unicode__(self):
        return 'Day: ' + str(self.numberDay)


class VenueDay(models.Model):
    order = models.IntegerField(validators=[MinValueValidator(1)])

    # ------------- Relationships --------------#
    venue = models.ForeignKey(Venue)
    day = models.ForeignKey(Day)

    class Meta:
        unique_together = ('venue', 'day')
        db_table = 'venue_day'


class Comment(models.Model):
    description = models.CharField(max_length=255, null=True)
    date = models.DateTimeField(default=timezone.now)
    # ------------- Relationships --------------#
    traveller = models.ForeignKey(Traveller)
    trip = models.ForeignKey(Trip)

    class Meta:
        db_table = 'comment'


class Judges(models.Model):
    like = models.BooleanField(default=False)

    # ------------- Relationships --------------#
    traveller = models.ForeignKey(Traveller)
    trip = models.ForeignKey(Trip, related_name='judgedTrip')

    class Meta:
        db_table = 'judges'


class Payment(models.Model):
    amount = models.FloatField(validators=[MinValueValidator(0)])
    date = models.DateTimeField(validators=[PastValidator])

    # ------------- Relationships --------------#
    traveller = models.ForeignKey(Traveller)

    class Meta:
        db_table = 'payment'


class CoinHistory(models.Model):
    amount = models.IntegerField()
    date = models.DateTimeField(validators=[PastValidator])
    concept = models.CharField(max_length=255)

    # -------------     Relationships --------------#
    traveller = models.ForeignKey(Traveller)
    payment = models.OneToOneField(Payment, null=True, blank=True)
    trip = models.OneToOneField(Trip, null=True, blank=True)

    class Meta:
        db_table = 'coin_history'

    def __unicode__(self):
        return str(self.amount)


class Schedule(models.Model):
    day = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(7)])
    openingTime = models.CharField(null=True, max_length=128)
    closingTime = models.CharField(null=True, max_length=128)

    # ------------- Relationships --------------#
    venue = models.ForeignKey(Venue)

    class Meta:
        db_table = 'schedule'


class Assessment(models.Model):
    score = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)])
    comment = models.CharField(max_length=255)

    # ------------- Relationships --------------#
    traveller = models.ForeignKey(Traveller)
    scorable = models.ForeignKey(Scorable)

    class Meta:
        db_table = 'assessment'
