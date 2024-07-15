import usaddress
from django.views.generic import TemplateView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.exceptions import ParseError


class Home(TemplateView):
    template_name = 'parserator_web/index.html'


class AddressParse(APIView):
    renderer_classes = [JSONRenderer]

    def get(self, request):
        address = request.query_params.get('address')
        if not address:
            return Response({'error': 'Address parameter is required'}, status=400)
        
        try:
            address_components, address_type = self.parse(address)
        except usaddress.RepeatedLabelError as e:
            return Response({'error': str(e)}, status=400)

        return Response({
            'input_string': address,
            'address_components': address_components,
            'address_type': address_type
        })

    def parse(self, address):
        address_components, address_type = usaddress.tag(address)
        return address_components, address_type