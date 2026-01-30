from js import Response

async def on_fetch(request, env):
    try:
        # --- 1. Safe Data Extraction ---
        # We handle the case where headers might be missing
        headers = request.headers
        client_ip = "Unknown"
        if headers:
            client_ip = headers.get("CF-Connecting-IP") or "Unknown"

        # Safely access Cloudflare data using a multi-step approach
        # This prevents crashing if 'request' doesn't have a 'cf' attribute
        cf_data = getattr(request, "cf", None)
        
        # Default values
        isp = "Unknown ISP"
        asn = "Unknown"
        country = "Unknown"
        city = "Unknown"

        # Only try to read fields if cf_data actually exists
        if cf_data:
            # We force everything to a string immediately to avoid JS Proxy errors
            isp = str(getattr(cf_data, "asOrganization", "") or "Unknown ISP")
            asn = str(getattr(cf_data, "asn", "") or "Unknown")
            country = str(getattr(cf_data, "country", "") or "Unknown")
            city = str(getattr(cf_data, "city", "") or "Unknown Location")

        # --- 2. HTML Construction ---
        html_content = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>My IP Details</title>
            <style>
                body {{ font-family: sans-serif; background: #f4f6f8; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }}
                .card {{ background: white; padding: 2rem; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); text-align: center; width: 300px; }}
                h1 {{ color: #2563eb; margin: 0 0 10px 0; font-size: 1.5rem; }}
                .label {{ font-size: 0.8rem; text-transform: uppercase; color: #888; margin-top: 15px; }}
                .val {{ font-weight: bold; color: #333; }}
            </style>
        </head>
        <body>
            <div class="card">
                <div class="label">Your IP</div>
                <h1>{client_ip}</h1>
                <div class="label">ISP</div>
                <div class="val">{isp}</div>
                <div class="label">Location</div>
                <div class="val">{city}, {country}</div>
                <div class="label">ASN</div>
                <div class="val">{asn}</div>
            </div>
        </body>
        </html>
        """

        # --- 3. Return Response (The Fix) ---
        # We pass a simple dictionary for options. 
        # The key must be "headers", and the value must be another dictionary.
        return Response.new(
            html_content, 
            {
                "headers": {
                    "content-type": "text/html; charset=utf-8"
                }
            }
        )

    except Exception as e:
        # --- 4. Debugging Block ---
        # If this crashes, it will now print the EXACT error to your screen
        # instead of a generic "Worker Exception"
        import traceback
        error_trace = traceback.format_exc()
        return Response.new(
            f"<h1>Worker Error</h1><pre>{error_trace}</pre>", 
            {
                "headers": {"content-type": "text/html"}
            }
        )