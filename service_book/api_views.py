from rest_framework import viewsets
from .models import Machine, Maintenance, Claim
from .serializers import MachineSerializer, MaintenanceSerializer, ClaimSerializer
from rest_framework.permissions import IsAuthenticated, BasePermission

class IsManagerOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        return request.user.groups.filter(name='Менеджер').exists()

class MachineViewSet(viewsets.ModelViewSet):
    queryset = Machine.objects.all()
    serializer_class = MachineSerializer
    permission_classes = [IsManagerOrReadOnly]

class MaintenanceViewSet(viewsets.ModelViewSet):
    queryset = Maintenance.objects.all()
    serializer_class = MaintenanceSerializer
    permission_classes = [IsAuthenticated]

class ClaimViewSet(viewsets.ModelViewSet):
    queryset = Claim.objects.all()
    serializer_class = ClaimSerializer
    permission_classes = [IsAuthenticated]