# Rama main

  __A partir de una [junta](https://meet.google.com/srq-yenw-wjk) el 8 de enero se decidió que el aplicativo no vivirá en Euler porque los usuarios del mismo no tienen VPNs ni VPIs por lo que no tienen acceso a la red de Coppel mientras esta la curentena del Covid-19 por lo que debemos de mover la aplicación a un ip pública.__

Esta rama la utilizaremos como rama de desarrollo, como no tenemos ambiente de producción los desarrollos seran locales, los cambios en esta rama ojala y se hagan con PRs cuando más de una persona colaboré. 

La idea es que despues de tener probados y testeados los cambios en local se muevan en alguna de las ramas que se creen, para producción. 

Hay varias ramas de producción pues ha la fecha no hay ambiente ni recursos fijos destinados para mantener el aplicativo y por eso se estan explorando varias opciones. 

# MKT_ROI
Aplicativo para captura de información de los esfuerzos de MKT de Coppel. 


## Set up 

En desarrollo estamos usando Ubuntu 20.04.


Vamos a usar PostgreSQL, aprovechando que ya la gente de CENIC ya esta familiarizada con él y es medio estándar en la industria. 

Installar PostgreSQL y set up Django en [dev.](https://www.digitalocean.com/community/tutorials/how-to-use-postgresql-with-your-django-application-on-ubuntu-14-04)

Vamos a crear una DB y un usuario dentro de ella con password fijo para ahorrarnos algo de pelea entre ambientes. 

```bash 
sudo apt-get install postgresql postgresql-contrib
sudo su - postgres
psql
# vamos a crear la DB y el usuario que servira en todas partes
CREATE DATABASE mkt_roi;
CREATE USER cenic_mkt_roi WITH PASSWORD 'cenic_mkt_roi';
ALTER ROLE cenic_mkt_roi SET client_encoding TO 'utf8';
ALTER ROLE cenic_mkt_roi SET default_transaction_isolation TO 'read committed';
ALTER ROLE cenic_mkt_roi SET timezone TO 'UTC';
ALTER USER cenic_mkt_roi WITH CREATEDB;
GRANT ALL PRIVILEGES ON DATABASE mkt_roi TO cenic_mkt_roi;
ALTER USER cenic_mkt_roi WITH SUPERUSER; # para limpiar la DB al alterar los modelos en Django
\q
exit
```

En este punto hay que instalar Conda para administrar los [ambientes](https://docs.conda.io/projects/conda/en/latest/user-guide/install/linux.html).
Y continuamos creando el ambiente e instalando Django. 


```bash
wget https://repo.anaconda.com/archive/Anaconda3-2020.11-Linux-x86_64.sh # bajar conda de los repos del desarrollador
bash Anaconda-*.sh
conda config --set auto_activate_base false # desintalar el enviroment base
conda create -n mkt_roi_env python=3.6
conda activate mkt_roi_env 
cd /home/antonio/Desktop/GitHub/MKT_ROI # Creamos un folder para guardar el proyecto donde se pueda 
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
django-admin startproject mkt_roi
python manage.py startapp app
# copiar el repo 
git clone https://github.com/fou-foo/MKT_ROI.git
# aqui igual y tienen problemas al sobre escribir archivos confien en mi y quedense con los del repo ya esta listo 
python manage.py makemigrations 
python manage.py migrate 
python manage.py runscript users 
# reset db despues de cambios en  los modleos 
```
Y de una vez creamos el super admin de Django para Antonio 

```bash
python manage.py createsuperuser
christian
christian.barradas@coppel.com
pass: christian.barradas
alejandro
alejandro.ahedo@coppel.com
pass: alejandro.ahedo
python manage.py runserver 
```




__Este paso ya esta echo en el repo, pero lo incluyo por si a caso__

 Configurar el archivo `settings.py` del proyecto Django para la conexión con [Postgres](https://www.digitalocean.com/community/tutorials/how-to-use-postgresql-with-your-django-application-on-ubuntu-14-04)


## Dependencias del enviroment `mkt_roi_env`

Las guardamos porque en la rama `prod`, vamos a crear variables de ambiente sobre este ambiente así que ocupamos crear otro otro base llamado `mkt_roi` (lo siento no vi venir esto).  

```bash 
conda list --name mkt_roi_env --explicit > requirementes_conda_env_dev.txt
conda create -n mkt_roi --file requirementes_conda_env_dev.txt
```


```bash
#comandos utiles 
fuser -n tcp -k 8000
sudo lsof -i -P -n | grep LISTEN
service nginx stop 
```




