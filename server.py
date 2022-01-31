from concurrent import futures
import grpc
import sys
import threading
import socket

import armazenamento_chave_valor_distribuido_pb2
import armazenamento_chave_valor_distribuido_pb2_grpc
#----------------------------------------------------

class ServidorDeParesChaveValor(armazenamento_chave_valor_distribuido_pb2_grpc.ServidorDeParesChaveValorServicer):
    def __init__(self, eventoDeParada, qtdArgumentos, idServidorNaRede):
        self.paresChaveValor = {}
        self.eventoDeParada = eventoDeParada
        self.qtdArgumentos = qtdArgumentos
        self.idServidorNaRede = idServidorNaRede
    
    def Inserir(self, chave_valor, context):
        if chave_valor.chave in self.paresChaveValor:
            return armazenamento_chave_valor_distribuido_pb2.FlagRetorno(flag=-1)
        else:
            self.paresChaveValor[chave_valor.chave] = chave_valor.valor
            return armazenamento_chave_valor_distribuido_pb2.FlagRetorno(flag=0)

    def Consultar(self, chave, context):
        if chave.chave in self.paresChaveValor:
            return armazenamento_chave_valor_distribuido_pb2.Valor(valor=self.paresChaveValor[chave.chave])
        else:
            return armazenamento_chave_valor_distribuido_pb2.Valor(valor="")

    def Ativar(self, idServico, context):
        if self.qtdArgumentos == 2:
            return armazenamento_chave_valor_distribuido_pb2.FlagRetorno(flag=0)
        else:
            with grpc.insecure_channel(idServico.idServico) as channel:
                stub = armazenamento_chave_valor_distribuido_pb2_grpc.ServidorCombinaServidoresStub(channel)

                parametro = armazenamento_chave_valor_distribuido_pb2.RegistroChaves(endServidorArmazenamento=self.idServidorNaRede)
                for chave in self.paresChaveValor.keys():
                    parametro.chaves.append(chave)

                numChavesProcessadas = stub.Registrar(parametro)

                return armazenamento_chave_valor_distribuido_pb2.FlagRetorno(flag=numChavesProcessadas.numChaves)

    def Terminar(self, paramVazio, context):
        self.eventoDeParada.set()
        return armazenamento_chave_valor_distribuido_pb2.FlagRetorno(flag=0)        

def executaServidor(portaDoServidor, qtdArgumentos):
    eventoDeParada = threading.Event()
    identificacaoServidor = socket.getfqdn()

    idServidorNaRede = identificacaoServidor+":"+portaDoServidor

    executaServidor = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    armazenamento_chave_valor_distribuido_pb2_grpc.add_ServidorDeParesChaveValorServicer_to_server(
        ServidorDeParesChaveValor(eventoDeParada, qtdArgumentos, idServidorNaRede), executaServidor)
    executaServidor.add_insecure_port(f'[::]:{portaDoServidor}')
    executaServidor.start()
    eventoDeParada.wait()
    executaServidor.stop(grace=1)


if __name__ == '__main__':
    #Não sei se tem isso mesmo
    qtdArgumentos = len(sys.argv) #Quantidade de argumentos passados como parâmetro na entrada 

    if qtdArgumentos < 2 or qtdArgumentos > 3:
        exit()

    portaDoServidor = sys.argv[1]

    executaServidor(portaDoServidor, qtdArgumentos)