Estrategia de la Aplicación
===========================

La aplicación de django requiere el siguiente stack:

* Python
* uwsgi
* mysql
* nginx
* nfs

La configuración del server debe ser:
::
    [server-1]
    * python
    * uwsgi
    * mysql
    * nginx
    * nfs-server

    [server-2]
    * python
    * uwsgi
    * nginx
    * nfs-client

    [server-3]
    * python 
    * uwsgi
    * nginx
    * nfs-client

    [server-n]
     ..

Server 2 hasta N tendrian una configuracion de BD hacia server-1 y compartir la aplicación python y estaticos por medio del nfs.

Consideraciones
===============

server-1 es el nodo madre, si el server-1 cambia de configuracion entonces server-2,3,4 ..n deben cambiar tambien.

*Django*

La aplicación debe tener una configuración de BD que apunte al nodo1

*DNS*

Por eso: el DNS de round robin debe apuntar a todos los servers con excepcion de server-1

*NFS*

La aplicación se debe de poner un directorio, los archivos estaticos en otro. Todo por nfs, 


*Network*

Lo ideal es que los servers nodos esten dentro de la misma red, asi atravez de una ip privada de redlocal puedan comunicarse por nfs.

*Uwsgi*

Si hay un cambio de archivos en python, uwsgi debe reiniciarse automaticamente, esto lo hace atravez del touch-reload[1]. 
Al hacer el cambio en el nodo central el cambio se propagara por nfs.

[1]: http://uwsgi-docs.readthedocs.org/en/latest/Management.html#reloading-the-server


Riesgos en server-1
===================

Server-1 seria el centro de la aplicacion y server-2 hasta n serian nodos de server-1

En server-1 hay que tener en cuenta lo siguiente:

si server-1 se cae, hay que tener un server-1.1 listo para que lo remplaze en el menor tiempo posible.

por lo que server-1 no debe recibir peticiones para que no tengan stress y solo se encargue de distribuir la aplicación.


