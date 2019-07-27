from exporters.backends.prometheus import PrometheusExporterBackend


def get_exporter_backend(uri, type="prometheus", logger=None):
    """
    A factory method pattern to decide which storage implementation to use

    @param: type - string (s3, filesystem)

    @return: Storage Class Implementation

    """
    if type == "prometheus":
        return PrometheusExporterBackend(uri, logger)
    raise NotImplementedError(
        f"No storage backend implementation for type {type}")
