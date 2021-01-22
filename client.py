import grpc

import scheme_pb2
import scheme_pb2_grpc
 

channel = grpc.insecure_channel('localhost:6066')
stub = scheme_pb2_grpc.InMemoryDBStub(channel)

def read_cmd(c=''):
    while True:
        cmd = input(f'{c}Command: ')
        if cmd != '':
            return cmd

def read_key_value(cmd):
    key = ''
    value = ''

    if cmd == 'Set':
        key = input('Key: ')
        value = input('Value: ')
    elif cmd == 'Get' or cmd == 'Delete':
        key = input('Key: ')            
    elif cmd.startswith('__w'):
        value = input('Value: ')

    return key, value

def chain_request():
    reqs = []
    idx = 0
    while True:
        idx += 1

        cmd = read_cmd(f'\nCommand #{idx}\n')
        
        key, value = read_key_value(cmd)
        
        if cmd == 'ChainEnd' or cmd == 'Chain':
            return scheme_pb2.ChainRequest(requests=reqs)
        
        if cmd.startswith('__'):
            idx -= 1

        if cmd == '__history':
            print('Buffer of reqs')
            print('***********************')
            print([print(f'Request #{i + 1}\n{r}\n') for i, r in enumerate(reqs)])
            print('***********************')
            continue
        if cmd == '__wremove':
            key = int(value) + 1
            print(f'Record with \n***********************\nidx:{key}, \nval: {reqs[key]}***********************\nwill be deleted, y/n?')
            if input() == 'y':
                del reqs[key]
            continue
        
        reqs.append(scheme_pb2.ChainRequest.SingleChainRequest(handler=cmd, 
                                                               request=scheme_pb2.Request(key=key, value=value))
        )


print('This is client for our GRPC server')
print('Usage:')
print('You can type commands and values to messaging with server')
print('Available commands are:')
print('    ChainStart/ChainEnd - Starting chain command, this command allows us to send multiple commands in single request')
print('    Get                 - Get value from Server')
print('    GetAll              - Get all keys with values from Server')
print('    Set                 - Set value on Server')
print('    Delete              - Delete key from Server')
print('    Chain[Unsupported]  - Server Chain call, for Chain call use ChainStart')

while True:
    cmd = read_cmd()
    
    request = None
    if cmd == 'ChainStart' or cmd == 'Chain':
        request = chain_request()
        cmd = 'Chain'
    else:
        key, value = read_key_value(cmd)
        request = scheme_pb2.Request(key=key, value=value)

    response = getattr(stub, cmd)(request)

    print('Resp: ')
    print(response) 