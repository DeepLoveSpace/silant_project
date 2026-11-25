from django import forms
from .models import Machine, Maintenance, Claim, MaintenanceOrganization
from django.contrib.auth.models import User

class MachineForm(forms.ModelForm):
    class Meta:
        model = Machine
        fields = '__all__'
        widgets = {
            'shipment_date': forms.DateInput(attrs={'type': 'date'}),
            'equipment': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['client'].queryset = User.objects.filter(groups__name='Клиент')
        self.fields['service_company'].queryset = User.objects.filter(groups__name='Сервисная организация')

class MaintenanceForm(forms.ModelForm):
    class Meta:
        model = Maintenance
        fields = [
            'maintenance_type', 'maintenance_date', 'operating_hours', 
            'work_order_number', 'work_order_date', 'organization', 
            'machine'
        ]
        widgets = {
            'maintenance_date': forms.DateInput(attrs={'type': 'date'}),
            'work_order_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        if user and user.groups.filter(name='Клиент').exists():
            self.fields['machine'].queryset = Machine.objects.filter(client=user)
        elif user and user.groups.filter(name='Сервисная организация').exists():
            self.fields['machine'].queryset = Machine.objects.filter(service_company=user)

class ClaimForm(forms.ModelForm):
    class Meta:
        model = Claim
        fields = [
            'failure_date', 'operating_hours', 'failure_node', 
            'failure_description', 'recovery_method', 'spare_parts', 
            'recovery_date', 'machine'
        ]
        widgets = {
            'failure_date': forms.DateInput(attrs={'type': 'date'}),
            'recovery_date': forms.DateInput(attrs={'type': 'date'}),
            'failure_description': forms.Textarea(attrs={'rows': 3}),
            'spare_parts': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        if user and user.groups.filter(name='Сервисная организация').exists():
            self.fields['machine'].queryset = Machine.objects.filter(service_company=user)