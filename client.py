import grpc
import sys

import armazenamento_chave_valor_distribuido_pb2
import armazenamento_chave_valor_distribuido_pb2_grpc
#----------------------------------------------------

def executaCliente(servidorConexao, qtdArgumentos):

    with grpc.insecure_channel(servidorConexao) as channel:

        #Verifica se o programa deve funcionar como o descrito na primeira parte da especificação (caso qtdArgumentos == 2),
        # com o método de ativação "vazio" ou como na segunda parte
        if qtdArgumentos == 2:
            stub = armazenamento_chave_valor_distribuido_pb2_grpc.ServidorDeParesChaveValorStub(channel)
        else:
            stub = armazenamento_chave_valor_distribuido_pb2_grpc.ServidorCombinaServidoresStub(channel)

        while(True):

            entrada = input()
            splitEntrada = entrada.split(',')
            comando = splitEntrada[0]

            if qtdArgumentos == 2:

                if comando == 'I':
                    resultado = stub.Inserir(armazenamento_chave_valor_distribuido_pb2.Chave_Valor(chave=int(splitEntrada[1]), valor=splitEntrada[2]))
                    print(resultado.flag)
                elif comando == 'C':
                    resultado = stub.Consultar(armazenamento_chave_valor_distribuido_pb2.Chave(chave=int(splitEntrada[1])))
                    print(resultado.valor)
                elif comando == 'A':
                    resultado = stub.Ativar(armazenamento_chave_valor_distribuido_pb2.StringIDServico(idServico=splitEntrada[1]))
                    print(resultado.flag)
                elif comando == 'T':
                    resultado = stub.Terminar(armazenamento_chave_valor_distribuido_pb2.ParamVazio())
                    print(resultado.flag)
                    if(resultado.flag==0):
                        break
            
            else:

                if comando == 'C':
                    resultado = stub.Mapear(armazenamento_chave_valor_distribuido_pb2.Chave(chave=int(splitEntrada[1])))

                    if resultado.idServico != "":

                        with grpc.insecure_channel(resultado.idServico) as channel:

                            stub2 = armazenamento_chave_valor_distribuido_pb2_grpc.ServidorDeParesChaveValorStub(channel)

                            resultado2 = stub2.Consultar(armazenamento_chave_valor_distribuido_pb2.Chave(chave=int(splitEntrada[1])))
                            print(resultado.idServico+":"+resultado2.valor)

                elif comando == 'T':
                    resultado = stub.Terminar(armazenamento_chave_valor_distribuido_pb2.ParamVazio())
                    print(resultado.numChaves)
                    break    

if __name__ == '__main__':
    qtdArgumentos = len(sys.argv) #Quantidade de argumentos passados como parâmetro na entrada

    if qtdArgumentos < 2 or qtdArgumentos > 3:
        exit()

    servidorConexao = sys.argv[1] #Servidor ao qual o cliente irá se conectar
    executaCliente(servidorConexao, qtdArgumentos)