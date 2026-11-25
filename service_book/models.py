from django.db import models
from django.contrib.auth.models import User

class Directory(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название")
    description = models.TextField(verbose_name="Описание", blank=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name

class TechniqueModel(Directory):
    class Meta:
        verbose_name = "Модель техники"
        verbose_name_plural = "Модели техники"

class EngineModel(Directory):
    class Meta:
        verbose_name = "Модель двигателя"
        verbose_name_plural = "Модели двигателя"

class TransmissionModel(Directory):
    class Meta:
        verbose_name = "Модель трансмиссии"
        verbose_name_plural = "Модели трансмиссии"

class DriveAxleModel(Directory):
    class Meta:
        verbose_name = "Модель ведущего моста"
        verbose_name_plural = "Модели ведущего моста"

class SteerAxleModel(Directory):
    class Meta:
        verbose_name = "Модель управляемого моста"
        verbose_name_plural = "Модели управляемого моста"

class MaintenanceType(Directory):
    class Meta:
        verbose_name = "Вид ТО"
        verbose_name_plural = "Виды ТО"

class FailureNode(Directory):
    class Meta:
        verbose_name = "Узел отказа"
        verbose_name_plural = "Узлы отказа"

class RecoveryMethod(Directory):
    class Meta:
        verbose_name = "Способ восстановления"
        verbose_name_plural = "Способы восстановления"

class MaintenanceOrganization(Directory):
    class Meta:
        verbose_name = "Организация, проводившая ТО"
        verbose_name_plural = "Организации, проводившие ТО"

class Machine(models.Model):
    serial_number = models.CharField(max_length=255, unique=True, verbose_name="Зав. № машины")
    technique_model = models.ForeignKey(TechniqueModel, on_delete=models.PROTECT, verbose_name="Модель техники")
    engine_model = models.ForeignKey(EngineModel, on_delete=models.PROTECT, verbose_name="Модель двигателя")
    engine_serial_number = models.CharField(max_length=255, verbose_name="Зав. № двигателя")
    transmission_model = models.ForeignKey(TransmissionModel, on_delete=models.PROTECT, verbose_name="Модель трансмиссии")
    transmission_serial_number = models.CharField(max_length=255, verbose_name="Зав. № трансмиссии")
    drive_axle_model = models.ForeignKey(DriveAxleModel, on_delete=models.PROTECT, verbose_name="Модель ведущего моста")
    drive_axle_serial_number = models.CharField(max_length=255, verbose_name="Зав. № ведущего моста")
    steer_axle_model = models.ForeignKey(SteerAxleModel, on_delete=models.PROTECT, verbose_name="Модель управляемого моста")
    steer_axle_serial_number = models.CharField(max_length=255, verbose_name="Зав. № управляемого моста")
    supply_contract = models.CharField(max_length=255, verbose_name="Договор поставки №, дата")
    shipment_date = models.DateField(verbose_name="Дата отгрузки с завода")
    consignee = models.CharField(max_length=255, verbose_name="Грузополучатель (конечный потребитель)")
    delivery_address = models.CharField(max_length=255, verbose_name="Адрес поставки (эксплуатации)")
    equipment = models.TextField(verbose_name="Комплектация (доп. опции)")
    client = models.ForeignKey(User, on_delete=models.PROTECT, related_name='client_machines', verbose_name="Клиент")
    service_company = models.ForeignKey(User, on_delete=models.PROTECT, related_name='service_machines', verbose_name="Сервисная компания")

    class Meta:
        verbose_name = "Машина"
        verbose_name_plural = "Машины"
        ordering = ['-shipment_date']

    def __str__(self):
        return self.serial_number

class Maintenance(models.Model):
    maintenance_type = models.ForeignKey(MaintenanceType, on_delete=models.PROTECT, verbose_name="Вид ТО")
    maintenance_date = models.DateField(verbose_name="Дата проведения ТО")
    operating_hours = models.IntegerField(verbose_name="Наработка, м/час")
    work_order_number = models.CharField(max_length=255, verbose_name="№ заказ-наряда")
    work_order_date = models.DateField(verbose_name="Дата заказ-наряда")
    organization = models.ForeignKey(MaintenanceOrganization, on_delete=models.PROTECT, verbose_name="Организация, проводившая ТО")
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE, related_name='maintenances', verbose_name="Машина")
    service_company = models.ForeignKey(User, on_delete=models.PROTECT, related_name='maintenance_service', verbose_name="Сервисная компания")

    class Meta:
        verbose_name = "ТО"
        verbose_name_plural = "ТО"
        ordering = ['-maintenance_date']

    def __str__(self):
        return f"{self.machine.serial_number} - {self.maintenance_type}"

class Claim(models.Model):
    failure_date = models.DateField(verbose_name="Дата отказа")
    operating_hours = models.IntegerField(verbose_name="Наработка, м/час")
    failure_node = models.ForeignKey(FailureNode, on_delete=models.PROTECT, verbose_name="Узел отказа")
    failure_description = models.TextField(verbose_name="Описание отказа")
    recovery_method = models.ForeignKey(RecoveryMethod, on_delete=models.PROTECT, verbose_name="Способ восстановления")
    spare_parts = models.TextField(verbose_name="Используемые запасные части")
    recovery_date = models.DateField(verbose_name="Дата восстановления")
    downtime = models.IntegerField(verbose_name="Время простоя техники", blank=True, null=True, editable=False)
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE, related_name='claims', verbose_name="Машина")
    service_company = models.ForeignKey(User, on_delete=models.PROTECT, related_name='claim_service', verbose_name="Сервисная компания")

    class Meta:
        verbose_name = "Рекламация"
        verbose_name_plural = "Рекламации"
        ordering = ['-failure_date']

    def save(self, *args, **kwargs):
        if self.recovery_date and self.failure_date:
            self.downtime = (self.recovery_date - self.failure_date).days
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.machine.serial_number} - {self.failure_node}"