from typing import Any

from fastapi import APIRouter, Depends, Response
from restconf_service.api.constants import RestconfHeader, RestconfErrorType, RestconfErrorTag
from restconf_service.api.exceptions.exceptions import RestconfHTTPException
from restconf_service.api.exceptions.http_error_data_map import HTTP_ERROR_DATA_MAP
from restconf_service.api.request_helper import get_body_by_content_type, get_accept_header
from restconf_service.api.response_factory import create_response
from restconf_service.exceptions import RestconfException
from restconf_service.restconf_service import RestconfService


class OperationsRouter(APIRouter):
    def __init__(
        self,
        service: RestconfService,
    ):
        super().__init__(prefix='/operations')
        self.add_api_route('/{resource_path:path}', self.process_operation, methods=['POST'])

        self._service = service

    def process_operation(
        self,
        resource_path: str,
        body: Any = Depends(get_body_by_content_type),
        accept: RestconfHeader = Depends(get_accept_header),
    ) -> Response:
        try:
            output = self._service.process_operation(
                operation=resource_path,
                input_kwargs=body,
            )
        except RestconfException as err:
            if err.rpc_info and err.rpc_info.is_output:
                raise RestconfHTTPException(
                    status_code=500,
                    media_type=accept,
                    error_type=RestconfErrorType.RPC,
                    error_tag=RestconfErrorTag.OPERATION_FAILED,
                    error_message=str(err)
                )
            http_error_data = HTTP_ERROR_DATA_MAP[type(err)]
            raise RestconfHTTPException(
                status_code=http_error_data.status_code,
                media_type=accept,
                error_type=http_error_data.error_type,
                error_tag=http_error_data.error_tag,
                error_message=str(err)
            )

        if not output:
            return Response(status_code=204)
        return create_response(
            status_code=200,
            content=output,
            media_type=accept,
        )
