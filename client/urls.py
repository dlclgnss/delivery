from django.urls import path
from .views import (
index,signup,signin

)

app_name = 'client'

urlpatterns = [
        path('', index, name='main'),
        path('signup/',signup, name='signup'),
        path('login/',signin, name='login'),
]
