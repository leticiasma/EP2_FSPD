compilaProto:
	python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. ./chave_valor_distribuido.proto