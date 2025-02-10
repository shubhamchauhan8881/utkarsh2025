from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomePageView.as_view(), name="homepage"),
    path('events', views.EventsPageView.as_view(), name="eventspage"),
    path('events/<slug:eventname>', views.EventsPageView.as_view()),
    path('events/enroll/<slug:eventname>',  views.EventsEnrollPageView.as_view()),
    path('events/enroll/<str:registration_type>/success/<int:regid>',  views.EventRegSuccess.as_view()),
    path('events/details/<slug:name>', views.EventsDetailedPageView.as_view()),
    path("events/<slug:eventname>/unenroll/<int:regid>", views.UnEnrollEvent.as_view()),
    
    path("profile", views.UserProfileView.as_view(), name="profilepage" ),
    
    path('login', views.LoginPageView.as_view(), name="loginpage"),
    path('logout', views.LogOutView.as_view(), name="logoutv"),
    path('register', views.RegisterView.as_view(), name="registerpage"),
    path('accomodation', views.Accmodation.as_view()),
]
