from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import User

from .models import (
    Machine, Maintenance, Claim,
    TechniqueModel, EngineModel, TransmissionModel,
    DriveAxleModel, SteerAxleModel,
    MaintenanceType, FailureNode, RecoveryMethod
)
from .forms import MachineForm, MaintenanceForm, ClaimForm

def index(request):
    machine = None
    search_query = request.GET.get('serial_number', '').strip()
    
    if search_query:
        try:
            machine = Machine.objects.get(serial_number__iexact=search_query)
        except Machine.DoesNotExist:
            machine = 'not_found'
        except Machine.MultipleObjectsReturned:
            machine = Machine.objects.filter(serial_number__iexact=search_query).first()
            
    return render(request, 'service_book/index.html', {
        'machine': machine, 
        'search_query': search_query
    })

def check_permission(user, action_type):
    """Проверяет права пользователя согласно таблице ролей из ТЗ."""
    is_manager = user.groups.filter(name='Менеджер').exists()
    is_service = user.groups.filter(name='Сервисная организация').exists()
    is_client = user.groups.filter(name='Клиент').exists()

    if action_type == 'machine':
        return is_manager
    if action_type == 'maintenance':
        return is_manager or is_service or is_client
    if action_type == 'claim':
        return is_manager or is_service
    return False

@login_required
def dashboard(request):
    user = request.user
    
    is_manager = user.groups.filter(name='Менеджер').exists()
    is_client = user.groups.filter(name='Клиент').exists()
    is_service = user.groups.filter(name='Сервисная организация').exists()

    if is_manager:
        machines_qs = Machine.objects.all()
        maintenances_qs = Maintenance.objects.all()
        claims_qs = Claim.objects.all()
    elif is_client:
        machines_qs = Machine.objects.filter(client=user)
        maintenances_qs = Maintenance.objects.filter(machine__client=user)
        claims_qs = Claim.objects.filter(machine__client=user)
    elif is_service:
        machines_qs = Machine.objects.filter(service_company=user)
        maintenances_qs = Maintenance.objects.filter(machine__service_company=user)
        claims_qs = Claim.objects.filter(machine__service_company=user)
    else:
        machines_qs = Machine.objects.none()
        maintenances_qs = Maintenance.objects.none()
        claims_qs = Claim.objects.none()

    if request.GET.get('tech_model'): machines_qs = machines_qs.filter(technique_model__id=request.GET.get('tech_model'))
    if request.GET.get('engine_model'): machines_qs = machines_qs.filter(engine_model__id=request.GET.get('engine_model'))
    if request.GET.get('trans_model'): machines_qs = machines_qs.filter(transmission_model__id=request.GET.get('trans_model'))
    if request.GET.get('drive_axle'): machines_qs = machines_qs.filter(drive_axle_model__id=request.GET.get('drive_axle'))
    if request.GET.get('steer_axle'): machines_qs = machines_qs.filter(steer_axle_model__id=request.GET.get('steer_axle'))

    if request.GET.get('to_type'): maintenances_qs = maintenances_qs.filter(maintenance_type__id=request.GET.get('to_type'))
    if request.GET.get('to_machine'): maintenances_qs = maintenances_qs.filter(machine__serial_number=request.GET.get('to_machine'))
    if request.GET.get('to_service'): maintenances_qs = maintenances_qs.filter(service_company__id=request.GET.get('to_service'))

    if request.GET.get('claim_node'): claims_qs = claims_qs.filter(failure_node__id=request.GET.get('claim_node'))
    if request.GET.get('claim_recovery'): claims_qs = claims_qs.filter(recovery_method__id=request.GET.get('claim_recovery'))
    if request.GET.get('claim_service'): claims_qs = claims_qs.filter(service_company__id=request.GET.get('claim_service'))

    current_tab = request.GET.get('tab', 'machines')
    sort_by = request.GET.get('sort', 'desc')

    if current_tab == 'machines':
        machines_qs = machines_qs.order_by('shipment_date' if sort_by == 'asc' else '-shipment_date')
    elif current_tab == 'to':
        maintenances_qs = maintenances_qs.order_by('maintenance_date' if sort_by == 'asc' else '-maintenance_date')
    elif current_tab == 'claims':
        claims_qs = claims_qs.order_by('failure_date' if sort_by == 'asc' else '-failure_date')

    context = {
        'machines': machines_qs,
        'maintenances': maintenances_qs,
        'claims': claims_qs,
        'is_manager': is_manager,
        'is_client': is_client,
        'is_service': is_service,
        'current_tab': current_tab,
        'current_sort': sort_by,
        'tech_models': TechniqueModel.objects.all(),
        'engine_models': EngineModel.objects.all(),
        'trans_models': TransmissionModel.objects.all(),
        'drive_axles': DriveAxleModel.objects.all(),
        'steer_axles': SteerAxleModel.objects.all(),
        'to_types': MaintenanceType.objects.all(),
        'machines_for_filter': machines_qs.values_list('serial_number', flat=True).distinct(),
        'service_users': User.objects.filter(groups__name='Сервисная организация'),
        'claim_nodes': FailureNode.objects.all(),
        'recovery_methods': RecoveryMethod.objects.all(),
        'current_filters': request.GET
    }
    return render(request, 'service_book/dashboard.html', context)

@login_required
def machine_detail(request, pk):
    machine = get_object_or_404(Machine, pk=pk)
    user = request.user
    
    if user.groups.filter(name='Клиент').exists() and machine.client != user:
        raise PermissionDenied("У вас нет доступа к этой машине.")
    if user.groups.filter(name='Сервисная организация').exists() and machine.service_company != user:
        raise PermissionDenied("У вас нет доступа к этой машине.")
        
    return render(request, 'service_book/machine_detail.html', {
        'machine': machine,
        'is_manager': user.groups.filter(name='Менеджер').exists(),
        'is_service': user.groups.filter(name='Сервисная организация').exists(),
        'is_client': user.groups.filter(name='Клиент').exists(),
    })

@login_required
def maintenance_detail(request, pk):
    maintenance = get_object_or_404(Maintenance, pk=pk)
    user = request.user
    
    if user.groups.filter(name='Клиент').exists() and maintenance.machine.client != user:
        raise PermissionDenied("У вас нет доступа к этому ТО.")
    if user.groups.filter(name='Сервисная организация').exists() and maintenance.machine.service_company != user:
        raise PermissionDenied("У вас нет доступа к этому ТО.")
        
    return render(request, 'service_book/maintenance_detail.html', {
        'maintenance': maintenance,
        'is_manager': user.groups.filter(name='Менеджер').exists(),
        'is_service': user.groups.filter(name='Сервисная организация').exists(),
        'is_client': user.groups.filter(name='Клиент').exists(),
    })

@login_required
def claim_detail(request, pk):
    claim = get_object_or_404(Claim, pk=pk)
    user = request.user
    
    if user.groups.filter(name='Клиент').exists() and claim.machine.client != user:
        raise PermissionDenied("У вас нет доступа к этой рекламации.")
    if user.groups.filter(name='Сервисная организация').exists() and claim.machine.service_company != user:
        raise PermissionDenied("У вас нет доступа к этой рекламации.")
        
    return render(request, 'service_book/claim_detail.html', {
        'claim': claim,
        'is_manager': user.groups.filter(name='Менеджер').exists(),
        'is_service': user.groups.filter(name='Сервисная организация').exists(),
        'is_client': user.groups.filter(name='Клиент').exists(),
    })

@login_required
def machine_create(request):
    if not check_permission(request.user, 'machine'):
        raise PermissionDenied("У вас нет прав на это действие.")
    
    if request.method == 'POST':
        form = MachineForm(request.POST)
        if form.is_valid():
            machine = form.save()
            return redirect('machine_detail', pk=machine.pk)
    else:
        form = MachineForm()
    return render(request, 'service_book/form_template.html', {
        'form': form, 
        'title': 'Добавить машину'
    })

@login_required
def machine_edit(request, pk):
    if not check_permission(request.user, 'machine'):
        raise PermissionDenied("У вас нет прав на это действие.")
    
    machine = get_object_or_404(Machine, pk=pk)
    if request.method == 'POST':
        form = MachineForm(request.POST, instance=machine)
        if form.is_valid():
            form.save()
            return redirect('machine_detail', pk=machine.pk)
    else:
        form = MachineForm(instance=machine)
    return render(request, 'service_book/form_template.html', {
        'form': form, 
        'title': f'Редактировать машину {machine.serial_number}'
    })

@login_required
def maintenance_create(request):
    if not check_permission(request.user, 'maintenance'):
        raise PermissionDenied("У вас нет прав на это действие.")
    
    if request.method == 'POST':
        form = MaintenanceForm(request.POST, user=request.user)
        if form.is_valid():
            maintenance = form.save(commit=False)
            maintenance.service_company = maintenance.machine.service_company
            maintenance.save()
            return redirect('maintenance_detail', pk=maintenance.pk)
    else:
        form = MaintenanceForm(user=request.user)
    return render(request, 'service_book/form_template.html', {
        'form': form, 
        'title': 'Добавить ТО'
    })

@login_required
def maintenance_edit(request, pk):
    if not check_permission(request.user, 'maintenance'):
        raise PermissionDenied("У вас нет прав на это действие.")
    
    maintenance = get_object_or_404(Maintenance, pk=pk)
    if request.method == 'POST':
        form = MaintenanceForm(request.POST, instance=maintenance, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('maintenance_detail', pk=maintenance.pk)
    else:
        form = MaintenanceForm(instance=maintenance, user=request.user)
    return render(request, 'service_book/form_template.html', {
        'form': form, 
        'title': f'Редактировать ТО для {maintenance.machine.serial_number}'
    })

@login_required
def claim_create(request):
    if not check_permission(request.user, 'claim'):
        raise PermissionDenied("У вас нет прав на это действие.")
    
    if request.method == 'POST':
        form = ClaimForm(request.POST, user=request.user)
        if form.is_valid():
            claim = form.save(commit=False)
            claim.service_company = claim.machine.service_company
            claim.save()
            return redirect('claim_detail', pk=claim.pk)
    else:
        form = ClaimForm(user=request.user)
    return render(request, 'service_book/form_template.html', {
        'form': form, 
        'title': 'Добавить рекламацию'
    })

@login_required
def claim_edit(request, pk):
    if not check_permission(request.user, 'claim'):
        raise PermissionDenied("У вас нет прав на это действие.")
    
    claim = get_object_or_404(Claim, pk=pk)
    if request.method == 'POST':
        form = ClaimForm(request.POST, instance=claim, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('claim_detail', pk=claim.pk)
    else:
        form = ClaimForm(instance=claim, user=request.user)
    return render(request, 'service_book/form_template.html', {
        'form': form, 
        'title': f'Редактировать рекламацию для {claim.machine.serial_number}'
    })