import datetime
import base64
import os
from .data_manager import LOGO_PATH

# Enhanced certificate with logo
def create_certificate(name, score, date):
    # Check if we have a company logo
    if os.path.exists(LOGO_PATH):
        # Encode logo to base64 for embedding in HTML
        with open(LOGO_PATH, "rb") as img_file:
            logo_base64 = base64.b64encode(img_file.read()).decode()
        logo_embed = f"data:image/png;base64,{logo_base64}"
    else:
        # Use placeholder if no logo
        logo_embed = "https://via.placeholder.com/100x100?text=LOGO"
    
    # Creating a more professional certificate with logo
    html = f"""
    <html>
    <head>
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;700&display=swap');
            body {{
                font-family: 'Montserrat', sans-serif;
                text-align: center;
                padding: 0;
                margin: 0;
                color: #333;
            }}
            .certificate {{
                border: 20px solid #1E88E5;
                border-radius: 10px;
                padding: 40px;
                margin: 20px auto;
                width: 800px;
                position: relative;
                background: #fff url('{logo_embed}') no-repeat 30px 30px;
                background-size: 100px;
            }}
            .certificate:after {{
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background-image: url('{logo_embed}');
                background-repeat: no-repeat;
                background-position: center;
                background-size: 50%;
                opacity: 0.05;
                pointer-events: none;
            }}
            .certificate-header {{
                font-size: 48px;
                margin: 20px 0;
                color: #1E88E5;
                border-bottom: 2px solid #1E88E5;
                padding-bottom: 10px;
            }}
            .certificate-title {{
                font-size: 36px;
                margin: 20px 0;
                color: #333;
            }}
            .certificate-recipient {{
                font-size: 30px;
                margin: 30px 0;
                color: #333;
                border-bottom: 1px solid #eee;
                padding-bottom: 10px;
                font-weight: bold;
            }}
            .certificate-message {{
                font-size: 20px;
                margin: 20px 0;
                line-height: 1.5;
            }}
            .certificate-score {{
                font-size: 24px;
                margin: 20px 0;
                color: #1E88E5;
                font-weight: bold;
            }}
            .certificate-date {{
                font-size: 18px;
                margin: 20px 0 40px 0;
            }}
            .certificate-signature {{
                margin: 60px auto 0 auto;
                border-top: 1px solid #333;
                width: 200px;
                padding-top: 10px;
                font-size: 16px;
            }}
            .certificate-footer {{
                font-size: 14px;
                margin-top: 50px;
                color: #777;
            }}
        </style>
    </head>
    <body>
        <div class="certificate">
            <div class="certificate-header">Certificate of Completion</div>
            <div class="certificate-title">Forklift Operator Safety Training</div>
            <p class="certificate-message">This certifies that</p>
            <div class="certificate-recipient">{name}</div>
            <p class="certificate-message">has successfully completed the Forklift Operator Safety Quiz</p>
            <div class="certificate-score">with a score of {score}%</div>
            <div class="certificate-date">Date of Completion: {date}</div>
            <div class="certificate-signature">Training Director</div>
            <div class="certificate-footer">This certificate validates that the recipient has demonstrated knowledge of forklift safety procedures and is qualified in accordance with OSHA standards for the operation of forklifts.</div>
        </div>
    </body>
    </html>
    """
    
    return html