# Arquitectura del sistema

El backend principal está desarrollado en Python utilizando FastAPI.
Los servicios se ejecutan dentro de contenedores Docker.

La aplicación expone una API REST para operaciones de usuarios, pagos y reportes.
El servicio de pagos se comunica con el resto de los componentes mediante HTTP.

La infraestructura está organizada en servicios independientes para facilitar el escalado y el mantenimiento.
