# Repositorio api inmobiliaria Bonpland

## 1. Descripción

Este repositorio alberga el código fuente del backend para la plataforma de gestión de inmobiliaria **_Bonpland_**. Para desarrollar este backend nos hemos apoyado de un marco de trabajo muy potentes conocido como [Django Rest](https://www.django-rest-framework.org/).

Este framework nos permite construir poderosas API web de manera rápida y fácil, siendo este un marco de trabajo de alto nivel en [Python](https://www.python.org/) que fomenta un diseño limpio y pragmático en el desarrollo.

### 1.1. Estructura
La estructura del proyecto es la siguiente:

```
└── 📁src
    └── 📁backend
        └── asgi.py
        └── 📁settings
            └── base.py
            └── local.py
            └── production.py
            └── __init__.py
        └── urls.py
        └── wsgi.py
        └── __init__.py
    └── manage.py
    └── requirements.txt
    └── 📁services
        └── __init__.py
    └── 📁test
        └── __init__.py
```

Esta estructura representa la organización de los archivos y directorios del proyecto. El directorio _src_ es el directorio raíz del proyecto. Contiene el directorio _backend_ para la configuración general de toda la API y el directorio de _services_ para las aplicaciones Django.

El directorio _backend_ es el núcleo de la aplicación y contiene la configuración de Django, las configuraciones de URL y las aplicaciones WSGI y ASGI. El directorio de configuración dentro del backend se divide en diferentes configuraciones para diferentes entornos (base, local, producción).

El directorio _services_ contiene las aplicaciones Django que contendrán la lógica empresarial y los puntos finales. Internamente, el árbol de archivos de cada aplicación sigue los principios de una arquitectura en capas. Esta separación de preocupaciones permite una mejor mantenibilidad y escalabilidad del código, ya que los cambios en una capa no afectan a las demás.

El directorio _test_ contendrá las pruebas unitarias necesarias para cada aplicación Django o servicios de la API.

El script _manage.py_ se utiliza para administrar el proyecto Django, incluidas tareas como migraciones de bases de datos y el inicio del servidor. El archivo _requirements.txt_ enumera las dependencias de Python necesarias para el proyecto, lo que garantiza que todos los paquetes necesarios estén instalados para que la aplicación se ejecute correctamente.

## 2. Instalación en local

Primero debes clonar este repositorio utilizando el siguiente comando en tu consola.

```bash
  git clone https://github.com/The-Asintota/api-inmobiliaria-bonpland.git
```

- **Paso 1 (requerimientos):** asegúrese de que Python esté instalado en su sistema operativo.

- **Paso 2 (instalar dependencias):** para instalar las teconologias y paquetes que usa el proyecto usa el siguiente comando. Asegurate de estar dentro de la carpeta _src_.

    ```bash
    pip install -r "requirements.txt"
    ```

- **Paso 3 (configurar variables de entorno):** se debe crear un archivo con el nombre _.env_ dentro de la carpeta _src_. Dentro de este archivo se definiran todas las variables de entorno de este proyecto.

    ```bash
    ENVIRONMENT_STATUS='development'
    KEY_DJANGO='value'
    ```

    El valor de la variable _KEY_DJANGO_ lo puedes obtener ejecutando los siguientes comandos. El ultimo comando retorna el valor de la variable que deberas copiar en el archivo _.env_.

    ```bash
    #Primer comando
    python

    #Segundo comando
    from django.core.management.utils import get_random_secret_key; print(get_random_secret_key()); exit()
    ```

- **Paso 4 (realizar migraciones):** migramos los modelos del proyecto necesarios para el funcionamiento del servidor con el siguiente comando.

    ```bash
    python manage.py migrate
    ```

- **Paso 5 (Iniciar el servidor):** para iniciar el servidor de manera local ejecuta el siguiente comando.

    ```bash
    python manage.py runserver
    ```

## 3. Tests
Para correr las pruebas unitarias del código ejecuta el siguiente comando.

```bash
python manage.py test
```

## 4. Integrantes del repositorio
- [Carlos Andres Aguirre](https://github.com/The-Asintota)