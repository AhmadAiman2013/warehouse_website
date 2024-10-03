from django.db import models
from api.models import CustomUser, Inbound, Outbound, Inventory
from rest_framework import generics
from .serializers import UserSerializer, InboundSerializer , OutboundSerializer , InventorySerializer ,MyTokenObtainPairSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from .permissions import IsManagerOrReadOnly
from rest_framework_simplejwt.views import TokenObtainPairView
from django_filters import rest_framework as filters
from rest_framework.filters import SearchFilter

from django.db.models import Q

# Create your models here.
class CreateUserView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

class InboundListCreateView(generics.ListCreateAPIView):
    queryset = Inbound.objects.all()
    serializer_class = InboundSerializer
    permission_classes = [IsManagerOrReadOnly]
    
class InboundDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Inbound.objects.all()
    serializer_class = InboundSerializer
    permission_classes = [IsManagerOrReadOnly]

class OutboundListCreateView(generics.ListCreateAPIView):
    queryset = Outbound.objects.all()
    serializer_class = OutboundSerializer
    permission_classes = [IsManagerOrReadOnly]
    
class InventoryCreateView(generics.ListCreateAPIView):
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer
    permission_classes = [IsManagerOrReadOnly]
    

class InventoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer
    permission_classes = [IsManagerOrReadOnly]

class InventoryFilter(filters.FilterSet):
    search = filters.CharFilter(method='search_filter', label="Search")

    class Meta:
        model = Inventory
        fields = ['sku', 'category', 'name', 'location', 'quantity', 'supplier', 'search']

    def search_filter(self, queryset, name, value):
        # if not value:
        #     return queryset  
        return queryset.filter(
            Q(sku__icontains=value) |
            Q(category__icontains=value) |
            Q(name__icontains=value) |
            Q(location__icontains=value) |
            Q(supplier__icontains=value)
        )

class InventoryList(generics.ListAPIView):
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = (filters.DjangoFilterBackend, SearchFilter)
    filterset_class = InventoryFilter
    search_fields = ['sku', 'category', 'name', 'location', 'supplier']
    
    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     search = self.request.query_params.get('search', None)
    #     if search is None or search.strip() == "":
    #         return queryset
    #     return self.filterset_class().search_filter(queryset, 'search', search)
    

        



