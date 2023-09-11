# Universal Payments

Este repositorio contiene un proyecto desarrollado en Django que integra múltiples plataformas de pago en un solo lugar y facilita la integración de dichas plataformas para otros desarrolladores, ofreciéndoles una documentación donde se explica el proceso desde la creación de su cuenta en cada plataforma de pago ofrecida por este proyecto, hasta la integración con nuestra API que actúa de intermediaria y abstrae gran parte del funcionamiento, evitando largas horas a los desarrolladores de lectura de extensas documentaciones e iteraciones de prueba y error.

## Instalación

1. Clonar el repositorio en tu máquina local
2. Dirigirse al directorio del proyecto
3. Crear un entorno virtual de python3
python3 -m venv .venv
4. Activar el entorno virtual
En Windows:
.venv\Scripts\activate

En macOS/Linux:
source .venv/bin/activate
5. Instalar las dependencias requeridas
pip install -r requirements.txt
6. Realiza rlas migraciones iniciales de la base de datos
python manage.py migrate oauth2_provider
python manage.py migrate
7. Iniciar el servidor de desarrollo de Django
python manage.py runserver