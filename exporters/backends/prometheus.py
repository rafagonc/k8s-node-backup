from prometheus_client import CollectorRegistry, Gauge, push_to_gateway


class PrometheusExporterBackend():
    def __init__(self, uri, logger):
        self.logger = logger
        self.uri = uri
        self.registry = CollectorRegistry()

    def export(self,
               metric_name,
               metric_value,
               metric_description="",
               labels={}):
        if self.uri:
            gauge = Gauge(
                metric_name,
                metric_description,
                registry=self.registry,
                labelnames=("hostname", ))
            gauge.labels(**labels).set(metric_value)
            push_to_gateway(
                self.uri, job='node-backups', registry=self.registry)
