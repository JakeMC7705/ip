from js import Response, Headers

async def on_fetch(request, env):
    try:
        # --- 1. Data Extraction ---
        headers = request.headers
        client_ip = headers.get("CF-Connecting-IP") if headers else "Unknown"

        cf_data = getattr(request, "cf", None)
        
        isp = "Unknown ISP"
        asn = "Unknown"
        country = "Unknown"
        city = "Unknown"

        if cf_data:
            isp = str(getattr(cf_data, "asOrganization", "") or "Unknown ISP")
            asn = str(getattr(cf_data, "asn", "") or "Unknown")
            country = str(getattr(cf_data, "country", "") or "Unknown")
            city = str(getattr(cf_data, "city", "") or "Unknown Location")

        # --- 2. HTML Construction ---
        # Added <meta http-equiv> as a safety net to force rendering
        html_content = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>My IP Details</title>
            <style>
                body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: #f4f6f8; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }}
                .card {{ background: white; padding: 2.5rem; border-radius: 16px; box-shadow: 0 10px 25px rgba(0,0,0,0.05); text-align: center; width: 320px; }}
                h1 {{ color: #2563eb; margin: 0 0 10px 0; font-size: 1.8rem; letter-spacing: -0.5px; }}
                .label {{ font-size: 0.75rem; text-transform: uppercase; letter-spacing: 1px; color: #9ca3af; margin-top: 20px; font-weight: 600; }}
                .val {{ font-size: 1.1rem; color: #1f2937; font-weight: 500; margin-top: 4px; }}
                .divider {{ height: 1px; background: #f3f4f6; margin: 20px 0; }}
            </style>
        </head>
        <body>
            <div class="card">
                <div class="label">Your IP Address</div>
                <h1>{client_ip}</h1>
                
                <div class="divider"></div>
                
                <div class="label">ISP / Organization</div>
                <div class="val">{isp}</div>
                
                <div class="label">Location</div>
                <div class="val">{city}, {country}</div>
                
                <div class="label">Network (ASN)</div>
                <div class="val">{asn}</div>
            </div>
        </body>
        </html>
        """

        # --- 3. Create Proper JS Headers ---
        # We explicitly create a JS Headers object. This is the most reliable way.
        my_headers = Headers.new({"Content-Type": "text/html; charset=utf-8"})

        # --- 4. Return Response ---
        # We pass the headers in the options dictionary.
        return Response.new(html_content, headers=my_headers)

    except Exception as e:
        # Debugging: Print error to screen if something goes wrong
        return Response.new(f"<h1>Worker Error</h1><p>{str(e)}</p>", headers=Headers.new({"Content-Type": "text/html"}))