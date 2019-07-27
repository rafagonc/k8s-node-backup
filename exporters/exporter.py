class Exporter():
    def __init__(self, uri, logger):
        raise NotImplementedError()

    def export(self,
               metric_name,
               metric_value,
               metric_description="",
               labels=[]):
        raise NotImplementedError()
