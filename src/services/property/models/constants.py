from enum import Enum


class AvailabilityType(Enum):
    BUY='Compra'
    RENT='Alquiler'
    TEMPORARY_RENTAL='Alquiler temporal'

class PropertyType(Enum):
    HOME='Casa'
    DEPARTMENT='Departamento'
    LOCAL='Local'

class LocalType(Enum):
    COMERCIAL='Comercial'
    INDUSTRIAL='Industrial'

class QueryParams(Enum):
    STR_FIELDS=['availability_type', 'type_local']
    INTEGER_FIELDS=['rooms', 'bathrooms', 'floors']
    BOOLEAN_FIELDS=['all', 'parking_lot', 'garages', 'garden']
    PRICE_FIELDS=['price_usd']