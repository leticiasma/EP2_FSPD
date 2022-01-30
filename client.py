import grpc
import sys

import chave_valor_distribuido_pb2
import chave_valor_distribuido_pb2_grpc

def runClient(serverAdd, qtdArgumentos):
    with grpc.insecure_channel(serverAdd) as channel:
        if qtdArgumentos == 2:
            stub = chave_valor_distribuido_pb2_grpc.ArmazenamentoChaveValorDistribuidoStub(channel)
        else:
            stub = chave_valor_distribuido_pb2_grpc.ArmazenamentoChavesServidoresStub(channel)

        while(True):
            command = input()
            inputSplit = command.split(',')

            if qtdArgumentos == 2:

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
            
            else:

                if inputSplit[0] == 'C':
                    response = stub.Mapear(chave_valor_distribuido_pb2.Chave(chave=int(inputSplit[1])))

                    if response.idServico != "":

                        with grpc.insecure_channel(response.idServico) as channel:

                            stub2 = chave_valor_distribuido_pb2_grpc.ArmazenamentoChaveValorDistribuidoStub(channel)

                            response2 = stub2.Consultar(chave_valor_distribuido_pb2.Chave(chave=int(inputSplit[1])))
                            print(response.idServico+":"+response2.valor)

                elif inputSplit[0] == 'T':
                    response = stub.Terminar(chave_valor_distribuido_pb2.ParamVazio())
                    print(response.numChaves)
                    break

            
        

if __name__ == '__main__':
    qtdArgumentos = len(sys.argv)

    if qtdArgumentos < 2 or qtdArgumentos > 3:
        exit()

    serverAdd = sys.argv[1]
    runClient(serverAdd, qtdArgumentos)