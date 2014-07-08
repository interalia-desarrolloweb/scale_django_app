Separar Aplicación
==================

La aplicación de django requiere el siguiente stack:

* Python
* uwsgi
* mysql
* nginx
* nfs

La configuración del server debe ser:

.. code:: none
    [server-1]
    * python
    * uwsgi
    * mysql
    * nginx

    [server-2]
    * python
    * uwsgi
    * nginx

    [server-3]
    * python 
    * uwsgi
    * nginx

    [server-n]
     ..


