import csv
import numpy
from scipy.stats import pearsonr
from mew.core.exceptions import InvalidInputException
from .filters import TraceFilter
from .serializer import TraceSerializer
from .models import Trace


class ContactService():
    def compute_correlation(self, fileA, fileB):
        list_A = []
        list_B = []
        with open(fileA, 'r') as csvfile:
            csvreader = csv.reader(csvfile)
            for row in csvreader:
                list_A.append(row[0])
        with open(fileB, 'r') as csvfile:
            csvreader = csv.reader(csvfile)
            for row in csvreader:
                list_B.append(float(row[0]))
        if len(list_A) < len(list_B):
            list_B = list_B[: len(list_A)]
        elif len(list_A) > len(list_B):
            list_A = list_A[: len(list_B)]
        A = numpy.array(list_A)
        B = numpy.array(list_B)
        corr, _ = pearsonr(A, B)
        return abs(corr)

    def detect(self, data):
        date = data.get('date')
        lng_lower_limits = data.get('lng_lower_limits', False)
        lng_upper_limits = data.get('lng_upper_limits', False)
        lat_lower_limits = data.get('lat_lower_limits', False)
        lat_upper_limits = data.get('lat_upper_limits', False)
        file_names = data.get('file_names', False)
        obj = TraceFilter({'date': date}, queryset=Trace.objects.filter(is_deleted=False))
        serialized_data = TraceSerializer(instance=obj, many=True).data
        contact_location = []
        num_of_contacts = 0
        for trace_obj in serialized_data:
            trace_lng_l_l = trace_obj['lng_lower_limit']
            trace_lng_u_l = trace_obj['lng_upper_limit']
            trace_lat_l_l = trace_obj['lat_lower_limit']
            trace_lat_u_l = trace_obj['lat_upper_limit']
            for count, lng_lower_limit in enumerate(lng_lower_limits):
                lng_lower = ((lng_lower_limit > trace_lng_l_l or lng_lower_limit < trace_lng_l_l) and lng_lower_limit < trace_lng_u_l)
                lat_lower = ((lat_lower_limits[count] > trace_lat_l_l or lat_lower_limits[count] < trace_lat_l_l) and lat_lower_limits[count] < trace_lat_u_l)
                lng_upper = ((lng_upper_limits[count] > trace_lng_u_l or lng_upper_limits[count] < trace_lng_u_l) and lng_upper_limits[count] > trace_lng_l_l)
                lat_upper = ((lat_upper_limits[count] > trace_lat_u_l or lat_upper_limits[count] < trace_lat_u_l) and lat_upper_limits[count] > trace_lat_l_l)
                if lng_lower and lng_upper and lat_lower and lat_upper:
                    corr = self.compute_correlation(file_names[count], trace_obj['trace_file_url'])
                    if corr >= 0.86:
                        contact_location.append([lng_lower_limit, lat_lower_limits[count],
                                                 lng_upper_limits[count], lat_upper_limits[count]])
                        num_of_contacts += 1
        if num_of_contacts != 0:
            return None, {'status': 'CONTACT', 'num_of_contacts': num_of_contacts, 'contact_locations': contact_location, 'corr': corr}
        else:
            return None, {'status': 'NO_CONTACT', 'num_of_contacts': 0, 'contact_locations': [], 'corr': corr}
