from django.urls import path, re_path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve

app_name = 'accounts'

urlpatterns = [
    path('dashboard', views.dashboard, name="dashboard"),
    path('make_payment_page',views.make_payment_page, name="make_payment_page"),
    path('deposit',views.deposit,name="deposit"),
    path('deposited/', views.deposit_complete, name='deposit_detail'),   
    path('generate_pdf/<str:ref>/', views.generate_pdf, name='generate_pdf'),
    path('payment_history', views.payment_history, name="payment_history"),
    path('generate_payment_history_pdf/', views.generate_payment_history_pdf, name='generate_payment_history_pdf'),
    path('user_fees/', views.user_fees_list, name='user_fees_list'),
    path('generate_pdf/', views.generate_pdf, name='generate_pdf'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

