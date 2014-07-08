Introducción
============

Este documento propone una forma de realizar una aplicación django pueda ser escalable horizontalmente.

Los requerimientos de la aplicación es dínamica, osea que no podemos usar:

varnish.

La estrategía es escalar horizontalmente, agregando nodos hijos de un nodo central

El cual consiste en tecnicas:

* DNS round-robin
* Separar aplicación en app y BD
* Provising
* Rackspace

DNS
===

El primer paso para escalar es configurar el dns con roundrobin

Esto quiere decir que se apuntara el dominio a varias IP cada una por server.
Lo que hara es que cada vez que se resuelva la dirección ip de un dominio podra dar 
alguno registro alterno.

.. code-block:: bash

    zodman  $  dig midominio.com

    ; <<>> DiG 9.9.5-3-Ubuntu <<>> midominio.com
    ;; global options: +cmd
    ;; Got answer:
    ;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 37150
    ;; flags: qr rd ra; QUERY: 1, ANSWER: 2, AUTHORITY: 0, ADDITIONAL: 1

    ;; OPT PSEUDOSECTION:
    ; EDNS: version: 0, flags:; udp: 4000
    ;; QUESTION SECTION:
    ;midominio.com.           IN  A

    ;; ANSWER SECTION:
    midominio.com.        316 IN  A   X.X.X.19
    midominio.com.        316 IN  A   X.X.X.18

    ;; Query time: 41 msec
    ;; SERVER: 192.168.1.254#53(192.168.1.254)
    ;; WHEN: Tue Jul 08 10:56:55 CDT 2014
    ;; MSG SIZE  rcvd: 72



Este es un ejemplo de un dns de roundrobin, existe 2 registros A para midominio.com
Cuando el browser resuelva el dominio puede resolver la ip 19 o la ip 18.

Ahora lo que sigue es instalar la aplicación en las ips.

Consideraciones
---------------

El registro de ttl del dominio debe ser minimo para que la propagación de cambios en dns sea minima.

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
---------------

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
-------------------

Server-1 seria el centro de la aplicacion y server-2 hasta n serian nodos de server-1

En server-1 hay que tener en cuenta lo siguiente:

si server-1 se cae, hay que tener un server-1.1 listo para que lo remplaze en el menor tiempo posible.

por lo que server-1 no debe recibir peticiones para que no tengan stress y solo se encargue de distribuir la aplicación.


Provisioning
============

Provisioning es la tecnica de crear e instalar las dependiencias del sistema operativo e instalar la aplicación.

Para provisioning utilizamos un script fabric, y para pruebas usamos vagrant.

La idea es tener un script on-shot instale todo los nodos hijos y central.

Y prepare todo para la sincronización


Servidor extra
==============


Es necesario un servidor aparte que genere video, el cual contendra este software:

* celery
* nfs-client


El cual se encargara de generar videos y compartirlos por nfs.


Arquitectura
============

.. image:: _static/arch.png
