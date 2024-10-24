# Uncomment the imports before you add the code
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = 'djangoapp'
urlpatterns = [
    # # path for registration

    # path for login
    
    path('login/', views.login_user, name='login'),
   
   # path for logout
    path('logout/', views.logout_user, name='logout'),  # Ensure this path is correctly defined

   #path to register
    path('register/', views.registration, name='register'),

    # path for dealer reviews view

    # path for add a review view

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
