from django.db import models
from .constants import AvailabilityType
import uuid


class BaseProperties(models.Model):
    """
    Abstract base model for properties.
    """
    
    id=models.UUIDField(
        db_column='id',
        default=uuid.uuid4,
        primary_key=True,
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
    rooms=models.IntegerField(
        db_column='rooms',
        db_index=True,
        null=False,
        blank=False,
    )
    bathrooms=models.IntegerField(
        db_column='bathrooms',
        db_index=True,
        null=False,
        blank=False,
    )
    floors=models.IntegerField(
        db_column='floors',
        db_index=True,
        null=False,
        blank=False,
    )
    ambient=models.JSONField(
        db_column='ambient',
        null=False,
        blank=False,
    )
    rules=models.JSONField(
        db_column='rules',
        null=False,
        blank=False,
    )
    location=models.CharField(
        db_column='location',
        max_length=100,
        unique=True,
        db_index=True,
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

    class Meta:
        abstract=True