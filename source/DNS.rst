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
===============

El registro de ttl del dominio debe ser minimo para que la propagación de cambios en dns sea minima.
