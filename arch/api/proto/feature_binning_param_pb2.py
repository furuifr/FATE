# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: feature-binning-param.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='feature-binning-param.proto',
  package='com.webank.ai.fate.common.mlmodel.buffer',
  syntax='proto3',
  serialized_pb=_b('\n\x1b\x66\x65\x61ture-binning-param.proto\x12(com.webank.ai.fate.common.mlmodel.buffer\"\xee\x01\n\x07IVParam\x12\x11\n\twoe_array\x18\x01 \x03(\x01\x12\x10\n\x08iv_array\x18\x02 \x03(\x01\x12\x19\n\x11\x65vent_count_array\x18\x03 \x03(\x03\x12\x1d\n\x15non_event_count_array\x18\x04 \x03(\x03\x12\x18\n\x10\x65vent_rate_array\x18\x05 \x03(\x01\x12\x1c\n\x14non_event_rate_array\x18\x06 \x03(\x01\x12\x14\n\x0csplit_points\x18\x07 \x03(\x01\x12\n\n\x02iv\x18\x08 \x01(\x01\x12\x18\n\x10is_woe_monotonic\x18\t \x01(\x08\x12\x10\n\x08\x62in_nums\x18\n \x01(\x03\"\xd9\x01\n\x13\x46\x65\x61tureBinningParam\x12^\n\tiv_result\x18\x01 \x03(\x0b\x32K.com.webank.ai.fate.common.mlmodel.buffer.FeatureBinningParam.IvResultEntry\x1a\x62\n\rIvResultEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12@\n\x05value\x18\x02 \x01(\x0b\x32\x31.com.webank.ai.fate.common.mlmodel.buffer.IVParam:\x02\x38\x01\x42\x1a\x42\x18\x46\x65\x61tureBinningParamProtob\x06proto3')
)




_IVPARAM = _descriptor.Descriptor(
  name='IVParam',
  full_name='com.webank.ai.fate.common.mlmodel.buffer.IVParam',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='woe_array', full_name='com.webank.ai.fate.common.mlmodel.buffer.IVParam.woe_array', index=0,
      number=1, type=1, cpp_type=5, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='iv_array', full_name='com.webank.ai.fate.common.mlmodel.buffer.IVParam.iv_array', index=1,
      number=2, type=1, cpp_type=5, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='event_count_array', full_name='com.webank.ai.fate.common.mlmodel.buffer.IVParam.event_count_array', index=2,
      number=3, type=3, cpp_type=2, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='non_event_count_array', full_name='com.webank.ai.fate.common.mlmodel.buffer.IVParam.non_event_count_array', index=3,
      number=4, type=3, cpp_type=2, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='event_rate_array', full_name='com.webank.ai.fate.common.mlmodel.buffer.IVParam.event_rate_array', index=4,
      number=5, type=1, cpp_type=5, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='non_event_rate_array', full_name='com.webank.ai.fate.common.mlmodel.buffer.IVParam.non_event_rate_array', index=5,
      number=6, type=1, cpp_type=5, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='split_points', full_name='com.webank.ai.fate.common.mlmodel.buffer.IVParam.split_points', index=6,
      number=7, type=1, cpp_type=5, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='iv', full_name='com.webank.ai.fate.common.mlmodel.buffer.IVParam.iv', index=7,
      number=8, type=1, cpp_type=5, label=1,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='is_woe_monotonic', full_name='com.webank.ai.fate.common.mlmodel.buffer.IVParam.is_woe_monotonic', index=8,
      number=9, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='bin_nums', full_name='com.webank.ai.fate.common.mlmodel.buffer.IVParam.bin_nums', index=9,
      number=10, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=74,
  serialized_end=312,
)


_FEATUREBINNINGPARAM_IVRESULTENTRY = _descriptor.Descriptor(
  name='IvResultEntry',
  full_name='com.webank.ai.fate.common.mlmodel.buffer.FeatureBinningParam.IvResultEntry',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='key', full_name='com.webank.ai.fate.common.mlmodel.buffer.FeatureBinningParam.IvResultEntry.key', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='value', full_name='com.webank.ai.fate.common.mlmodel.buffer.FeatureBinningParam.IvResultEntry.value', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=_descriptor._ParseOptions(descriptor_pb2.MessageOptions(), _b('8\001')),
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=434,
  serialized_end=532,
)

_FEATUREBINNINGPARAM = _descriptor.Descriptor(
  name='FeatureBinningParam',
  full_name='com.webank.ai.fate.common.mlmodel.buffer.FeatureBinningParam',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='iv_result', full_name='com.webank.ai.fate.common.mlmodel.buffer.FeatureBinningParam.iv_result', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[_FEATUREBINNINGPARAM_IVRESULTENTRY, ],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=315,
  serialized_end=532,
)

_FEATUREBINNINGPARAM_IVRESULTENTRY.fields_by_name['value'].message_type = _IVPARAM
_FEATUREBINNINGPARAM_IVRESULTENTRY.containing_type = _FEATUREBINNINGPARAM
_FEATUREBINNINGPARAM.fields_by_name['iv_result'].message_type = _FEATUREBINNINGPARAM_IVRESULTENTRY
DESCRIPTOR.message_types_by_name['IVParam'] = _IVPARAM
DESCRIPTOR.message_types_by_name['FeatureBinningParam'] = _FEATUREBINNINGPARAM
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

IVParam = _reflection.GeneratedProtocolMessageType('IVParam', (_message.Message,), dict(
  DESCRIPTOR = _IVPARAM,
  __module__ = 'feature_binning_param_pb2'
  # @@protoc_insertion_point(class_scope:com.webank.ai.fate.common.mlmodel.buffer.IVParam)
  ))
_sym_db.RegisterMessage(IVParam)

FeatureBinningParam = _reflection.GeneratedProtocolMessageType('FeatureBinningParam', (_message.Message,), dict(

  IvResultEntry = _reflection.GeneratedProtocolMessageType('IvResultEntry', (_message.Message,), dict(
    DESCRIPTOR = _FEATUREBINNINGPARAM_IVRESULTENTRY,
    __module__ = 'feature_binning_param_pb2'
    # @@protoc_insertion_point(class_scope:com.webank.ai.fate.common.mlmodel.buffer.FeatureBinningParam.IvResultEntry)
    ))
  ,
  DESCRIPTOR = _FEATUREBINNINGPARAM,
  __module__ = 'feature_binning_param_pb2'
  # @@protoc_insertion_point(class_scope:com.webank.ai.fate.common.mlmodel.buffer.FeatureBinningParam)
  ))
_sym_db.RegisterMessage(FeatureBinningParam)
_sym_db.RegisterMessage(FeatureBinningParam.IvResultEntry)


DESCRIPTOR.has_options = True
DESCRIPTOR._options = _descriptor._ParseOptions(descriptor_pb2.FileOptions(), _b('B\030FeatureBinningParamProto'))
_FEATUREBINNINGPARAM_IVRESULTENTRY.has_options = True
_FEATUREBINNINGPARAM_IVRESULTENTRY._options = _descriptor._ParseOptions(descriptor_pb2.MessageOptions(), _b('8\001'))
# @@protoc_insertion_point(module_scope)
