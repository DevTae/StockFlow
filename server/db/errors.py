# ERR Documentation and Summary

from rest_framework.response import Response
from rest_framework import status

def message(code, header, message):
    return { "err_code" : code, "message" : str(header) + message }

def RES_ERR_MSG_HEAD_MUST_EXISTS(header) -> Response:
    return Response(message(1, header, " header must needs to exists."), status=status.HTTP_400_BAD_REQUEST)

def RES_ERR_MSG_HEAD_NOT_SUPPORTED(header) -> Response:
    return Response(message(2, header, " header is not supported."), status=status.HTTP_400_BAD_REQUEST)

def RES_ERR_MSG_VAL_FORMAT_MISMATCH(header) -> Response:
    return Response(message(3, header, " value has not supported format."), status=status.HTTP_400_BAD_REQUEST)

def RES_ERR_MSG_VAL_NOT_VALID(header) -> Response:
    return Response(message(4, header, " value is not valid."), status=status.HTTP_401_UNAUTHORIZED)

def RES_ERR_MSG_VAL_NOT_FOUND(header) -> Response:
    return Response(message(5, header, " value is not found."), status=status.HTTP_204_NO_CONTENT)
