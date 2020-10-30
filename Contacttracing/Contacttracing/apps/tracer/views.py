from rest_framework.views import APIView
from mew.core.utils import APIResponse
from .services import TraceService


class TraceView(APIView):
    def get(self, request):
        error, res = TraceService.get_trace(request)
        return APIResponse.send(data=res, error=error)

    def post(self, request):
        data = {
            'user_id': request.data.get('user_id', False),
            'lng_lower_limit': request.data.get('lng_lower_limit', False),
            'lng_upper_limit': request.data.get('lng_upper_limit', False),
            'lat_lower_limit': request.data.get('lat_lower_limit', False),
            'lat_upper_limit': request.data.get('lat_upper_limit', False),
            'trace_file_url': request.data.get('trace_file_url', False),
            'date': request.data.get('date', False),
            'files': request.FILES.get('magnetic_trace', False)
        }
        error, res = TraceService.create_trace(data=data)
        return APIResponse(data=res, error=error)

    def delete(self, request):
        error, res = TraceService.delete_trace(request.GET)
        return APIResponse.send(data=res, error=error)


class S3PresignedURL(APIView):

    def get(self, request):
        """
        """
        params = {
            "user_id": request.GET.get("user_id"),
            "file_extension": request.GET.get("file_extersion"),
            "file_name": request.GET.get("file_name"),
        }
        resp = APIService().generate_presigned_url(params)
        if not resp['status']:
            return APIResponse.send(data={}, error=resp['message'])
        return APIResponse.send(data=resp['data'], error="")
