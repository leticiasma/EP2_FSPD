from concurrent import futures
import grpc
import sys
import threading

import chave_valor_distribuido_pb2
import chave_valor_distribuido_pb2_grpc

class ArmazenamentoChavesServidores(chave_valor_distribuido_pb2_grpc.ArmazenamentoChavesServidoresServicer):
    def __init__(self, stop_event):
        self.servidorChaves = {}
        self._stop_event = stop_event
    
    def Registrar(self, servidor_chaves, context):
        for chave in servidor_chaves.chaves:
            self.servidorChaves[chave] = servidor_chaves.enderecoServidor
        return chave_valor_distribuido_pb2.NumChavesProcessadas(numChaves=len(servidor_chaves.chaves))

    def Mapear(self, chave, context):
        if chave.chave in self.servidorChaves:
            return chave_valor_distribuido_pb2.StringIDServico(idServico=self.servidorChaves[chave.chave])
        else:
            return chave_valor_distribuido_pb2.StringIDServico(idServico="")

    def Terminar(self, paramVazio, context):
        self._stop_event.set()
        return chave_valor_distribuido_pb2.FlagRetorno(flag=0)        

def server(serverPort):
    stop_event = threading.Event()

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    chave_valor_distribuido_pb2_grpc.add_ArmazenamentoChavesServidoresServicer_to_server(
        ArmazenamentoChavesServidores(stop_event), server)
    server.add_insecure_port(f'[::]:{serverPort}')
    server.start()
    stop_event.wait()
    server.stop(grace=1)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        exit()

    serverPort = sys.argv[1]

    server(serverPort)