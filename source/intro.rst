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
