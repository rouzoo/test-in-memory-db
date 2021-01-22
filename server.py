import time
from concurrent import futures
 
import grpc
 
import scheme_pb2
import scheme_pb2_grpc

database = dict()
 
class InMemoryDBServicer(scheme_pb2_grpc.InMemoryDBServicer):
    def Chain(self, request, context):
        response = scheme_pb2.ChainResponse()

        for req in request.requests:
            chain_resp = scheme_pb2.ChainResponse.SingleChainResponse()
            single_resp = getattr(self, req.handler)(req.request, context)
            if req.handler == 'Get':
                chain_resp.getResponse.CopyFrom(single_resp)
            elif req.handler == 'GetAll':
                chain_resp.getAllResponse.CopyFrom(single_resp)
            else:
                chain_resp.headers.CopyFrom(single_resp)

            response.responses.append(chain_resp)
        
        return response

    def Set(self, request, context):
        response = scheme_pb2.Headers()
        response.status = "ok"

        key, value = request.key, request.value
        database[key] = value
        
        return response
    
    def GetAll(self, request, context):
        response = scheme_pb2.GetAllResponse()
        response.headers.status = 'ok'
        
        for k, v in database.items():
            if v is not None or v != '':
                response.payloads.append(k)
        
        return response

    def Get(self, request, context):
        response = scheme_pb2.GetResponse()
        response.headers.status = 'ok'

        key = request.key
        if not key in database.keys():
            response.headers.status = 'no such key in database'
            return response
        
        response.payload = database.get(key)
        return response

    def Delete(self, request, context):
        response = scheme_pb2.Headers()
        response.status = "ok"

        key = request.key
        del database[key]
        
        return response
 
 
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=4))
 
    scheme_pb2_grpc.add_InMemoryDBServicer_to_server(InMemoryDBServicer(), server)
 
    print('Starting server on port 6066.')
    server.add_insecure_port('[::]:6066')
    server.start()
 
    try:
        while True:
            time.sleep(3600)
    except KeyboardInterrupt:
        server.stop(0)
 
 
if __name__ == '__main__':
    serve()