import boto3
import logging
import requests
from Contacttracing.apps.users.models import User
from mew.core.exceptions import InvalidInputException
from botocore.config import Config
from .filters import TraceFilter
from .serializer import TraceSerializer
from .models import Trace, Count


class TraceService():
    def get_trace(self, request):
        result = TraceFilter(request.GET, queryset=Trace.objects.filter(is_deleted=False))
        serialized_data = TraceSerializer(instance=result.qs, many=True).data
        return None, serialized_data

    def create_trace(self, data):
        user_id = data.get('user_id', False)
        date = data.get('date', False)
        lng_upper_limit = data.get('lng_upper_limit', False)
        lng_lower_limit = data.get('lng_lower_limit', False)
        lat_upper_limit = data.get('lat_upper_limit', False)
        lat_lower_limit = data.get('lat_lower_limit', False)
        trace_file_url = data.get('trace_file_url', False)
        files = data.get('file')
        if not user_id or not lng_lower_limit or not lng_upper_limit or not lat_lower_limit or not lat_upper_limit or not date:
            raise InvalidInputException('Missing Data')
        file_name = 'infected_trace' + str(user_id) + '.csv'
        with open(file_name, 'wb+') as destination:
            for chunk in files.chunks():
                destination.write(chunk)
        try:
            user_obj = User.objects.get(user_id=user_id)
            obj = Trace.objects.create(user_id=user_id, lng_lower_limit=lng_lower_limit, lng_upper_limit=lng_upper_limit,
                                       lat_lower_limit=lat_lower_limit, lat_upper_limit=lat_upper_limit, trace_file_url=file_name)
            obj.save()
            serialized_data = TraceSerializer(instance=obj).data
        except User.DoesNotExist:
            raise InvalidInputException('User does not exist')
        return None, serialized_data

    def delete_trace(self, data):
        try:
            user_id = data.get('user_id', False)
            if not user_id:
                raise InvalidInputException('Missing user id')
            obj = Trace.objects.get(user_id=user_id)
            obj.delete()
            return None, 'Deleted Successfully'
        except Trace.DoesNotExist:
            raise InvalidInputException('Trace does not exist')
        except:
            raise InvalidInputException('Delete Failed')


"""class TraceUpload():
    def upload_file(self, data):
        files = data.get('file')
        obj, created = Count.objects.get_or_create(count_gte=0)
        file_name = 'infected_trace' + str(obj.count) + '.csv'
        with open(file_name, 'wb+') as destination:
            for chunk in files.chunks():
                destination.write(chunk)"""


"""class APIService():

    def generate_presigned_url(self, params):     
        if not params.get("user_id") or not params.get("file_name"):
            raise InvalidInputException('Missing Patient ID and/or File Name')

        try:
            conf = Config(
                region_name=settings.CONFIG['S3']['BUCKET_REGION'],
            )

            file_name = params.get("user_id") + "/" + params.get("file_name")

            s3_client = boto3.client('s3', aws_access_key_id=settings.CONFIG['S3']['ACCESS_KEY'],
                                     aws_secret_access_key=settings.CONFIG['S3']['SECRET_KEY'], config=conf)
            response = s3_client.generate_presigned_url('put_object',
                                                        Params={'Bucket': settings.CONFIG['S3']['BUCKET_NAME'],
                                                                'Key': file_name},
                                                        ExpiresIn=3600)

            obj = Trace.objects.get(user_id=params.get('user_id'))
            obj.trace_file_url = response
            return {'status': True, 'data': {"pre_signed_url": response}}
        except Trace.DoesNotExist:
            raise InvalidInputException('Trace of user does not exist')
        except Exception as e:
            logging.error(e)
            raise InvalidInputException("Unable to generate a pre-signed URL.")"""
