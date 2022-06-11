from base.permissions import IsHrm
from ethnicities.models import Ethnicities
from base.views import (
    BaseListCreateAPIView,
    BaseRetrieveUpdateDestroyAPIView
)
from .serializers import (
    EthnicitiesSerializer
)


class ListCreateEthnicitiesAPIView(BaseListCreateAPIView):
    
    model = Ethnicities
    serializer_class = EthnicitiesSerializer
    permission_classes = [IsHrm]
    search_fields = ['name', 'ethnicity']
    filter_fields = {
        'ethnicity': ['exact', 'in'],
    }


class RetrieveUpdateDestroyEthnicitiesAPIView(BaseRetrieveUpdateDestroyAPIView):
    
    model = Ethnicities
    serializer_class = EthnicitiesSerializer
    permission_classes = [IsHrm]
    lookup_url_kwarg = "id"