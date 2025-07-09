from fastapi import FastAPI
from .routers import image_classification_router
from .config import setup_logging
from fastapi.responses import HTMLResponse
setup_logging("DEBUG")  # Set the desired log level here, e.g., "DEBUG

app = FastAPI(
    title="AI Tools API",
    description="API for various AI tools",
    version="1.0.0",
    root_path="/api/v1/ai",
)

@app.get("/", tags=["Home"])
def home():
    return HTMLResponse(content="""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>AI Tools API</title>
        <style>
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                margin: 0;
                padding: 0;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
            }
            .container {
                background: white;
                border-radius: 20px;
                padding: 3rem;
                box-shadow: 0 20px 40px rgba(0,0,0,0.1);
                text-align: center;
                max-width: 600px;
            }
            h1 {
                color: #333;
                margin-bottom: 1rem;
                font-size: 2.5rem;
            }
            .subtitle {
                color: #666;
                font-size: 1.2rem;
                margin-bottom: 2rem;
            }
            .features {
                display: grid;
                gap: 1rem;
                margin: 2rem 0;
            }
            .feature {
                background: #f8f9fa;
                padding: 1rem;
                border-radius: 10px;
                border-left: 4px solid #667eea;
            }
            .api-link {
                display: inline-block;
                background: #667eea;
                color: white;
                padding: 12px 24px;
                border-radius: 25px;
                text-decoration: none;
                margin-top: 1rem;
                transition: background 0.3s;
            }
            .api-link:hover {
                background: #5a67d8;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🤖 AI Tools API</h1>
            <p class="subtitle">Your gateway to powerful AI functionalities</p>
            
            <div class="features">
                <div class="feature">
                    <h3>🖼️ Image Classification</h3>
                    <p>Advanced image recognition and classification</p>
                </div>
                <div class="feature">
                    <h3>🚀 Fast & Reliable</h3>
                    <p>Built with FastAPI for optimal performance</p>
                </div>
                <div class="feature">
                    <h3>📚 Well Documented</h3>
                    <p>Complete API documentation available</p>
                </div>
            </div>
            
            <a href="/docs" class="api-link">Explore API Documentation</a>
        </div>
    </body>
    </html>
    """)

app.include_router(image_classification_router)

