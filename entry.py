from js import Response

async def on_fetch(request, env):
    # 1. Gather Data (with defaults to prevent crashes)
    client_ip = "Unknown"
    try:
        if request.headers:
            client_ip = request.headers.get("CF-Connecting-IP") or "Unknown"
    except:
        pass

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

    # 2. Build Branded HTML
    # - Added the logo image at the top of the card.
    # - Changed the color scheme to a dark theme matching the logo's background.
    # - Used the blue-to-purple gradient for the main IP address and brand title.
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Let's Tech - My IP Details</title>
        <style>
            :root {{
                --brand-bg: #1a1a1a; /* Dark background from logo */
                --brand-card-bg: #242424;
                --brand-text-primary: #ffffff;
                --brand-text-secondary: #a3a3a3;
                --brand-accent-blue: #2563eb;
                --brand-accent-purple: #a855f7;
            }}
            body {{
                font-family: -apple-system, system-ui, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
                background: var(--brand-bg);
                color: var(--brand-text-primary);
                display: flex;
                justify-content: center;
                align-items: center;
                min-height: 100vh;
                margin: 0;
                padding: 20px;
                box-sizing: border-box;
            }}
            .card {{
                background: var(--brand-card-bg);
                padding: 2.5rem;
                border-radius: 24px;
                box-shadow: 0 20px 40px rgba(0,0,0,0.4);
                text-align: center;
                width: 100%;
                max-width: 380px;
                border: 1px solid #333;
            }}
            .logo-container {{
                margin-bottom: 1.5rem;
            }}
            .logo-img {{
                width: 80px;
                height: auto;
                margin-bottom: 1rem;
            }}
            .brand-title {{
                font-size: 1.5rem;
                font-weight: 700;
                margin: 0;
                background: linear-gradient(to right, var(--brand-accent-blue), var(--brand-accent-purple));
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
            }}
            .brand-tagline {{
                font-size: 0.9rem;
                color: var(--brand-text-secondary);
                margin-top: 0.5rem;
                margin-bottom: 2rem;
            }}
            .ip-address {{
                font-size: 2rem;
                font-weight: 800;
                margin: 0 0 1rem 0;
                letter-spacing: -0.5px;
                background: linear-gradient(to right, var(--brand-accent-blue), var(--brand-accent-purple));
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                word-break: break-word;
            }}
            .label {{
                font-size: 0.75rem;
                text-transform: uppercase;
                letter-spacing: 1.2px;
                color: var(--brand-text-secondary);
                margin-top: 1.5rem;
                font-weight: 600;
            }}
            .val {{
                font-size: 1.1rem;
                color: var(--brand-text-primary);
                font-weight: 500;
                margin-top: 0.4rem;
            }}
            .divider {{
                height: 1px;
                background: #333;
                margin: 1.5rem 0;
            }}
        </style>
    </head>
    <body>
        <div class="card">
            <div class="logo-container">
                <img src="image_0.png" alt="Let's Tech Logo" class="logo-img">
                <h1 class="brand-title">Let's Tech</h1>
                <p class="brand-tagline">Diving Into Technology Together</p>
            </div>
            
            <div class="divider"></div>

            <div class="label">Your IP Address</div>
            <div class="ip-address">{client_ip}</div>
            
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

    # 3. Create Response & Set Header Manually
    response = Response.new(html_content)
    response.headers.set("Content-Type", "text/html; charset=utf-8")

    return response