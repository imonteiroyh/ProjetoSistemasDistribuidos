# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: proto/lamp.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x10proto/lamp.proto\"\x15\n\x13GetLampStateRequest\">\n\x16\x43hangeLampColorRequest\x12\x16\n\thex_color\x18\x01 \x01(\tH\x00\x88\x01\x01\x42\x0c\n\n_hex_color\"6\n\x16\x43hangeLampStateRequest\x12\x12\n\x05state\x18\x01 \x01(\x08H\x00\x88\x01\x01\x42\x08\n\x06_state\"P\n\x0cLampResponse\x12\x13\n\x06status\x18\x01 \x01(\x08H\x00\x88\x01\x01\x12\x14\n\x07message\x18\x02 \x01(\tH\x01\x88\x01\x01\x42\t\n\x07_statusB\n\n\x08_message2\xae\x01\n\x04Lamp\x12\x38\n\x0c\x63hange_state\x12\x17.ChangeLampStateRequest\x1a\r.LampResponse\"\x00\x12\x32\n\tget_state\x12\x14.GetLampStateRequest\x1a\r.LampResponse\"\x00\x12\x38\n\x0c\x63hange_color\x12\x17.ChangeLampColorRequest\x1a\r.LampResponse\"\x00\x62\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'proto.lamp_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _GETLAMPSTATEREQUEST._serialized_start=20
  _GETLAMPSTATEREQUEST._serialized_end=41
  _CHANGELAMPCOLORREQUEST._serialized_start=43
  _CHANGELAMPCOLORREQUEST._serialized_end=105
  _CHANGELAMPSTATEREQUEST._serialized_start=107
  _CHANGELAMPSTATEREQUEST._serialized_end=161
  _LAMPRESPONSE._serialized_start=163
  _LAMPRESPONSE._serialized_end=243
  _LAMP._serialized_start=246
  _LAMP._serialized_end=420
# @@protoc_insertion_point(module_scope)
