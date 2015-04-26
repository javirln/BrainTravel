from django.conf.urls import patterns, include, url
from django.contrib import admin
from BrainTravel import settings

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'principal.views.MainViews.home'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^signin/$', 'principal.views.UserViews.sign_in'),
    url(r'^logout/$', 'principal.views.UserViews.system_logout'),
    url(r'^search', 'principal.views.TripViews.search_trip'),
    #Para indicar en las URLs un metodo que se encuentra dentro de un archivo .py
    # url(r'^<nombre_url>$', '<app>.<paquete>.<archivo>.<metodo>'),
    # url(r'^<nombre_url>$', 'principal.views.ViewsModel1.method1')
    url(r'^register_traveller/$', 'principal.views.UserViews.create_traveller'),
    url(r'^confirm_account/$', 'principal.views.UserViews.confirm_account'),
    url(r'^public_trip_details/(?P<trip_id>[0-9]+)$', 'principal.views.TripViews.public_trip_details'),
    url(r'^administrator/trip/list/$', 'principal.views.TripViews.list_trip_administrator'),
    url(r'^administrator/trip/update/(?P<trip_id>[0-9]+)$', 'principal.views.TripViews.update_state'),
    url(r'^coin/list/$', 'principal.views.Coinviews.list_coin_traveller'),
    url(r'^trip/mylist/(?P<optional>.*)$', 'principal.views.TripViews.list_all_by_traveller'),
    url(r'^trip/edit/(?P<trip_id>[0-9]+)$$', 'principal.views.TripViews.trip_edit'),
    url(r'^trip/create/$', 'principal.views.TripViews.trip_create'),
    url(r'^judge/(?P<trip_id>[0-9]+)/(?P<like>[0-1])', 'principal.views.JudgeViews.judge'),
    url(r'^profile/(?P<traveller_id>[0-9]+)$', 'principal.views.TravellerViews.profile_details'),
    url(r'^profile/edit/$', 'principal.views.TravellerViews.profile_edit'),
    url(r'^profile/edit/password/$', 'principal.views.TravellerViews.profile_edit_password'),
    url(r'^trip/draft/$', 'principal.views.TripViews.list_all_by_traveller_draft'),
    url(r'^public_trip_details/comment/', 'principal.views.TripViews.comment_trip'),
    url(r'^public_trip_details/rate/', 'principal.views.TripViews.send_assessment'),
    url(r'^auth_request/$', 'principal.views.FoursquareViews.foursquare_request'),
    url(r'^trip/list/(?P<profile_id>[0-9]+)$', 'principal.views.TripViews.list_trip_approved_by_profile'),
    url(r'^trip/planned_trips$', 'principal.views.TripViews.planned_trips'),
    url(r'^payment/$', 'principal.views.TravellerViews.all_payments'),
    #paypal urls
    url(r'^buy_coins/$', 'principal.views.Coinviews.buy_coins'),
    url(r'^test_paypal/$', 'principal.views.PayPalViews.test_paypal_view'),
    url(r'^show_planning/(?P<trip_id>[0-9]+)/$', 'principal.views.FoursquareViews.show_planning'),
    url(r'^venue_details/(?P<id_venue>[0-9]+)$', 'principal.views.FoursquareViews.retrieve_venue'),
    url(r'^venue_details/rate/$', 'principal.views.TripViews.send_feedback'),
    url(r'^venue_details/value_tip/(?P<id_venue>[0-9]+)/(?P<id_tip>[0-9]+)$', 'principal.views.TripViews.value_tip'),
    url(r'^statistics/$', 'principal.views.TripViews.stats'),
    #planner URLs
    url(r'^planner/list_venues/$', 'principal.views.FoursquareViews.foursquare_list_venues'),
    (r'^something/paypal/', include('paypal.standard.ipn.urls')),

    #i18n
    url(r'i18n/change_language', 'principal.views.TranslateViews.change_language'),
)

if settings.DEBUG:
    import debug_toolbar

urlpatterns += patterns('',
                        url(r'^__debug__/', include(debug_toolbar.urls)),
)