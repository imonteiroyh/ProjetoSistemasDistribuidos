# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: message.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\rmessage.proto\"9\n\x08\x44iscover\x12\x13\n\x0b\x64\x65vice_type\x18\x01 \x01(\t\x12\n\n\x02ip\x18\x02 \x01(\t\x12\x0c\n\x04port\x18\x03 \x01(\x05\"\"\n\x04\x44\x61ta\x12\x0c\n\x04type\x18\x01 \x01(\t\x12\x0c\n\x04\x64\x61ta\x18\x02 \x01(\t\"X\n\x07Message\x12\x0c\n\x04type\x18\x01 \x01(\t\x12\x1d\n\x08\x64iscover\x18\x02 \x01(\x0b\x32\t.DiscoverH\x00\x12\x15\n\x04\x64\x61ta\x18\x03 \x01(\x0b\x32\x05.DataH\x00\x42\t\n\x07\x63ontent')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'message_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _DISCOVER._serialized_start=17
  _DISCOVER._serialized_end=74
  _DATA._serialized_start=76
  _DATA._serialized_end=110
  _MESSAGE._serialized_start=112
  _MESSAGE._serialized_end=200
# @@protoc_insertion_point(module_scope)