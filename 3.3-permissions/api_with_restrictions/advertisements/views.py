from django.contrib.auth.models import Group
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from advertisements.filters import AdvertisementFilter
from advertisements.models import Advertisement, Favourite
from advertisements.permissions import IsOwnerOrReadOnly
from advertisements.serializers import AdvertisementSerializer


class AdvertisementViewSet(ModelViewSet):
    """ViewSet для объявлений."""
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    filterset_class = AdvertisementFilter


    def get_permissions(self):
        """Получение прав для действий."""

        if self.action in ["create", "update", "partial_update", "destroy"]:
            if self.request.user.is_staff:
                return [IsAdminUser()]
            return [IsAuthenticated(), IsOwnerOrReadOnly()]
        return []

    def list(self, request, *args, **kwargs):
        try:
            status_queryset = Advertisement.objects.all().exclude(~Q(creator=request.user), status='DRAFT')
            queryset = self.filter_queryset(status_queryset)
            serializer = AdvertisementSerializer(queryset, many=True)
        except TypeError:
            status_queryset = Advertisement.objects.all().exclude(status='DRAFT')
            queryset = self.filter_queryset(status_queryset)
            serializer = AdvertisementSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['GET'])
    def favourites(self, request, *args, **kwargs):
        try:
            ads = Advertisement.objects.filter(favourites__user=self.request.user)
            serializer = AdvertisementSerializer(ads, many=True)
            return Response(serializer.data)
        except TypeError:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

    @action(detail=True, methods=['POST'], url_path='add-to-favourite')
    def add_to_favourite(self, request, *args, **kwargs):
        ads = self.get_object()
        user = request.user
        if user == ads.creator:
            return Response({'detail': "you can't add your own listing to favorites"})
        try:
            favourite, created = Favourite.objects.get_or_create(user=user, advertisement=ads)
            return Response(status=status.HTTP_201_CREATED)
        except TypeError:
            return Response({'detail': 'register to add to favorites'})

    @action(detail=True, methods=['DELETE'], url_path='remove-from-favourite')
    def remove_from_favourite(self, request, *args, **kwargs):
        ads = self.get_object()
        user = request.user
        favourite = Favourite.objects.filter(user=user, advertisement=ads).first()
        if not favourite:
            return Response(status=status.HTTP_404_NOT_FOUND)
        favourite.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)