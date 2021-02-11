from django.urls import path
from . import views
urlpatterns = [
    path('sign_up/', views.SignUpView.as_view(), name='sign_up'),
    path('sign_in/', views.SignInView.as_view(), name='sign_in'),
    path('sign_out/', views.SignOutView.as_view(), name='sign_out'),

]