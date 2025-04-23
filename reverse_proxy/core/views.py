from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Server, Endpoint, EndpointServer
from .utils import get_next_server
from django.db.models import Max

@api_view(['POST'])
def proxy_request(request, endpoint_name):
    try:
        endpoint = Endpoint.objects.get(name=endpoint_name)
        server = get_next_server(endpoint)

        if not server:
            return Response({'error': 'No active servers available'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

        # Log request
        server.request_log += f"Request: {request.path} | Method: {request.method}\n"
        server.save()

        return Response({
            'message': 'Request forwarded',
            'forwarded_to': server.ip_address,
            'request_data': request.data
        }, status=status.HTTP_200_OK)

    except Endpoint.DoesNotExist:
        return Response({'error': 'Endpoint not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def update_server_status(request):
    ip = request.data.get('ip')
    status_value = request.data.get('status')

    try:
        server = Server.objects.get(ip_address=ip)
        server.is_active = True if status_value == 'up' else False
        server.save()
        return Response({'message': f'Server {ip} status updated to {status_value}'}, status=status.HTTP_200_OK)
    except Server.DoesNotExist:
        return Response({'error': 'Server not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def server_logs(request):
    logs = {}
    for server in Server.objects.all():
        logs[server.ip_address] = server.request_log.splitlines()
    return Response(logs)


@api_view(['POST'])
def add_server(request):
    ip = request.data.get('ip')
    if not ip:
        return Response({'error': 'IP address is required'}, status=status.HTTP_400_BAD_REQUEST)

    server, created = Server.objects.get_or_create(ip_address=ip)
    if not created:
        return Response({'message': f'Server {ip} already exists'}, status=status.HTTP_200_OK)

    return Response({'message': f'Server {ip} added successfully'}, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def assign_server_to_endpoint(request):
    ip = request.data.get('ip')
    endpoint_name = request.data.get('endpoint')

    try:
        server = Server.objects.get(ip_address=ip)
        endpoint, _ = Endpoint.objects.get_or_create(name=endpoint_name)

        # Find current max position
        current_max = EndpointServer.objects.filter(endpoint=endpoint).aggregate(Max('position'))['position__max']
        position = (current_max + 1) if current_max is not None else 0

        EndpointServer.objects.create(endpoint=endpoint, server=server, position=position)
        return Response({'message': f'Server {ip} assigned to endpoint {endpoint_name} at position {position}'})
    except Server.DoesNotExist:
        return Response({'error': 'Server not found'}, status=404)
