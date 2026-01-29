from js import Response

async def on_fetch(request, env):
    """
    Handles the incoming request and returns the visitor's IP address.
    """
    # Cloudflare automatically adds the 'CF-Connecting-IP' header
    # to incoming requests.
    client_ip = request.headers.get("CF-Connecting-IP")

    # Handle edge cases where the header might be missing (unlikely in CF)
    if not client_ip:
        client_ip = "IP not found"

    # Return the IP as a simple text response
    return Response.new(client_ip)