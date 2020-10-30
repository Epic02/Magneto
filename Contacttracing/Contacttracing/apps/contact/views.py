import random
from rest_framework.views import APIView
from mew.core.utils import APIResponse
from .services import ContactService


class ContactCheckerView(APIView):
    def post(self, request):
        files = request.FILES
        lng_upper_limits = request.data.get('lng_upper_limits', None)
        data = {
            'date': request.data.get('date', None),
            'lng_upper_limits': lng_upper_limits,
            'lng_lower_limits': request.data.get('lng_lower_limits', None),
            'lat_upper_limits': request.data.get('lat_upper_limits', None),
            'lat_lower_limits': request.data.get('lat_lower_limits', None),
        }
        file_names = []
        for count, lng in enumerate(lng_upper_limits):
            uploaded_file = files.get('trace_'+str(count))
            file_name = 'trace_' + str(random.randint(0, 1000)) + '.csv'
            file_names.append(file_name)
            with open(file_name, 'wb+') as destination:
                for chunk in uploaded_file.chunks():
                    destination.write(chunk)
            print(type(files.get('magnetic_trace')))
        data['file_names'] = file_names
        error, res = ContactService().detect(data=data)
        return APIResponse.send(data=res, error=error)
