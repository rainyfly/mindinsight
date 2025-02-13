# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: mindinsight_profiling_parallel.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from . import mindinsight_anf_ir_pb2 as mindinsight__anf__ir__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='mindinsight_profiling_parallel.proto',
  package='mindinsight',
  syntax='proto2',
  serialized_options=b'\370\001\001',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n$mindinsight_profiling_parallel.proto\x12\x0bmindinsight\x1a\x18mindinsight_anf_ir.proto\"q\n\x11ProfilingParallel\x12\x0f\n\x07version\x18\x01 \x01(\t\x12#\n\x06\x63onfig\x18\x02 \x01(\x0b\x32\x13.mindinsight.Config\x12&\n\x05graph\x18\x03 \x01(\x0b\x32\x17.mindinsight.GraphProto\"x\n\x06\x43onfig\x12\x0f\n\x07rank_id\x18\x01 \x01(\r\x12\x10\n\x08stage_id\x18\x02 \x01(\r\x12\x15\n\rparallel_type\x18\x03 \x01(\t\x12\x34\n\rstage_devices\x18\x04 \x03(\x0b\x32\x1d.mindinsight.TensorShapeProtoB\x03\xf8\x01\x01'
  ,
  dependencies=[mindinsight__anf__ir__pb2.DESCRIPTOR,])




_PROFILINGPARALLEL = _descriptor.Descriptor(
  name='ProfilingParallel',
  full_name='mindinsight.ProfilingParallel',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='version', full_name='mindinsight.ProfilingParallel.version', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='config', full_name='mindinsight.ProfilingParallel.config', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='graph', full_name='mindinsight.ProfilingParallel.graph', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=79,
  serialized_end=192,
)


_CONFIG = _descriptor.Descriptor(
  name='Config',
  full_name='mindinsight.Config',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='rank_id', full_name='mindinsight.Config.rank_id', index=0,
      number=1, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='stage_id', full_name='mindinsight.Config.stage_id', index=1,
      number=2, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='parallel_type', full_name='mindinsight.Config.parallel_type', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='stage_devices', full_name='mindinsight.Config.stage_devices', index=3,
      number=4, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=194,
  serialized_end=314,
)

_PROFILINGPARALLEL.fields_by_name['config'].message_type = _CONFIG
_PROFILINGPARALLEL.fields_by_name['graph'].message_type = mindinsight__anf__ir__pb2._GRAPHPROTO
_CONFIG.fields_by_name['stage_devices'].message_type = mindinsight__anf__ir__pb2._TENSORSHAPEPROTO
DESCRIPTOR.message_types_by_name['ProfilingParallel'] = _PROFILINGPARALLEL
DESCRIPTOR.message_types_by_name['Config'] = _CONFIG
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

ProfilingParallel = _reflection.GeneratedProtocolMessageType('ProfilingParallel', (_message.Message,), {
  'DESCRIPTOR' : _PROFILINGPARALLEL,
  '__module__' : 'mindinsight_profiling_parallel_pb2'
  # @@protoc_insertion_point(class_scope:mindinsight.ProfilingParallel)
  })
_sym_db.RegisterMessage(ProfilingParallel)

Config = _reflection.GeneratedProtocolMessageType('Config', (_message.Message,), {
  'DESCRIPTOR' : _CONFIG,
  '__module__' : 'mindinsight_profiling_parallel_pb2'
  # @@protoc_insertion_point(class_scope:mindinsight.Config)
  })
_sym_db.RegisterMessage(Config)


DESCRIPTOR._options = None
# @@protoc_insertion_point(module_scope)
