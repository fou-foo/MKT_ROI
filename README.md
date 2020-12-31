# MKT_ROI
Aplicativo para captura de información de los esfuerzos de MKT de Coppel. 


## Set up 

En desarrollo estamos usando Ubuntu 20.04, en producción estamos usando Ubuntu 18.XX .

Vamos a usar PostgreSQL, aprovechando que ya se tiene en producción y pues es medio estándar en la industria. 

Installar PostgreSQL y set up Django en [dev.](https://www.digitalocean.com/community/tutorials/how-to-use-postgresql-with-your-django-application-on-ubuntu-14-04)

```bash 
sudo apt-get install postgresql postgresql-contrib
sudo su - postgres
psql
CREATE DATABASE mkt_roi;
CREATE USER cenic_mkt_roi WITH PASSWORD 'cenic_mkt_roi';
ALTER ROLE cenic_mkt_roi SET client_encoding TO 'utf8';
ALTER ROLE cenic_mkt_roi SET default_transaction_isolation TO 'read committed';
ALTER ROLE cenic_mkt_roi SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE mkt_roi TO cenic_mkt_roi;
\q
exit
```

En este punto hay que instalar Conda para administrar los [ambientes](https://docs.conda.io/projects/conda/en/latest/user-guide/install/linux.html).
Y continuamos creando el ambiente e instalando Django. 

El server de Euler de prod. tiene salida a internet y permite instalar conda sin problemas. 

```bash
conda create -n mkt_roi_env python=3.6
conda activate mkt_roi_env 
cd /home/euler/Desktop/Antonio/MKT_ROI # Creamos un folder para guardar el proyecto donde se pueda 
mkdir mkt_roi
cd mkt_roi/
conda install -c anaconda django
conda install -c anaconda psycopg2
pip install django-extensions
django-admin startproject mkt_roi
python manage.py startapp app
```

### Configurar el archivo `settings.py` del proyecto Django para la conexión con [Postgres](https://www.digitalocean.com/community/tutorials/how-to-use-postgresql-with-your-django-application-on-ubuntu-14-04)

Lo que podemeos hacer es copiar el archivo directo del repo cuidando los nombres y contraseñas. 

- Cambiar el idioma en el mismo archivo de `settings.py`

Y de una vez creamos el super admin de Django para Antonio 

```bash
python manage.py createsuperuser
antonio
antonio.garciar@coppel.com
pass: antonio.garciar
python manage.py runserver 0.0.0.0:8000 # test server 
```

El archivo MKT_ROI/mkt_roi/mkt_roi

```bash
python manage.py runscript users # LOS USERS LOS TUBE QUE CREAR CON LA UI DEL ADMIN












