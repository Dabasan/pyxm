"""
Client for Python XOPSManipulator
"""
from py4j.java_gateway import JavaGateway

class PyXMClient(object):
    """
    Client for Python XOPSManipulator
    """
    def __init__(self):
        super().__init__()

        self.gateway=JavaGateway()
        self.entry_point=self.gateway.entry_point

    def shutdown(self):
        self.entry_point.shutdown()
        self.gateway.shutdown()

    def get_gateway(self):
        return self.gateway
    def get_entry_point(self):
        return self.entry_point
