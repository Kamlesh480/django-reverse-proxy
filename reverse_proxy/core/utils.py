from .models import EndpointServer

def get_next_server(endpoint):
    servers = list(endpoint.servers.filter(is_active=True).order_by('endpointserver__position'))
    if not servers:
        return None

    # Rotate: Move first to last
    first = servers.pop(0)
    servers.append(first)

    # Update position values
    for idx, srv in enumerate(servers):
        es = EndpointServer.objects.get(endpoint=endpoint, server=srv)
        es.position = idx
        es.save()

    return first
