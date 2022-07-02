from django.urls import path
from . import views


urlpatterns = [
    path('upload/<filename>', views.ExcelUploadView.as_view(), name='upload'),
    path('clients/', views.ClientListView.as_view(), name='client_list'),
    path('bills/', views.BillListView.as_view(), name='bill_list'),
]
