# Persistencia y base de datos

PostgreSQL es la base de datos principal del sistema.
La aplicación utiliza un pool de conexiones con un máximo de 20 conexiones simultáneas.

Las transacciones de pagos se almacenan en PostgreSQL.
Los datos críticos deben persistirse antes de confirmar una operación como exitosa.

Los backups de la base de datos se realizan una vez por día.
