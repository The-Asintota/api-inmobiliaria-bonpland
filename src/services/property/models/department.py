from django.db import models
from . import base_property
from .constants import PropertyType


class Department(base_property.BaseProperties):
    """
    Model representing a Department property.
    """
    
    type_property=models.CharField(
        db_column='type_property',
        default=PropertyType.DEPARTMENT.value,
        max_length=25,
    )
    covered_meters=models.DecimalField(
        db_column='covered_meters',
        max_digits=5,
        decimal_places=2,
        null=False,
        blank=False,
    )
    extra_services=models.JSONField(
        db_column='extra_services',
        null=False,
        blank=False,
    )
    building_services=models.JSONField(
        db_column='building_services',
        null=False,
        blank=False,
    )
    date_joined=models.DateTimeField(
        db_column='date_joined',
        auto_now_add=True,
        editable=False,
    )
    
    class Meta:
        db_table='department'
        verbose_name="department"
        verbose_name_plural="departments"
        ordering=['-date_joined']