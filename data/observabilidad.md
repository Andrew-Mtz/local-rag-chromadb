# Observabilidad

La aplicación registra logs estructurados en formato JSON.

Prometheus recopila métricas del backend y Grafana se utiliza para visualizar dashboards.
Se monitorean latencia, errores HTTP y uso de recursos.

Una alerta de criticidad alta se dispara cuando la tasa de errores HTTP 500 supera el 5 por ciento durante cinco minutos consecutivos.
