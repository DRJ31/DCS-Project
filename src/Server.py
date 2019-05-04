from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler


# Restrict to a particular path.
class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)


# Create server
with SimpleXMLRPCServer(('localhost', 8000), requestHandler=RequestHandler) as server:
    server.register_introspection_functions()


    class AllFuncs():

        def __init__(self):
            self.buffer = ""
            self.identities = []

        def assign_name(self, name):
            self.identities.append(name)
            return len(self.identities) - 1, name

        def get_identities(self):
            return self.identities

        def get_msg(self):
            return self.buffer

        def send_msg(self, msg):
            self.buffer = msg
            return True

    server.register_instance(AllFuncs())

    # Run the server's main loop
    server.serve_forever()
