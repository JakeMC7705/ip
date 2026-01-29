from js import Response, JSON

async def on_fetch(request, env):
    """
    Returns the visitor's IP, ISP, and ASN as a JSON response.
    """
    # 1. Get the IP Address
    client_ip = request.headers.get("CF-Connecting-IP") or "Unknown"

    # 2. Get ISP/Network Data from the 'cf' object
    # The 'cf' object contains geolocation and network data.
    # We use .get() or default values in case the data is missing.
    cf_data = request.cf
    
    isp = "Unknown"
    asn = 0
    country = "Unknown"

    if cf_data:
        # 'asOrganization' usually holds the ISP name (e.g., "Comcast Cable")
        isp = getattr(cf_data, "asOrganization", "Unknown")
        asn = getattr(cf_data, "asn", 0)
        country = getattr(cf_data, "country", "Unknown")

    # 3. Build the response dictionary
    data = {
        "ip": client_ip,
        "isp": isp,
        "asn": asn,
        "country": country
    }

    # 4. Return as JSON
    # We use JSON.stringify from the JS API for easiest compatibility, 
    # or the standard Python json library.
    import json
    return Response.new(
        json.dumps(data), 
        headers={"Content-Type": "application/json"}
    )