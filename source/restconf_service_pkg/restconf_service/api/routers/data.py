import logging
from typing import Any

from fastapi import APIRouter, Depends, Response
from restconf_service.api.constants import RestconfHeader
from restconf_service.api.exceptions.exceptions import RestconfHTTPException
from restconf_service.api.exceptions.http_error_data_map import HTTP_ERROR_DATA_MAP
from restconf_service.api.request_helper import get_accept_header, get_body_by_content_type
from restconf_service.api.response_factory import create_response
from restconf_service.exceptions import RestconfException
from restconf_service.restconf_service import RestconfService

logger = logging.getLogger()


class DataRouter(APIRouter):
    def __init__(
        self,
        service: RestconfService,
    ):
        super().__init__(prefix='/data')
        self.add_api_route('/{resource_path:path}', self.get_resource, methods=['GET'])
        self.add_api_route('/{resource_path:path}', self.patch_resource, methods=['PATCH'])

        self._service = service

    def get_resource(
        self,
        resource_path: str = '',
        accept: RestconfHeader = Depends(get_accept_header),
    ) -> Response:
        try:
            resource = self._service.get_resource(resource_path)
            return create_response(
                status_code=200,
                content=resource,
                media_type=accept,
            )

        except RestconfException as err:
            http_error_data = HTTP_ERROR_DATA_MAP[type(err)]
            raise RestconfHTTPException(
                status_code=http_error_data.status_code,
                media_type=accept,
                error_type=http_error_data.error_type,
                error_tag=http_error_data.error_tag,
                error_message=str(err)
            )

    def patch_resource(
        self,
        body: Any = Depends(get_body_by_content_type),
        resource_path: str = '',
        accept: RestconfHeader = Depends(get_accept_header),
    ) -> Response:
        try:
            self._service.update_resource(resource_path, body)
            return Response(status_code=204)

        except RestconfException as err:
            http_error_data = HTTP_ERROR_DATA_MAP[type(err)]
            raise RestconfHTTPException(
                status_code=http_error_data.status_code,
                media_type=accept,
                error_type=http_error_data.error_type,
                error_tag=http_error_data.error_tag,
                error_message=str(err)
            )
