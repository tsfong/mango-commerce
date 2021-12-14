from django.urls import path
from .views.users import SignUp, SignIn, SignOut, ChangePassword
from .views.mango import MangosView

urlpatterns = [
    path('sign-up/', SignUp.as_view(), name='sign-up'),
    path('sign-in/', SignIn.as_view(), name='sign-in'),
    path('sign-out/', SignOut.as_view(), name='sign-out'),
    path('mangos/', MangosView.as_view(), name='mangos'),
    path('change-password/', ChangePassword.as_view(), name='change-password'),
]