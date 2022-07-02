from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import MinValueValidator, MaxValueValidator


class Client(models.Model):
    name = models.CharField(max_length=255, unique=True)

    objects = models.Manager()

    def __str__(self):
        return self.name

    @property
    def income(self):
        """ Сумма по счетам всех организаций клиента """
        return self.bills.aggregate(income=models.Sum('sum'))['income']


class Organization(models.Model):

    name = models.CharField(max_length=255, unique=True)
    client = models.ForeignKey(Client, on_delete=models.SET_NULL, blank=True, null=True, related_name='orgs')
    address = models.TextField(max_length=1000, default='', blank=True)
    fraud_weight = models.PositiveIntegerField(default=0)

    objects = models.Manager()

    class Meta:
        unique_together = ['name', 'client']

    def __str__(self):
        return self.name


class Service(models.Model):
    cls = models.PositiveSmallIntegerField(default=0, verbose_name='Service class')
    name = models.CharField(max_length=255)

    objects = models.Manager()

    def __str__(self):
        return f'{self.cls}: {self.name}'


class Bill(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='bills')
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='bills')
    number = models.PositiveIntegerField()
    sum = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    service = models.ForeignKey(Service, on_delete=models.SET_NULL, blank=True, null=True)
    fraud_score = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(1)])

    objects = models.Manager()

    class Meta:
        unique_together = ['organization', 'number']
        ordering = ['organization', 'client', 'number']

    def __str__(self):
        return f'{self.organization} (bill {self.number})'


@receiver(post_save, sender=Bill)
def update_fraud_weight(sender, instance, **kwargs):
    """ Увеличивает fraud_weight организации в зависимости от fraud_score сохраненного счета """
    if instance.fraud_score >= 0.9:
        org = instance.organization
        current_weight = org.fraud_weight
        instance.organization.fraud_weight = current_weight + 1
        org.save()
