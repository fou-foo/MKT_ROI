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
ALTER USER cenic_mkt_roi WITH CREATEDB;
GRANT ALL PRIVILEGES ON DATABASE mkt_roi TO cenic_mkt_roi;
ALTER USER cenic_mkt_roi WITH SUPERUSER; # para limpiar la DB del desmadre que hice con los modelos
\q
exit
```

En este punto hay que instalar Conda para administrar los [ambientes](https://docs.conda.io/projects/conda/en/latest/user-guide/install/linux.html).
Y continuamos creando el ambiente e instalando Django. 

El server de Euler de prod. tiene salida a internet y permite instalar conda sin problemas. 

```bash
wget https://repo.anaconda.com/archive/Anaconda3-2020.11-Linux-x86_64.sh # bajar conda de los repos del desarrollador
bash Anaconda-*.sh
conda config --set auto_activate_base false # desintalar el enviroment base

conda create -n mkt_roi_env python=3.6
conda activate mkt_roi_env 
cd /home/euler/Desktop/Antonio/MKT_ROI # Creamos un folder para guardar el proyecto donde se pueda en PROD
mkdir mkt_roi
cd mkt_roi/
conda install -c anaconda django
conda install -c anaconda psycopg2
#pip install django-extensions
conda install -c conda-forge django-extensions
conda install -c conda-forge numpy
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc"  -delete
python manage.py reset_db # borrar la base 
python manage.py flush 
# copiar el repo 
python manage.py makemigrations 
python manage.py migrate 
python manage.py runscript users # luego asignar los users manualmente en la vista dle admin -_-
#django-admin startproject mkt_roi
#python manage.py startapp app

 # reset db despues de cambios en  los modleos 
```

### Configurar el archivo `settings.py` del proyecto Django para la conexión con [Postgres](https://www.digitalocean.com/community/tutorials/how-to-use-postgresql-with-your-django-application-on-ubuntu-14-04)

Y de una vez creamos el super admin de Django para Antonio 

```bash
python manage.py createsuperuser
antonio
antonio.garciar@coppel.com
pass: antonio.garciar
python manage.py runserver 0.0.0.0:8000 # test server y lo vemos en la http://10.26.53.54:8000/admin/

l archivo MKT_ROI/mkt_roi/mkt_roi

```bash
python manage.py runscript users # LOS USERS LOS TUBE QUE CREAR CON LA UI DEL ADMIN












