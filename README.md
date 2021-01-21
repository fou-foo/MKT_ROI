# MKT_ROI

## Readme PROD 
Aplicativo para captura de información de los esfuerzos de MKT de Coppel. 


## Set up 

Basicamente segui esta [guía](https://codeburst.io/beginners-guide-to-deploying-a-django-postgresql-project-on-google-cloud-s-flexible-app-engine-e3357b601b91). 


Con PostgreSQL 12

-   500Gb de SSD
-   1 vCPU
-   3.75Gb RAM

El tipo (tamaño) de la maquina y capacidad en disco se pueden cambiar.

En Oregon, con backups de 12-4 am la clave del user `postgres` es `369analytics`, con el Cloud Shell.
En este punto se crea otro usser que es el que crea la applicación.

```bash 
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

Se instala y configura la [SDK](https://cloud.google.com/sdk/docs/quickstart#deb) de GCP.

Para configurar las variables de ambiente fui al penultimo paso del tutorial y se tubo que checar la parte de la conexion a la DB con el [SQL proxy](https://cloud.google.com/sql/docs/postgres/sql-proxy). Para lo cualse creo un service [account](https://cloud.google.com/sql/docs/postgres/sql-proxy#create-service-account) que genero el archivo  `mkt_roi_db_key.jason` y se prende con la linea:

Tuve que matar lo que estaba escuchando en mi local en la 127.0.0.1 
en particular el cupsd y cambiar el hostname de mi postgres local como dice [aqui](https://stackoverflow.com/a/64121220/5484791).


```bash 
sudo systemctl disable cups.socket cups.path cups.service
sudo systemctl kill --signal=SIGKILL cups.service
sudo systemctl stop cups.socket cups.path
gcloud init
gcloud auth login
./cloud_sql_proxy -instances=rmf2gcp:us-west1:mktroidb=tcp:5432
./cloud_sql_proxy -credential_file=/home/antonio/Desktop/GitHub/MKT_ROI/mkt_roi/mkt_roi/mkt_roi_db_key.json -instances=rmf2gcp:us-west1:mktroidb=tcp:5432
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












