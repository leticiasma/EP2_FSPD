import grpc
import sys

import chave_valor_distribuido_pb2
import chave_valor_distribuido_pb2_grpc

def runClient(serverAdd):
    with grpc.insecure_channel(serverAdd) as channel:
        stub = chave_valor_distribuido_pb2_grpc.ArmazenamentoChaveValorDistribuidoStub(channel)
        #while(True):
        arquivo = open('myfile.txt', 'r')
        linhas = arquivo.readlines()

        for linha in linhas:

        #command = input()
            command = linha
            inputSplit = command.split(',')

            if inputSplit[0] == 'I':
                response = stub.Inserir(chave_valor_distribuido_pb2.Chave_Valor(chave=int(inputSplit[1]), valor=inputSplit[2]))
                print(response.flag)
            elif inputSplit[0] == 'C':
                response = stub.Consultar(chave_valor_distribuido_pb2.Chave(chave=int(inputSplit[1])))
                print(response.valor)
            elif inputSplit[0] == 'A':
                response = stub.Ativar(chave_valor_distribuido_pb2.StringIDServico(idServico=inputSplit[1]))
                print(response.flag)
            elif inputSplit[0] == 'T':
                response = stub.Terminar(chave_valor_distribuido_pb2.ParamVazio())
                print(response.flag)
                if(response.flag==0):
                    break

        arquivo.close()
            
        

if __name__ == '__main__':
    if len(sys.argv) != 2:
        exit()

    serverAdd = sys.argv[1]
    runClient(serverAdd)