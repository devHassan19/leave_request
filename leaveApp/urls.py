from django.urls import path
from .views import login_view, staff_page, admin_page , register_view , logout_view
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', login_view, name='login'),
    path('staff-page/', staff_page, name='staff_page'),
    path('admin-page/', admin_page, name='admin_page'),
    path('register/',   register_view, name='register'),
    path('logout/', logout_view, name='logout'),
]



if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)