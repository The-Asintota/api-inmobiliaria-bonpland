from django.db import models
from .constants import AvailabilityType, PropertyType, LocalType
import uuid


class Local(models.Model):
    """
    Model representing a Local property.
    """
    
    id=models.UUIDField(
        db_column='id',
        default=uuid.uuid4,
        primary_key=True,
    )
    type_property=models.CharField(
        db_column='type_property',
        default=PropertyType.LOCAL.value,
        max_length=25,
    )
    availability_type=models.CharField(
        db_column='availability_type',
        choices=[
            (AvailabilityType.BUY.value, AvailabilityType.BUY.value),
            (AvailabilityType.RENT.value, AvailabilityType.RENT.value),
            (AvailabilityType.TEMPORARY_RENTAL.value, AvailabilityType.TEMPORARY_RENTAL.value),
        ],
        max_length=25,
        db_index=True,
        null=False,
        blank=False,
    )
    short_description=models.TextField(
        db_column='short_description',
        max_length=50,
        null=False,
        blank=False,
    )
    long_description=models.TextField(
        db_column='long_description',
        max_length=200,
        null=False,
        blank=False,
    )
    type_local=models.CharField(
        db_column='type_local',
        choices=[
            (LocalType.COMERCIAL.value, LocalType.COMERCIAL.value),
            (LocalType.INDUSTRIAL.value, LocalType.INDUSTRIAL.value)
        ],
        max_length=25,
        db_index=True,
        null=False,
        blank=False,
    )
    extra_services=models.JSONField(
        db_column='extra_services',
        null=False,
        blank=False,
    )
    use=models.JSONField(
        db_column='use',
        null=False,
        blank=False,
    )
    parking_lot=models.BooleanField(
        db_column='parking_lot',
        db_index=True,
        default=False,
    )
    location=models.CharField(
        db_column='location',
        max_length=100,
        unique=True,
        db_index=True,
        null=False,
        blank=False,
    )
    location_in=models.CharField(
        db_column='location_in',
        max_length=100,
        null=False,
        blank=False,
    )
    price_usd = models.DecimalField(
        db_column='price_usd',
        max_digits=10,
        decimal_places=2,
        db_index=True,
        null=False,
        blank=False,
    )
    date_joined=models.DateTimeField(
        db_column='date_joined',
        auto_now_add=True,
        editable=False,
    )

    class Meta:
        db_table='local'
        verbose_name="local"
        verbose_name_plural="local"
        ordering=['-date_joined']