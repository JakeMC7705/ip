from js import Response

async def on_fetch(request, env):
    try:
        # --- 1. Data Extraction ---
        client_ip = request.headers.get("CF-Connecting-IP") or "Unknown"
        
        # Safely access Cloudflare data
        cf_data = getattr(request, "cf", None)
        
        # Defaults
        isp = "Unknown ISP"
        asn = "Unknown"
        country = "Unknown"
        city = "Unknown"

        if cf_data:
            # We use str() to safely convert JS objects to Python strings
            isp = str(getattr(cf_data, "asOrganization", "") or "Unknown ISP")
            asn = str(getattr(cf_data, "asn", "") or "Unknown")
            country = str(getattr(cf_data, "country", "") or "Unknown")
            city = str(getattr(cf_data, "city", "") or "Unknown Location")

        # --- 2. HTML Construction ---
        # We use a Python f-string to insert variables directly into the HTML.
        # Note: In f-strings, CSS braces { } need to be doubled {{ }} to escape them.
        html_content = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>My IP Details</title>
            <style>
                body {{
                    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
                    background-color: #f4f6f8;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                    margin: 0;
                }}
                .card {{
                    background: white;
                    padding: 40px;
                    border-radius: 16px;
                    box-shadow: 0 10px 25px rgba(0,0,0,0.05);
                    text-align: center;
                    max-width: 400px;
                    width: 90%;
                }}
                .label {{
                    text-transform: uppercase;
                    font-size: 0.75rem;
                    letter-spacing: 1px;
                    color: #888;
                    margin-top: 20px;
                    margin-bottom: 5px;
                }}
                .value {{
                    font-size: 1.1rem;
                    color: #333;
                    font-weight: 500;
                }}
                .main-ip {{
                    font-size: 2.5rem;
                    font-weight: 700;
                    color: #2563eb;
                    margin-bottom: 30px;
                    word-break: break-word;
                }}
                .divider {{
                    height: 1px;
                    background: #eee;
                    margin: 20px 0;
                }}
            </style>
        </head>
        <body>
            <div class="card">
                <div class="label">Your Public IP Address</div>
                <div class="main-ip">{client_ip}</div>
                
                <div class="divider"></div>

                <div class="label">Internet Service Provider</div>
                <div class="value">{isp}</div>

                <div class="label">Location</div>
                <div class="value">{city}, {country}</div>

                <div class="label">ASN</div>
                <div class="value">{asn}</div>
            </div>
        </body>
        </html>
        """

        # --- 3. Return Response ---
        # We allow 'text/html' so the browser renders the page
        return Response.new(
            html_content, 
            {
                "headers": {"Content-Type": "text/html; charset=utf-8"}
            }
        )

    except Exception as e:
        # Fallback error message
        return Response.new(f"Error: {str(e)}", {"status": 500})