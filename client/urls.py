from django.urls import path
from .views import (
index,signup,signin,order

)

app_name = 'client'

urlpatterns = [
        path('', index, name='main'),
        path('signup/',signup, name='signup'),
        path('login/',signin, name='login'),
        path('<int:partner_id>/',order, name='order'),
]
