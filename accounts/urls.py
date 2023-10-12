from django.urls import path, re_path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve

app_name = 'accounts'

urlpatterns = [
    path('dashboard', views.dashboard, name="dashboard"),
    path('make_payment_page',views.make_payment_page, name="make_payment_page"),
    path('pay', views.pay, name="pay"),
    path('deposit',views.deposit,name="deposit"),
    path('verify/<str:reference>/', views.verify_payment, name='verify_payment'),   
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

