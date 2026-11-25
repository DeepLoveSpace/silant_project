from rest_framework import serializers
from .models import Machine, Maintenance, Claim, TechniqueModel

class MachineSerializer(serializers.ModelSerializer):
    technique_model_name = serializers.CharField(source='technique_model.name', read_only=True)
    engine_model_name = serializers.CharField(source='engine_model.name', read_only=True)
    transmission_model_name = serializers.CharField(source='transmission_model.name', read_only=True)
    drive_axle_model_name = serializers.CharField(source='drive_axle_model.name', read_only=True)
    steer_axle_model_name = serializers.CharField(source='steer_axle_model.name', read_only=True)
    client_name = serializers.CharField(source='client.username', read_only=True)
    service_company_name = serializers.CharField(source='service_company.username', read_only=True)

    class Meta:
        model = Machine
        fields = '__all__'

class MaintenanceSerializer(serializers.ModelSerializer):
    maintenance_type_name = serializers.CharField(source='maintenance_type.name', read_only=True)
    machine_serial = serializers.CharField(source='machine.serial_number', read_only=True)
    organization_name = serializers.CharField(source='organization.username', read_only=True)
    
    class Meta:
        model = Maintenance
        fields = '__all__'

class ClaimSerializer(serializers.ModelSerializer):
    failure_node_name = serializers.CharField(source='failure_node.name', read_only=True)
    recovery_method_name = serializers.CharField(source='recovery_method.name', read_only=True)
    machine_serial = serializers.CharField(source='machine.serial_number', read_only=True)
    
    class Meta:
        model = Claim
        fields = '__all__'