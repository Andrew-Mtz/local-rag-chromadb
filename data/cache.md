# Sistema de caché

Redis se utiliza como sistema de caché para reducir consultas repetitivas a PostgreSQL.

Las claves almacenadas en Redis tienen un TTL de 300 segundos.
Cuando una clave expira, la aplicación vuelve a consultar la base de datos y actualiza la caché.

Redis no se utiliza como fuente principal de persistencia.
Si Redis no está disponible, la aplicación puede continuar consultando PostgreSQL directamente.
