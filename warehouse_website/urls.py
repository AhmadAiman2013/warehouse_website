"""
URL configuration for warehouse_website project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from api.views import CreateUserView, MyTokenObtainPairView, InboundListCreateView, InboundDetailView, OutboundListCreateView, InventoryCreateView, InventoryDetailView, InventoryList
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/user/register/', CreateUserView.as_view(), name='register'),
    path('api/token/', MyTokenObtainPairView.as_view(), name='get_token'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='refresh'),
    path('api/inbound/', InboundListCreateView.as_view(), name='inbound-list'),
    path('api/inbound/<int:pk>/', InboundDetailView.as_view(), name='inbound-detail'),
    path('api/outbound/', OutboundListCreateView.as_view(), name='outbound-list'),
    path('api/inventory/<int:pk>/', InventoryDetailView.as_view(), name='inventory-detail'),
    path('api/inventory/list/', InventoryList.as_view(), name='inventory-list-filter'),
    path('api/inventory/', InventoryCreateView.as_view(), name='inventory-create')
]
