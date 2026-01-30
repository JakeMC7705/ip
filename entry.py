from js import Response

async def on_fetch(request, env):
    # 1. Gather Data (with defaults to prevent crashes)
    client_ip = "Unknown"
    # Safely try to get the header
    try:
        if request.headers:
            client_ip = request.headers.get("CF-Connecting-IP") or "Unknown"
    except:
        pass

    # Safely try to get the CF object
    cf_data = getattr(request, "cf", None)
    
    isp = "Unknown ISP"
    asn = "Unknown"
    country = "Unknown"
    city = "Unknown"

    # Only access properties if cf_data exists
    if cf_data:
        # Force string conversion immediately
        isp = str(getattr(cf_data, "asOrganization", "") or "Unknown ISP")
        asn = str(getattr(cf_data, "asn", "") or "Unknown")
        country = str(getattr(cf_data, "country", "") or "Unknown")
        city = str(getattr(cf_data, "city", "") or "Unknown Location")

    # 2. Build HTML
    # We include the <meta> tag as a backup to force the browser to render HTML
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>My IP Details</title>
        <style>
            body {{ font-family: -apple-system, system-ui, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: #f4f6f8; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }}
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

    # 3. Create the Response Object (Plain)
    # We do NOT pass headers here to avoid the constructor crashing
    response = Response.new(html_content)

    # 4. Set the Header Manually (The Safe Way)
    # This modifies the response object directly using the JS API
    response.headers.set("Content-Type", "text/html; charset=utf-8")

    return response