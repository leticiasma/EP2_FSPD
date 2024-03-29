# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

import armazenamento_chave_valor_distribuido_pb2 as armazenamento__chave__valor__distribuido__pb2


class ServidorDeParesChaveValorStub(object):
  """---------------------------------------------------------
  COMANDOS E MENSAGENS TROCADAS ENTRE CLIENTES E SERVIDORES
  ---------------------------------------------------------

  Comandos da "Primeira parte: um servidor de pares (chave,valor)"
  """

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.Inserir = channel.unary_unary(
        '/ServidorDeParesChaveValor/Inserir',
        request_serializer=armazenamento__chave__valor__distribuido__pb2.Chave_Valor.SerializeToString,
        response_deserializer=armazenamento__chave__valor__distribuido__pb2.FlagRetorno.FromString,
        )
    self.Consultar = channel.unary_unary(
        '/ServidorDeParesChaveValor/Consultar',
        request_serializer=armazenamento__chave__valor__distribuido__pb2.Chave.SerializeToString,
        response_deserializer=armazenamento__chave__valor__distribuido__pb2.Valor.FromString,
        )
    self.Ativar = channel.unary_unary(
        '/ServidorDeParesChaveValor/Ativar',
        request_serializer=armazenamento__chave__valor__distribuido__pb2.StringIDServico.SerializeToString,
        response_deserializer=armazenamento__chave__valor__distribuido__pb2.FlagRetorno.FromString,
        )
    self.Terminar = channel.unary_unary(
        '/ServidorDeParesChaveValor/Terminar',
        request_serializer=armazenamento__chave__valor__distribuido__pb2.ParamVazio.SerializeToString,
        response_deserializer=armazenamento__chave__valor__distribuido__pb2.FlagRetorno.FromString,
        )


class ServidorDeParesChaveValorServicer(object):
  """---------------------------------------------------------
  COMANDOS E MENSAGENS TROCADAS ENTRE CLIENTES E SERVIDORES
  ---------------------------------------------------------

  Comandos da "Primeira parte: um servidor de pares (chave,valor)"
  """

  def Inserir(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def Consultar(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def Ativar(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def Terminar(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_ServidorDeParesChaveValorServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'Inserir': grpc.unary_unary_rpc_method_handler(
          servicer.Inserir,
          request_deserializer=armazenamento__chave__valor__distribuido__pb2.Chave_Valor.FromString,
          response_serializer=armazenamento__chave__valor__distribuido__pb2.FlagRetorno.SerializeToString,
      ),
      'Consultar': grpc.unary_unary_rpc_method_handler(
          servicer.Consultar,
          request_deserializer=armazenamento__chave__valor__distribuido__pb2.Chave.FromString,
          response_serializer=armazenamento__chave__valor__distribuido__pb2.Valor.SerializeToString,
      ),
      'Ativar': grpc.unary_unary_rpc_method_handler(
          servicer.Ativar,
          request_deserializer=armazenamento__chave__valor__distribuido__pb2.StringIDServico.FromString,
          response_serializer=armazenamento__chave__valor__distribuido__pb2.FlagRetorno.SerializeToString,
      ),
      'Terminar': grpc.unary_unary_rpc_method_handler(
          servicer.Terminar,
          request_deserializer=armazenamento__chave__valor__distribuido__pb2.ParamVazio.FromString,
          response_serializer=armazenamento__chave__valor__distribuido__pb2.FlagRetorno.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'ServidorDeParesChaveValor', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))


class ServidorCombinaServidoresStub(object):
  """Segunda "Segunda parte: um servidor que combina servidores"
  """

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.Registrar = channel.unary_unary(
        '/ServidorCombinaServidores/Registrar',
        request_serializer=armazenamento__chave__valor__distribuido__pb2.RegistroChaves.SerializeToString,
        response_deserializer=armazenamento__chave__valor__distribuido__pb2.NumChavesProcessadas.FromString,
        )
    self.Mapear = channel.unary_unary(
        '/ServidorCombinaServidores/Mapear',
        request_serializer=armazenamento__chave__valor__distribuido__pb2.Chave.SerializeToString,
        response_deserializer=armazenamento__chave__valor__distribuido__pb2.StringIDServico.FromString,
        )
    self.Terminar = channel.unary_unary(
        '/ServidorCombinaServidores/Terminar',
        request_serializer=armazenamento__chave__valor__distribuido__pb2.ParamVazio.SerializeToString,
        response_deserializer=armazenamento__chave__valor__distribuido__pb2.NumChavesProcessadas.FromString,
        )


class ServidorCombinaServidoresServicer(object):
  """Segunda "Segunda parte: um servidor que combina servidores"
  """

  def Registrar(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def Mapear(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def Terminar(self, request, context):
    """Neste caso, o NumChavesProcessadas é o total
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_ServidorCombinaServidoresServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'Registrar': grpc.unary_unary_rpc_method_handler(
          servicer.Registrar,
          request_deserializer=armazenamento__chave__valor__distribuido__pb2.RegistroChaves.FromString,
          response_serializer=armazenamento__chave__valor__distribuido__pb2.NumChavesProcessadas.SerializeToString,
      ),
      'Mapear': grpc.unary_unary_rpc_method_handler(
          servicer.Mapear,
          request_deserializer=armazenamento__chave__valor__distribuido__pb2.Chave.FromString,
          response_serializer=armazenamento__chave__valor__distribuido__pb2.StringIDServico.SerializeToString,
      ),
      'Terminar': grpc.unary_unary_rpc_method_handler(
          servicer.Terminar,
          request_deserializer=armazenamento__chave__valor__distribuido__pb2.ParamVazio.FromString,
          response_serializer=armazenamento__chave__valor__distribuido__pb2.NumChavesProcessadas.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'ServidorCombinaServidores', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))
