from js import Response
import json

async def on_fetch(request, env):
    try:
        # 1. Get the IP
        client_ip = request.headers.get("CF-Connecting-IP") or "Unknown"

        # 2. Safely access the 'cf' object
        # usage of getattr prevents crashing if 'cf' doesn't exist (common in local testing)
        cf_data = getattr(request, "cf", None)
        
        # Set defaults
        isp = "Unknown"
        asn = 0
        country = "Unknown"

        # 3. Extract data with Type Casting
        # We wrap values in str() or int() to convert them from JS Proxies to Python types.
        # This prevents the "Object of type Proxy is not JSON serializable" error.
        if cf_data:
            # We use 'or' to handle cases where the field exists but is empty/null
            isp = str(getattr(cf_data, "asOrganization", "Unknown") or "Unknown")
            asn = int(getattr(cf_data, "asn", 0) or 0)
            country = str(getattr(cf_data, "country", "Unknown") or "Unknown")

        # 4. Build Dictionary
        data = {
            "ip": client_ip,
            "isp": isp,
            "asn": asn,
            "country": country
        }

        return Response.new(
            json.dumps(data), 
            headers={"Content-Type": "application/json"}
        )

    except Exception as e:
        # 5. Error Handling
        # If it crashes, this will return the actual error message to your browser
        error_response = {
            "error": "The worker encountered an exception",
            "details": str(e)
        }
        return Response.new(
            json.dumps(error_response),
            headers={"Content-Type": "application/json"}
        )