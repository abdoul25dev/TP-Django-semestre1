
from rest_framework import viewsets, permissions

from .models import Reservation, Salle
from .serializers import ReservationSerializer, SalleSerializer
from .permissions import IsOwnerOrReadOnly


class SalleViewSet(viewsets.ModelViewSet):
    queryset = Salle.objects.all()
    serializer_class = SalleSerializer

    permission_classes = [permissions.IsAdminUser]


class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def perform_create(self, serializer):
      serializer.save(utilisateur=self.request.user)

