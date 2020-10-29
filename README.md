
<p align="center">
  <img src="https://2.bp.blogspot.com/-p12HxfQddqg/Vg9qgr--eqI/AAAAAAAAAFA/66wfGkfqkd8/w1200-h630-p-k-no-nu/evento%2Blogo%2B%257Bevent%2Bproduction.jpg" width="150">
  <br />
  <br />

--------------------------------------------------------------------------------

Event Organizer es un proyecto que busca organizar a los invitados de un evento de manera que su ingreso sea semi-automático haciendo uso de códigos QR los cuales son de uso único. Estos son escaneados por seguridad y permiten el ingreso. Además el proyecto incluye pagina administrativa personalizada, pagina promoción del evento y tarjetas virtuales.



### What's New:

- First Release October 2020: [First Release](//github.com/cettipao/ProyectoFinal)


### Features:

- Openpyxl para descargar Excel de invitados
- Ajax para consultas al Backend
- Templates HTML de W3layouts
- Twilio para bot de Whatsapp:

```python
from django_twilio.decorators import twilio_view
from twilio.twiml.messaging_response import MessagingResponse,Message

@twilio_view
def smsView(request):
...
```
Documentacion de  [django-twilio](https://django-twilio.readthedocs.io/en/latest/)

# Requirements and Installation

| Paquetes | Version |
|:---|:---:|
| certifi| 2020.6.20 |
| Django| 2.2|
| django-jet| 1.0.8|
| django-phonenumber-field| 5.0.0|
| django-twilio| 0.13.0.post1|
| et-xmlfile| 1.0.1|
| gunicorn| 20.0.4|
| idna| 2.10|
| jdcal| 1.4.1|
| openpyxl| 3.0.5|
| phonenumbers| 8.12.11|
| Pillow| 8.0.0|
| PyJWT| 1.7.1|
| pytz| 2020.1|
| qrcode| 6.1|
| requests| 2.24.0|
| six| 1.15.0|
| sqlparse| 0.4.1|
| twilio| 6.46.0|
| urllib3| 1.25.10|
| whitenoise| 5.2.0|


* **To install requirements.txt** in a virtualenv:
```bash
pip install -r requirements.txt
```


# Getting Started

### Instalacion

#### Descarga de archivos de repositorio

Para descargar los archivos de este repositorio tendremos que ejecutar los siguientes comandos en terminal
```
git init

git clone https://github.com/cettipao/ProyectoFinal.git
```

## Built With

* [Python](https://www.python.org/)
* [Django](https://www.djangoproject.com/)
* [Twilio](https://twilio.com/)
* [Materialize](https://materializecss.com/)
* [JavaScript](https://www.javascript.com/)
* [AJAX](https://api.jquery.com/jquery.ajax/)
* [Bootstrap](https://getbootstrap.com/)
# License

Bajo el Colegio [ITS Villada](https://www.itsv.edu.ar/)

