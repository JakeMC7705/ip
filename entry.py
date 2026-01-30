from js import Response, Headers

async def on_fetch(request, env):
    try:
        # 1. Get Data
        client_ip = request.headers.get("CF-Connecting-IP") or "Unknown"
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

        # 2. Create the HTML String (No json.dumps!)
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
                p {{ color: #555; margin: 5px 0; }}
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

        # 3. FIX: Create explicit Headers object
        # This ensures the browser 100% understands this is HTML
        my_headers = Headers.new({"content-type": "text/html; charset=utf-8"})

        return Response.new(html_content, {"headers": my_headers})

    except Exception as e:
        return Response.new(f"Error: {str(e)}", {"status": 500})