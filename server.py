from concurrent import futures
import grpc
import sys
import threading
import socket

import chave_valor_distribuido_pb2
import chave_valor_distribuido_pb2_grpc

class ArmazenamentoChaveValorDistribuido(chave_valor_distribuido_pb2_grpc.ArmazenamentoChaveValorDistribuidoServicer):
    def __init__(self, stop_event, qtdArgumentos, idServidorNaRede):
        self.paresChaveValor = {}
        self._stop_event = stop_event
        self.qtdArgumentos = qtdArgumentos
        self.idServidorNaRede = idServidorNaRede
    
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
        if self.qtdArgumentos == 2:
            return chave_valor_distribuido_pb2.FlagRetorno(flag=0)
        else:
            with grpc.insecure_channel(idServico.idServico) as channel:
                stub = chave_valor_distribuido_pb2_grpc.ArmazenamentoChavesServidoresStub(channel)

                parametro = chave_valor_distribuido_pb2.RegistroChaves(enderecoServidor=self.idServidorNaRede)
                for chave in self.paresChaveValor.keys():
                    parametro.chaves.append(chave)

                numChavesProcessadas = stub.Registrar(parametro)

                return chave_valor_distribuido_pb2.FlagRetorno(flag=numChavesProcessadas.numChaves)

    def Terminar(self, paramVazio, context):
        self._stop_event.set()
        return chave_valor_distribuido_pb2.FlagRetorno(flag=0)        

def server(serverPort, qtdArgumentos):
    stop_event = threading.Event()

    serverHostName = socket.getfqdn()

    idServidorNaRede = serverHostName+":"+serverPort

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    chave_valor_distribuido_pb2_grpc.add_ArmazenamentoChaveValorDistribuidoServicer_to_server(
        ArmazenamentoChaveValorDistribuido(stop_event, qtdArgumentos, idServidorNaRede), server)
    server.add_insecure_port(f'[::]:{serverPort}')
    server.start()
    stop_event.wait()
    server.stop(grace=1)


if __name__ == '__main__':
    qtdArgumentos = len(sys.argv)

    if qtdArgumentos < 2 or qtdArgumentos > 3:
        exit()

    serverPort = sys.argv[1]

    server(serverPort, qtdArgumentos)