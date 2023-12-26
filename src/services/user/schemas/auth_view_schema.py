from drf_spectacular.utils import extend_schema, OpenApiResponse


user_auth_schema = extend_schema(
    description='Autenticar a los usuarios con sus credenciales _correo electrónico_ y _contraseña_.',
    tags=['Usuarios'],
    auth=[],
    request={
        'application/json': {
            'required': [
                'email',
                'password'
            ],
            'properties': {
                'email': {
                    'type': 'string',
                    'maxLength': 100,
                    'nullable': False,
                    'pattern': '^([A-Za-z0-9]+[-_.])*[A-Za-z0-9]+@[A-Za-z]+(\.[A-Z|a-z]{2,4}){1,2}$',
                    'example': 'correo@example.com'
                },
                'password': {
                    'type': 'string',
                    'minLength': 8,
                    'maxLength': 30,
                    'nullable': False,
                    'example': 'Aaa1234567890'
                }
            }
        }
    },
    responses={
        200: OpenApiResponse(
            response={
                'properties': {
                    'access': {
                        'type': 'string',
                        'example': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY4MzIxNjU3NiwiaWF0IjoxNjgzMTMwMTc2LCJqdGkiOiI5NWJmOTE4ZmRiNjc0Y2ExYjVjNWRhMGE2OWZlYmE1MiIsInVzZXJfaWQiOjF9.PZPJ8kO-eO2Gyqr3COlVcw1n-55xWYNOgxpgorou5xE'
                    },
                    'refresh': {
                        'type': 'string',
                        'example': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY4MzIxNjU3NiwiaWF0IjoxNjgzMTMwMTc2LCJqdGkiOiI5NWJmOTE4ZmRiNjc0Y2ExYjVjNWRhMGE2OWZlYmE1MiIsInVzZXJfaWQiOjF9.PZPJ8kO-eO2Gyqr3COlVcw1n-55xWYNOgxpgorou5xE'
                    }
                }
            },
            description="(OK) La autenticación se completo con éxito, se crean los JWT para el usuario."
        ),
        401: OpenApiResponse(
            response={
                'properties': {
                    'detail': {
                        'type': 'string',
                        'example': 'No active account found with the given credentials'
                    }
                }
            },
            description='(UNAUTHORIZED) Las credenciales del usuario son inválidas o no existe un usuario con esas credenciales.'
        ),
        400: OpenApiResponse(
            response={
                'properties': {
                    'code_error': {
                        'type': 'string',
                        'example': 'invalid_data'
                    },
                    "details": {
                        'type': 'object',
                        'properties': {
                            'email': {
                                'type': 'array',
                                'items': {
                                    'type': 'string'
                                },
                                'example': [
                                    'Correo electrónico inválido.'
                                ]
                            },
                            'password': {
                                'type': 'array',
                                'items': {
                                    'type': 'string'
                                },
                                'example': [
                                    'El valor ingresado debe ser de al menos 8 caracteres.'
                                ]
                            }
                        }
                    }
                }
            },
            description='(BAD_REQUEST)  Los datos de la petición son inválidos, se retorna el/los mensajes de error por cada campo del formulario que no paso las validaciones:\n1. Campo email:\n  - **Correo electrónico inválido:** el correo electrónico debe tener una estructura válida, los siguientes ejemplos se consideran correos inválidos.\n    - correo@.com\n    - correo@[cualquier-número-simbolo].com\n    - correo.com\n    - correo@\n    - correo@example.[cualquier-número-simbolo]\n    - @.com\n  - **Este campo es requerido:** el correo electrónico del usuario debe ir en el cuerpo de la petición.\n  - **Este campo no puede estar en blanco:** no se admiten valores vacíos (\"\") para este campo.\n  - **Este correo electrónico ya está en uso:** no se admiten correos electrónicos duplicados en la base de datos.\n  - **El valor ingresado supera el número máximo de caracteres permitidos:** el máximo de caracteres permitido para este campo es de 90.\n2. campo password:\n  - **El valor ingresado debe ser de al menos 8 caracteres:** la contraseña debe ser de al menos 8 caracteres para ser considerada una contraseña segura.\n  - **Este campo es requerido:** la contraseña del usuario debe ir en el cuerpo de la petición.\n  - **Este campo no puede estar en blanco:** no se admiten valores vacíos (\"\") para este campo.\n'
        ),
        500: OpenApiResponse(
            description='(INTERNAL_SERVER_ERROR) Ocurrió un error al intentar intertar guardar el usuario en la base de datos, este error puede ser causado por las siguientes razones:\n1. Fallo en la conexión con la base de datos.\n2. El servidor no tiene los permisos necesarios para guardar el usuario.'
        ),
    }
)
