# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
import datetime
from principal.models import Administrator, Category, Scorable, Venue, Feedback, City, Trip, Traveller, \
    Likes, Day, VenueDay, Comment, Judges, Payment, CoinHistory, Schedule, Assessment

#Los archivos que se encuentren en el paquete commands, se podr�n llamar
#desde manage.py, de forma que para popular la base de datos debemos hacer
# 'manage.py populate_db'

class Command(BaseCommand):
    args = '<foo bar ...>'
    help = 'our help string comes here'

    def _migrate(self):
        # Drop all tables
        print('Dropping tables...')
        
        #Aqui el borrado de todas las tablas
        #Example: User.objects.all().delete()
        Administrator.objects.all().delete()
        User.objects.all().delete()
        Category.objects.all().delete()
        Scorable.objects.all().delete()
        Venue.objects.all().delete()
        Schedule.objects.all().delete()
        City.objects.all().delete()
        Traveller.objects.all().delete()
        Trip.objects.all().delete()
        Feedback.objects.all().delete()
        Likes.objects.all().delete()
        Day.objects.all().delete()
        VenueDay.objects.all().delete()
        Comment.objects.all().delete()
        Judges.objects.all().delete()
        Payment.objects.all().delete()
        CoinHistory.objects.all().delete()
        Assessment.objects.all().delete()

        print('Dropping tables...OK')
        print('Populating database...')

        # Aqui la creaci�n de los objetos que populan la base de datos
        #Example: Objeto1.save()

        #Administrator initializer
        admin_admin = Administrator(
            username='admin',
            email = 'admin@admin.com')
        admin_admin.set_password('admin12')
        admin_admin.is_staff = True
        admin_admin.is_superuser = True
        admin_admin.save()
        print('Admins created...Ok')

        # Categories

        arts_entertaiment = Category(
            id_foursquare='4d4b7104d754a06370d81259',
            name='Arts&Entertaiment')
        arts_entertaiment.save()

        musemum = Category(
            id_foursquare='4bf58dd8d48988d181941735',
            name='Musemum')
        musemum.save()

        music_venue = Category(
            id_foursquare='4bf58dd8d48988d1e5931735',
            name='Music Venue')
        music_venue.save()

        outdoor_sculpture = Category(
            id_foursquare='52e81612bcbc57f1066b79ed',
            name='Outdoor Sculpture')
        outdoor_sculpture.save()

        public_art = Category(
            id_foursquare='507c8c4091d498d9fc8c67a9',
            name='Public Art')
        public_art.save()

        stadium = Category(
            id_foursquare='4bf58dd8d48988d184941735',
            name='Stadium')
        stadium.save()

        college_university = Category(
            id_foursquare='4d4b7105d754a06372d81259',
            name='College & University')
        college_university.save()

        buffet = Category(
            id_foursquare='52e81612bcbc57f1066b79f4',
            name='Buffet')
        buffet.save()

        cafe = Category(
            id_foursquare='4bf58dd8d48988d16d941735',
            name='Cafe')
        cafe.save()

        chinese_restaurant = Category(
            id_foursquare='4bf58dd8d48988d145941735',
            name='Chinese Restaurant')
        chinese_restaurant.save()

        fish_chips = Category(
            id_foursquare='4edd64a0c7ddd24ca188df1a',
            name='Fish and Chips Shop')
        fish_chips.save()

        irish_pub = Category(
            id_foursquare='52e81612bcbc57f1066b7a06',
            name='Irish Pub')
        irish_pub.save()

        italian_restaurant = Category(
            id_foursquare='4bf58dd8d48988d110941735',
            name='Italian Restaurant')
        italian_restaurant.save()

        bar = Category(
            id_foursquare='4bf58dd8d48988d116941735',
            name='Bar')
        bar.save()

        brewery = Category(
            id_foursquare='50327c8591d4c4b30a586d5d',
            name='Brewery')
        brewery.save()

        cocktail_bar = Category(
            id_foursquare='4bf58dd8d48988d11e941735',
            name='Cocktail Bar')
        cocktail_bar.save()

        nightlife = Category(
            id_foursquare='4bf58dd8d48988d11f941735',
            name='Nightlife')
        nightlife.save()

        park = Category(
            id_foursquare='4bf58dd8d48988d163941735',
            name='Park')
        park.save()

        market = Category(
            id_foursquare='50be8ee891d4fa8dcc7199a7',
            name='Market')
        market.save()

        theater = Category(
            id_foursquare='4bf58dd8d48988d137941735',
            name='Theater')
        theater.save()

        steakhouse = Category(
            id_foursquare='4bf58dd8d48988d1cc941735',
            name='Steakhouse')
        steakhouse.save()

        castle = Category(
            id_foursquare='50aaa49e4b90af0d42d5de11',
            name='Castle')
        castle.save()

        monument_landmark = Category(
            id_foursquare='4bf58dd8d48988d12d941735',
            name='Monument / Landmark')
        monument_landmark.save()

        palace = Category(
            id_foursquare='52e81612bcbc57f1066b7a14',
            name='Palace')
        palace.save()

        bookstore = Category(
            id_foursquare='4bf58dd8d48988d114951735',
            name='Bookstore')
        bookstore.save()

        historic_site = Category(
            id_foursquare='4deefb944765f83613cdba6e',
            name='Historic Site')
        historic_site.save()

        burger = Category(
            id_foursquare='4bf58dd8d48988d16c941735',
            name='Burger Joint')
        burger.save()

        print('Categories...Ok')

        vsc_tower_london = Scorable(
            name='Score Tower of London',
            description='The best place to visit if you want to learn more about' 
                        'Londons history. And of course it houses the Crown Jewels, the most '
                        'famous jewellery collection in the world',
            rating=9.1)
        vsc_tower_london.save()

        vsc_big_ben = Scorable(
            name='Score Big Ben',
            description='Big Ben refers to the 13 ton bell in the clock tower of Westminster Palace.'
                        'Opinion is divided as to whether it was named after the then Commissioner of Works, or a famous prize-fighter of the time.',
             rating=9.5)
        vsc_big_ben.save()

        vsc_buckingham = Scorable(
            name='Score Buckingham Palace',
            description='Get your ticket stamped on exit and it serves as a year-long pass.',
            rating=9.0)
        vsc_buckingham.save()

        vsc_tour_eiffel = Scorable(
            name='Score Tour Eiffel',
            description='A Have to go and see in Paris. The view from the Top is Fantastic. Love PARIS',
            rating=9.7)
        vsc_tour_eiffel.save()

        vsc_parc_du_champs_de_mars = Scorable(
            name='Score Parc du Champs de Mars',
            description='Run to get in better shape! But avoid the Eiffel tower with all the tourists!',
            rating=9.3)
        vsc_parc_du_champs_de_mars.save()

        vsc_shakespeare = Scorable(
            name='Shakespeare & Company',
            description='Looking for a good book? Do like Hemingway & Fitzgerald did in their time and go to the iconic Shakespeare bookstore!',
            rating=8.3)

        vsc_shakespeare.save()

        tsc_london = Scorable(
            name='Score to London trip',
            description='Love it! Absolutely LOVE IT!',
            rating=9.7)
        tsc_london.save()

        tsc_paris = Scorable(
            name='Score to Paris trip',
            description='Went there with my partner and got engaged under the Tour Eiffel. Thanks Paris!',
            rating=10)
        tsc_paris.save()

        print('Scores...Ok')

        v_tower_london = Venue(
            id_foursquare='4ac518cef964a520f7a520e3',
            name='Tower of London',
            description='Explore this mighty fortress and see the Crown Jewels, then discover more stories from this royal palace that once housed a zoo!',
            latitude='51.50802127486276',
            longitude='-0.07626056671142578',
            photo='tower_of_london.jpg',
            phone='+44 844 482 7777')
        v_tower_london.save()
        v_tower_london.categories.add(castle)

        v_big_ben = Venue(
            id_foursquare='4ac518cef964a520f6a520e3',
            name='Big Ben',
            description='Big Ben is the name was given to the Great Bell. The tower housing Big Ben and the four clock dials is called Elizabeth Tower.',
            latitude='51.50064517819402',
            longitude='-0.1245725154876709',
            photo='big_ben.jpg',
            phone='')
        v_big_ben.save()
        v_big_ben.categories.add(monument_landmark, historic_site)

        v_buckingham = Venue(
            id_foursquare='4abe4502f964a520558c20e3',
            name='Buckingham Palace',
            description='Buckingham Palace is the working headquarters of the Monarchy, where The Queen carries out her official '
                        'and ceremonial duties as Head of State of the United Kingdom and Head of the Commonwealth.',
            latitude='51.50130303159478',
            longitude='-0.1421034336090088',
            photo='buckingham_palace.jpg',
            phone='')
        v_buckingham.save()
        v_buckingham.categories.add(palace)

        v_burger = Venue(
            id_foursquare='4dfdff771f6e05048d8b1cde',
            name='Honest Burgers',
            description='As gourmet patties lead the meat revolution in London, we pick out ten must-try burger joints',
            latitude='51.462316',
            longitude='-0.111953',
            photo='burger.jpg',
            phone='+442077337963')
        v_burger.save()
        v_burger.categories.add(burger)

        v_tour_eiffel = Venue(
            id_foursquare='51a2445e5019c80b56934c75',
            name='Tour Eiffel',
            latitude='48.85816464940564',
            longitude='2.2944259643554683',
            photo='tour_eiffel.jpg',
            phone='+33892701239')
        v_tour_eiffel.save()
        v_tour_eiffel.categories.add(monument_landmark)

        v_italian_restaurant = Venue(
            id_foursquare='4af86dccf964a5202d0d22e3',
            name='La Fabbrica',
            latitude='48.87746235398098',
            longitude='2.2950826269836853',
            photo='italian_restaurant.jpg',
            phone='+33155379000')
        v_italian_restaurant.save()
        v_italian_restaurant.categories.add(italian_restaurant)

        v_parc_du_champs_de_mars = Venue(
            id_foursquare='4b0d54cbf964a520764623e3',
            name='Parc du Champs de Mars',
            description='Son nom, emprunte au dieu romain de la guerre, lui vient de sa premiere fonction : cetait un champ dexercice pour les cadets de lEcole militaire. Aujourdhui, '
                        'cest un lieu de rassemblement pour les touristes et les Parisiens, a lombre de la Tour Eiffel.',
            latitude='48.85544',
            longitude='2.298975',
            photo='parc_du_champs_de_mars.jpg',
            phone='')
        v_parc_du_champs_de_mars.save()
        v_parc_du_champs_de_mars.categories.add(park)

        v_shakespeare = Venue(
            id_foursquare='4adcda21f964a520f23921e3',
            name='Shakespeare & Company',
            latitude='48.85258084884126',
            longitude='2.3471474647521973',
            photo='shakespeare.jpg',
            phone='+33143714722')
        v_shakespeare.save()
        v_shakespeare.categories.add(bookstore)

        v_museum = Venue(
            id_foursquare='4adcda10f964a520af3521e3',
            name='Louvre',
            latitude='48.860649275706926',
            longitude='2.3370838165283203',
            photo='louvre_museum.jpg',
            phone='+33140205050')
        v_museum.save()
        v_museum.categories.add(musemum)

        print('Venues...Ok')

        sch_tower_london = Schedule(
            day=1,
            openingTime='0900',
            closingTime='1530',
            venue=v_tower_london
            )
        sch_tower_london.save()

        sch_tower_london_1 = Schedule(
            day=1,
            openingTime='1600',
            closingTime='2000',
            venue=v_tower_london)
        sch_tower_london_1.save()

        sch_buckingham = Schedule(
            day=3,
            openingTime='0830',
            closingTime='1000',
            venue=v_buckingham)
        sch_buckingham.save()

        sch_big_ben = Schedule(
            day=2,
            openingTime='1800',
            closingTime='2000',
            venue=v_big_ben)
        sch_big_ben.save()

        print('Schedules...Ok')

        london = City(
            name='London',
            country='United Kingdom',
            description='London is by far the largest city in England and the United Kingdom.' 
                        '8.6 million people live in London, which is on the River Thames. It is the capital of the United Kingdom.')
        london.save()

        paris = City(
            name='Paris',
            country='France',
            description='Paris is the capital city of France, and the largest city in that country.'
                        'The area is 105 square km, and around 2.15 million people live there. If suburbs are counted, the population of the Paris area rises to 12 million people.')
        paris.save()

        print('Cities...Ok')
        
        traveller_annie = Traveller(
            username='annie',
            email='annie@mail.com',
            first_name='Annie',
            last_name='Stone',
            genre='FE',
            photo='annie_stone.jpg',
            reputation=7.5,
            coins=30,
            recommendations=5)
        traveller_annie.set_password('annie')
        traveller_annie.save()

        sch_annie = Scorable(
            name='Traveller score',
            description='Amazing girl',
            rating=78.5)
        sch_annie.save()

        traveller_allen = Traveller(
            username='allen',
            email = 'allen@mail.com',               
            first_name='Allen',
            last_name='Sutton',
            genre='MA',
            photo='allen_sutton.jpg',
            reputation=8.2,
            coins=23,
            recommendations=13)
        traveller_allen.set_password('allen')
        traveller_allen.save()

        sch_allen = Scorable(
            name='Traveller score',
            description='Amazing boy',
            rating=86.0)
        sch_allen.save()
        
        print('Travellers...Ok')

        trip_london = Trip(
            publishedDescription='Once you arrive in London, start your first day at the true heart of the city - Trafalgar Square. '
                                 'The most famous tourist attractions follow on your itinerary: London Eye, Big Ben and Buckingham Palace. You can finish your '
                                 'day in one of the great museums. Take a little rest from the lively city on the second day, head to the Windsor Castle and take a'                                 
                                 'walk in the Greewich Park afterwards. On the third day, your London itinerary takes you to the landmarks in the center again: the Tower with Tower Bridge next to it and St. Pauls Cathedral.',
            startDate=datetime.date(2014, 12, 25),
            endDate=datetime.date(2014, 12, 28),
            planified=True,
            coins=34,
            likes=125,
            dislikes=30,
            traveller=traveller_allen,
            city=london)                            
        trip_london.save()

        trip_paris = Trip(
            publishedDescription='Most of my friends and family come by for three-day visits and whether its their first time in Paris or their 20th' 
                                 'time, this itinerary always make them happy to be in the city. Although its impossible to discover all of Paris within three days, this guide will give you a good impression of the citys treasures.',
            startDate=datetime.date(2014, 8, 13),
            endDate=datetime.date(2014, 8, 18),
            planified=False,
            coins=23,
            likes=89,
            dislikes=22,
            traveller=traveller_annie,
            city=paris)
        trip_paris.save()

        print('Trips...Ok')

        f_tour_eiffel = Feedback(
            description='Excellent view from the top, we had to wait a lot though',
            leadTime=45,
            duration=60,
            usefulCount=7,
            traveller=traveller_annie,
            venues=v_tour_eiffel)
        f_tour_eiffel.save()

        f_shakespeare = Feedback(
            description='I do really loved that bookstore',
            leadTime=0,
            duration=30,
            usefulCount=8,
            traveller=traveller_annie,
            venues=v_shakespeare)
        f_shakespeare.save()

        f_parc_du_champs_de_mars = Feedback(
            description='Lovely place in front of the Tour Eiffel',
            leadTime=0,
            duration=40,
            usefulCount=9,
            traveller=traveller_annie,
            venues=v_parc_du_champs_de_mars)
        f_parc_du_champs_de_mars.save()

        f_tower_london = Feedback(
            description='Quite mysterious place',
            leadTime=30,
            duration=180,
            usefulCount=8,
            traveller=traveller_allen,
            venues=v_tower_london)
        f_tower_london.save()

        print('Feedback...Ok')

        like_1 = Likes(
            useful=True,
            comment='Nice!',
            traveller=traveller_allen,
            feedback=f_shakespeare)
        like_1.save()

        like_2 = Likes(
            useful=False,
            comment='Already noticed...',
            traveller=traveller_allen,
            feedback=f_tour_eiffel)
        like_2.save()

        print('Likes...Ok')

        day_1_london = Day(
            numberDay=1,
            date=datetime.date(2014, 12, 25),
            description='We didnt want a busy day, just a few things',
            trip=trip_london)
        day_1_london.save()

        day_2_london = Day(
            numberDay=2,
            date=datetime.date(2014, 12, 26),
            description='Buckingham and good burgers!',
            trip=trip_london)
        day_2_london.save()

        day_3_london = Day(
            numberDay=3,
            date=datetime.date(2014, 12, 26),
            description='',
            trip=trip_london)
        day_3_london.save()

        day_1_paris = Day(
            numberDay=1,
            date=datetime.date(2014, 8, 13),
            description='First day in Paris',
            trip=trip_paris)
        day_1_paris.save()

        day_2_paris = Day(
            numberDay=2,
            date=datetime.date(2014, 8, 14),
            description='Second day in Paris',
            trip=trip_paris)
        day_2_paris.save()

        day_3_paris = Day(
            numberDay=3,
            date=datetime.date(2014, 8, 15),
            description='Third day in Paris',
            trip=trip_paris)
        day_3_paris.save()

        day_4_paris = Day(
            numberDay=4,
            date=datetime.date(2014, 8, 16),
            description='Fourth day in Paris',
            trip=trip_paris)
        day_4_paris.save()

        day_5_paris = Day(
            numberDay=5,
            date=datetime.date(2014, 8, 17),
            description='Fifth day in Paris',
            trip=trip_paris)
        day_5_paris.save()

        print('Days...Ok')

        venue_london_tower_london = VenueDay(
            order=1,
            venue=v_tower_london,
            day=day_1_london)
        venue_london_tower_london.save()

        venue_london_big_ben = VenueDay(
            order=1,
            venue=v_big_ben,
            day=day_2_london)
        venue_london_big_ben.save()

        venue_london_burger = VenueDay(
            order=2,
            venue=v_burger,
            day=day_2_london)
        venue_london_burger.save()

        venue_buckingham = VenueDay(
            order=1,
            venue=v_buckingham,
            day=day_3_london)
        venue_buckingham.save()

        venue_paris_tour_eiffel = VenueDay(
            order=1,
            venue=v_tour_eiffel,
            day=day_1_paris)
        venue_paris_tour_eiffel.save()

        venue_paris_italian_restaurant = VenueDay(
            order=1,
            venue=v_italian_restaurant,
            day=day_2_paris)
        venue_paris_italian_restaurant.save()

        venue_paris_shakespeare = VenueDay(
            order=1,
            venue=v_shakespeare,
            day=day_3_paris)
        venue_paris_shakespeare.save()

        venue_paris_parc_du_champs_de_mars = VenueDay(
            order=1,
            venue=v_parc_du_champs_de_mars,
            day=day_4_paris)
        venue_paris_parc_du_champs_de_mars.save()

        venue_paris_musem = VenueDay(
            order=1,
            venue=v_museum,
            day=day_5_paris)
        venue_paris_musem.save()

        print('VenueDays...Ok')

        comment_1 = Comment(
            description='Love the trip you made, really!',
            traveller=traveller_allen,
            trip=trip_paris)
        comment_1.save()

        comment_2 = Comment(
            description='What a trip, oh my Gosh!',
            traveller=traveller_annie,
            trip=trip_london)
        comment_2.save()

        print('Comments...Ok')

        judge_1 = Judges(
            like=True,
            traveller=traveller_allen,
            trip=trip_paris)
        judge_1.save()

        judge_2 = Judges(
            like=False,
            traveller=traveller_annie,
            trip=trip_london)
        judge_2.save()

        print('Judges...Ok')

        payment_annie = Payment(
            amount=7.5,
            date=datetime.date(2014, 3, 3),
            traveller=traveller_annie)
        payment_annie.save()

        payment_allen = Payment(
            amount=2.5,
            date=datetime.date(2014, 12, 20),
            traveller=traveller_allen)
        payment_allen.save()

        print('Payment...Ok')

        coin_history_annie = CoinHistory(
            amount=4.5,
            date=datetime.date(2014, 3, 3),
            concept='Trip to Paris',
            traveller=traveller_annie,
            payment=payment_annie,
            trip=trip_paris)
        coin_history_annie.save()

        coin_history_allen = CoinHistory(
            amount=3.5,
            date=datetime.date(2014, 12, 20),
            concept='Trip to London',
            traveller=traveller_allen,
            payment=payment_allen,
            trip=trip_london)
        coin_history_allen.save()

        print('CoinHistory...Ok')

        assessment_1 = Assessment(
            score=1,
            comment='Assess 1',
            traveller=traveller_annie,
            scorable=sch_annie)
        assessment_1.save()

        assessment_2 = Assessment(
            score=1,
            comment='Assess 2',
            traveller=traveller_allen,
            scorable=sch_allen)
        assessment_2.save()

        print('Assesment...OK\n'
              'Populating database...OK\n'
              'Ready to use!')

    def handle(self, *args, **options):
        self._migrate()