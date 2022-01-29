from concurrent import futures
import grpc
import sys
import threading

import chave_valor_distribuido_pb2
import chave_valor_distribuido_pb2_grpc

class ArmazenamentoChaveValorDistribuido(chave_valor_distribuido_pb2_grpc.ArmazenamentoChaveValorDistribuidoServicer):
    def __init__(self, stop_event):
        self.paresChaveValor = {}
        self._stop_event = stop_event
    
    def Inserir(self, chave_valor, context):
        if chave_valor.chave in self.paresChaveValor:
            return chave_valor_distribuido_pb2.FlagRetorno(flag=-1)
        else:
            self.paresChaveValor[chave_valor.chave] = chave_valor.valor
            return chave_valor_distribuido_pb2.FlagRetorno(flag=0)

    def Consultar(self, chave, context):
        if chave.chave in self.paresChaveValor:
            return chave_valor_distribuido_pb2.Valor(valor=self.paresChaveValor[chave.chave])
        else:
            return chave_valor_distribuido_pb2.Valor(valor="")

    def Ativar(self, idServico, context):
        return chave_valor_distribuido_pb2.FlagRetorno(flag=0)

    def Terminar(self, paramVazio, context):
        self._stop_event.set()
        return chave_valor_distribuido_pb2.FlagRetorno(flag=0)        

def server(serverPort):
    stop_event = threading.Event()

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    chave_valor_distribuido_pb2_grpc.add_ArmazenamentoChaveValorDistribuidoServicer_to_server(
        ArmazenamentoChaveValorDistribuido(stop_event), server)
    server.add_insecure_port(f'[::]:{serverPort}')
    server.start()
    stop_event.wait()
    server.stop(grace=1)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        exit()

    serverPort = sys.argv[1]

    server(serverPort)