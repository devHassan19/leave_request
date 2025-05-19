from django.urls import path
from .views import login_view, staff_page, admin_page


urlpatterns = [
    path('', login_view, name='login'),
    path('staff-page/', staff_page, name='staff_page'),
    path('admin-page/', admin_page, name='admin_page'),
]
