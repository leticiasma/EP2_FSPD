from concurrent import futures
import grpc
import sys
import threading

import armazenamento_chave_valor_distribuido_pb2
import armazenamento_chave_valor_distribuido_pb2_grpc
#----------------------------------------------------

class ServidorCombinaServidores(armazenamento_chave_valor_distribuido_pb2_grpc.ServidorCombinaServidoresServicer):
    def __init__(self, eventoDeParada):
        self.paresChaveServidor = {}
        self.eventoDeParada = eventoDeParada
        self.servidoresDeArmazenamento = [] #Guardará no máximo 10 servidores que armazenam pares chave-valor
    
    #O parâmetro servidor_chaves contém o identificador do servidor e as chaves que ele têm armazenadas naquele momento
    def Registrar(self, servidor_chaves, context):
        if servidor_chaves.endServidorArmazenamento in self.servidoresDeArmazenamento or len(self.servidoresDeArmazenamento) < 10:
            if servidor_chaves.endServidorArmazenamento not in self.servidoresDeArmazenamento:
                self.servidoresDeArmazenamento.append(servidor_chaves.endServidorArmazenamento)

            for chave in servidor_chaves.chaves:
                self.paresChaveServidor[chave] = servidor_chaves.endServidorArmazenamento
            return armazenamento_chave_valor_distribuido_pb2.NumChavesProcessadas(numChaves=len(servidor_chaves.chaves))

    def Mapear(self, chave, context):
        if chave.chave in self.paresChaveServidor:
            return armazenamento_chave_valor_distribuido_pb2.StringIDServico(idServico=self.paresChaveServidor[chave.chave])
        else:
            #Caso o um servidor com aquela chave não tenha sido encontrado
            return armazenamento_chave_valor_distribuido_pb2.StringIDServico(idServico="")

    def Terminar(self, paramVazio, context):
        self.eventoDeParada.set()
        return armazenamento_chave_valor_distribuido_pb2.FlagRetorno(flag=0)        

def executaServidor(portaDoServidor):
    eventoDeParada = threading.Event()

    executaServidor = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    armazenamento_chave_valor_distribuido_pb2_grpc.add_ServidorCombinaServidoresServicer_to_server(ServidorCombinaServidores(eventoDeParada), executaServidor)
    executaServidor.add_insecure_port(f'[::]:{portaDoServidor}')
    executaServidor.start()
    eventoDeParada.wait()
    executaServidor.stop(grace=1)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        exit()

    portaDoServidor = sys.argv[1]

    executaServidor(portaDoServidor)