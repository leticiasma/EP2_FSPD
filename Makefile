compilaProto:
	@python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. ./armazenamento_chave_valor_distribuido.proto
run_serv_pares_1: compilaProto
	@python ./server.py $(arg)
run_serv_pares_2: compilaProto
	@python ./server.py $(arg) 0
run_cli_pares: compilaProto
	@python ./client.py $(arg)
run_serv_central: compilaProto
	@python ./server_central.py $(arg)
run_cli_central: compilaProto
	@python ./client.py $(arg) 0
clean: 
	rm *_pb2.py *_pb2_grpc.py