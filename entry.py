from js import Response
import json

async def on_fetch(request, env):
    try:
        # 1. Get the IP (Default to "Unknown" if missing)
        client_ip = request.headers.get("CF-Connecting-IP") or "Unknown"

        # 2. Safely access the 'cf' object
        # We use getattr to avoid crashing if 'cf' is missing (e.g. local dev)
        cf_data = getattr(request, "cf", None)
        
        # Set defaults
        isp = "Unknown"
        asn = 0
        country = "Unknown"

        # 3. Extract data
        if cf_data:
            # We cast to str() to ensure we have Python strings, not JS Proxies
            isp = str(getattr(cf_data, "asOrganization", "Unknown") or "Unknown")
            asn = int(getattr(cf_data, "asn", 0) or 0)
            country = str(getattr(cf_data, "country", "Unknown") or "Unknown")

        data = {
            "ip": client_ip,
            "isp": isp,
            "asn": asn,
            "country": country
        }

        # 4. FIX: Pass headers inside a dictionary as the 2nd positional argument
        return Response.new(
            json.dumps(data), 
            {
                "headers": {"Content-Type": "application/json"}
            }
        )

    except Exception as e:
        return Response.new(str(e), {"status": 500})