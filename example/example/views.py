from django.core.urlresolvers import reverse
from rest_framework import viewsets, status
from rest_framework.decorators import list_route
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework_csv.parsers import CSVParser
from rest_framework_csv.renderers import CSVRenderer
from example.serializers import TalkSerializer
from example.models import Talk


class TalkViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows talks to be viewed or edited.
    """
    queryset = Talk.objects.all()
    parser_classes = (CSVParser,) + tuple(api_settings.DEFAULT_PARSER_CLASSES)
    renderer_classes = (CSVRenderer,) + tuple(api_settings.DEFAULT_RENDERER_CLASSES)
    serializer_class = TalkSerializer

    def get_renderer_context(self):
        context = super(TalkViewSet, self).get_renderer_context()
        context['header'] = (
            self.request.GET['fields'].split(',')
            if 'fields' in self.request.GET else None)
        return context

    @list_route(methods=['POST'])
    def bulk_upload(self, request, *args, **kwargs):
        """
        Try out this view with the following curl command:

        curl -X POST http://localhost:8000/talks/bulk_upload/ \
            -d "speaker,topic,scheduled_at
                Ana Balica,Testing,2016-11-03T15:15:00+01:00
                Aymeric Augustin,Debugging,2016-11-03T16:15:00+01:00" \
            -H "Content-type: text/csv" \
            -H "Accept: text/csv"
        """
        serializer = self.get_serializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_303_SEE_OTHER, headers={'Location': reverse('talk-list')})
