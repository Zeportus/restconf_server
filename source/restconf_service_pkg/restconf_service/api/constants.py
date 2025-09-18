from enum import Enum


class RestconfHeader(Enum):
    YANG_DATA_JSON  = 'application/yang-data+json'


class RestconfErrorType(Enum):
    TRANSPORT = 'transport'
    RPC = 'rpc'
    PROTOCOL = 'protocol'
    APPLICATION = 'application'


class RestconfErrorTag(Enum):
    INVALID_VALUE = 'invalid-value'
    UNKNOWN_ELEMENT = 'unknown-element'
    OPERATION_NOT_SUPPORTED = 'operation-not-supported'
    OPERATION_FAILED = 'operation-failed'
    BAD_ELEMENT = 'bad-element'
    MALFORMED_MESSAGE = 'malformed-message'
