from django.db import models
from . import base_property
from .constants import PropertyType


class Home(base_property.BaseProperties):
    """
    Model representing a Home property.
    """
    
    type_property=models.CharField(
        db_column='type_property',
        default=PropertyType.HOME.value,
        max_length=25,
    )
    garages=models.BooleanField(
        db_column='garages',
        db_index=True,
        null=False,
        blank=False,
    )
    garden=models.BooleanField(
        db_column='garden',
        db_index=True,
        null=False,
        blank=False,
    )
    extra_services=models.JSONField(
        db_column='extra_services',
        null=False,
        blank=False,
    )
    covered_meters=models.IntegerField(
        db_column='covered_meters',
        null=False,
        blank=False,
    )
    discovered_meters=models.IntegerField(
        db_column='discovered_meters',
        null=False,
        blank=False,
    )
    date_joined=models.DateTimeField(
        db_column='date_joined',
        auto_now_add=True,
        editable=False,
    )
    
    class Meta:
        db_table='home'
        verbose_name="home"
        verbose_name_plural="homes"
        ordering=['-date_joined']