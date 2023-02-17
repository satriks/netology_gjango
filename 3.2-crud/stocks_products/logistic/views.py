from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter,OrderingFilter
from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination
from rest_framework.viewsets import ModelViewSet

from logistic.models import Product, Stock
from logistic.serializers import ProductSerializer, StockSerializer


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend,SearchFilter, OrderingFilter]
    # при необходимости добавьте параметры фильтрации
    search_fields = ['title', 'description']
    ordering_fields = ['id', 'title', 'description']
    pagination_class = LimitOffsetPagination

class StockViewSet(ModelViewSet):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer
    # при необходимости добавьте параметры фильтрации
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields  = ['products']
    search_fields = ['products__title', 'products__description']
    pagination_class = LimitOffsetPagination
