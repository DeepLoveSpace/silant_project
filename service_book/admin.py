from django.contrib import admin
from .models import *

admin.site.register(TechniqueModel)
admin.site.register(EngineModel)
admin.site.register(TransmissionModel)
admin.site.register(DriveAxleModel)
admin.site.register(SteerAxleModel)
admin.site.register(MaintenanceType)
admin.site.register(FailureNode)
admin.site.register(RecoveryMethod)
admin.site.register(MaintenanceOrganization)

@admin.register(Machine)
class MachineAdmin(admin.ModelAdmin):
    list_display = ('serial_number', 'technique_model', 'client', 'shipment_date')
    list_filter = ('technique_model', 'engine_model', 'transmission_model')
    search_fields = ('serial_number',)

@admin.register(Maintenance)
class MaintenanceAdmin(admin.ModelAdmin):
    list_display = ('machine', 'maintenance_type', 'maintenance_date')
    list_filter = ('maintenance_type', 'service_company')
    search_fields = ('machine__serial_number',)

@admin.register(Claim)
class ClaimAdmin(admin.ModelAdmin):
    list_display = ('machine', 'failure_date', 'recovery_date', 'downtime')
    list_filter = ('failure_node', 'recovery_method')
    search_fields = ('machine__serial_number',)