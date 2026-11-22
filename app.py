"""
AutoDeploy - Automated CI/CD Web Application
A lightweight, production-ready Flask application demonstrating an automated
CI/CD pipeline with GitHub Actions, Docker, and Render.
"""

import os
from datetime import datetime, timezone
from flask import Flask, jsonify, render_template_string

# Initialize Flask application
app = Flask(__name__)

# Application metadata
APP_NAME = "AutoDeploy"
APP_VERSION = "1.0.0"

# Professional, modern HTML & CSS template embedded directly into the app
HOME_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ app_name }} - Automated CI/CD Pipeline</title>
    <style>
        :root {
            --bg-color: #0f172a;
            --card-bg: #1e293b;
            --card-border: #334155;
            --text-primary: #f8fafc;
            --text-secondary: #94a3b8;
            --accent-blue: #38bdf8;
            --accent-green: #22c55e;
            --accent-purple: #a855f7;
            --code-bg: #090d16;
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            background-color: var(--bg-color);
            color: var(--text-primary);
            line-height: 1.6;
            min-height: 100vh;
            padding: 2rem 1rem;
            display: flex;
            flex-direction: column;
            align-items: center;
        }

        .container {
            max-width: 900px;
            width: 100%;
        }

        header {
            text-align: center;
            margin-bottom: 2.5rem;
        }

        .badge-status {
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            background: rgba(34, 197, 94, 0.15);
            color: var(--accent-green);
            border: 1px solid rgba(34, 197, 94, 0.3);
            padding: 0.35rem 1rem;
            border-radius: 9999px;
            font-size: 0.875rem;
            font-weight: 600;
            margin-bottom: 1rem;
        }

        .status-dot {
            width: 8px;
            height: 8px;
            background-color: var(--accent-green);
            border-radius: 50%;
            box-shadow: 0 0 10px var(--accent-green);
            animation: pulse 2s infinite;
        }

        @keyframes pulse {
            0%, 100% { opacity: 1; transform: scale(1); }
            50% { opacity: 0.4; transform: scale(0.9); }
        }

        h1 {
            font-size: 2.75rem;
            font-weight: 800;
            letter-spacing: -0.025em;
            background: linear-gradient(135deg, #38bdf8 0%, #818cf8 50%, #c084fc 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 0.75rem;
        }

        .subtitle {
            font-size: 1.15rem;
            color: var(--text-secondary);
            max-width: 600px;
            margin: 0 auto;
        }

        .card {
            background-color: var(--card-bg);
            border: 1px solid var(--card-border);
            border-radius: 1rem;
            padding: 1.75rem;
            margin-bottom: 1.75rem;
            box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3);
        }

        h2 {
            font-size: 1.35rem;
            font-weight: 700;
            margin-bottom: 1rem;
            display: flex;
            align-items: center;
            gap: 0.5rem;
            color: var(--accent-blue);
        }

        /* Pipeline Workflow Grid */
        .pipeline-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
            gap: 1rem;
            margin-top: 1rem;
        }

        .step-card {
            background: rgba(15, 23, 42, 0.6);
            border: 1px solid var(--card-border);
            border-radius: 0.75rem;
            padding: 1.25rem 1rem;
            text-align: center;
            position: relative;
            transition: transform 0.2s, border-color 0.2s;
        }

        .step-card:hover {
            transform: translateY(-3px);
            border-color: var(--accent-blue);
        }

        .step-num {
            font-size: 0.75rem;
            font-weight: 700;
            color: var(--accent-purple);
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-bottom: 0.25rem;
        }

        .step-title {
            font-weight: 600;
            font-size: 1rem;
            margin-bottom: 0.35rem;
        }

        .step-desc {
            font-size: 0.8rem;
            color: var(--text-secondary);
        }

        /* Endpoints section */
        .endpoint-list {
            display: flex;
            flex-direction: column;
            gap: 0.75rem;
        }

        .endpoint-item {
            display: flex;
            align-items: center;
            justify-content: space-between;
            background: var(--code-bg);
            border: 1px solid var(--card-border);
            padding: 0.85rem 1.25rem;
            border-radius: 0.5rem;
            font-family: monospace;
            font-size: 0.95rem;
        }

        .endpoint-method {
            background: rgba(56, 189, 248, 0.15);
            color: var(--accent-blue);
            padding: 0.2rem 0.5rem;
            border-radius: 0.25rem;
            font-weight: bold;
            font-size: 0.8rem;
            margin-right: 0.75rem;
        }

        .endpoint-path a {
            color: var(--text-primary);
            text-decoration: none;
            transition: color 0.2s;
        }

        .endpoint-path a:hover {
            color: var(--accent-blue);
            text-decoration: underline;
        }

        .endpoint-desc {
            font-family: sans-serif;
            font-size: 0.85rem;
            color: var(--text-secondary);
        }

        /* Tech stack pills */
        .tech-tags {
            display: flex;
            flex-wrap: wrap;
            gap: 0.5rem;
            margin-top: 0.75rem;
        }

        .tag {
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid var(--card-border);
            padding: 0.3rem 0.75rem;
            border-radius: 0.35rem;
            font-size: 0.8rem;
            color: var(--text-secondary);
        }

        footer {
            margin-top: 2rem;
            text-align: center;
            font-size: 0.85rem;
            color: var(--text-secondary);
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <div class="badge-status">
                <span class="status-dot"></span>
                <span>Application Status: Running</span>
            </div>
            <h1>{{ app_name }}</h1>
            <p class="subtitle">Production-grade automated CI/CD pipeline built with Flask, Pytest, Docker, GitHub Actions, and Render.</p>
        </header>

        <div class="card">
            <h2>🚀 Continuous Integration & Deployment Pipeline</h2>
            <p>Every git push and pull request is automatically analyzed, tested, packaged, and continuously deployed:</p>
            <div class="pipeline-grid">
                <div class="step-card">
                    <div class="step-num">Step 1</div>
                    <div class="step-title">Git Commit</div>
                    <div class="step-desc">Developer pushes code to main or creates a pull request.</div>
                </div>
                <div class="step-card">
                    <div class="step-num">Step 2</div>
                    <div class="step-title">Pytest CI</div>
                    <div class="step-desc">GitHub Actions runs automated unit tests with Flask client.</div>
                </div>
                <div class="step-card">
                    <div class="step-num">Step 3</div>
                    <div class="step-title">Docker Build</div>
                    <div class="step-desc">Validates reproducible container image on Python 3.11-slim.</div>
                </div>
                <div class="step-card">
                    <div class="step-num">Step 4</div>
                    <div class="step-title">Render CD</div>
                    <div class="step-desc">Automatic live deployment triggered only when CI passes.</div>
                </div>
            </div>
        </div>

        <div class="card">
            <h2>🔌 Application Endpoints</h2>
            <div class="endpoint-list">
                <div class="endpoint-item">
                    <div>
                        <span class="endpoint-method">GET</span>
                        <span class="endpoint-path"><a href="/">/</a></span>
                    </div>
                    <span class="endpoint-desc">Homepage & Pipeline Overview</span>
                </div>
                <div class="endpoint-item">
                    <div>
                        <span class="endpoint-method">GET</span>
                        <span class="endpoint-path"><a href="/health">/health</a></span>
                    </div>
                    <span class="endpoint-desc">Health Check & Monitoring API</span>
                </div>
                <div class="endpoint-item">
                    <div>
                        <span class="endpoint-method">GET</span>
                        <span class="endpoint-path"><a href="/api/info">/api/info</a></span>
                    </div>
                    <span class="endpoint-desc">Application Metadata & Telemetry</span>
                </div>
            </div>
        </div>

        <div class="card">
            <h2>🛠️ Technology Stack</h2>
            <div class="tech-tags">
                <span class="tag">Python 3.11</span>
                <span class="tag">Flask 3.1</span>
                <span class="tag">Gunicorn WSGI</span>
                <span class="tag">Pytest</span>
                <span class="tag">Docker</span>
                <span class="tag">GitHub Actions</span>
                <span class="tag">Render Cloud</span>
                <span class="tag">AWS Cloud</span>
                <span class="tag">This is Mohit 1st project on CI/CD</span>
            </div>
        </div>

        <footer>
            <p>&copy; {{ current_year }} {{ app_name }} &bull; Automated DevOps CI/CD Showcase</p>
        </footer>
    </div>
</body>
</html>
"""


@app.route("/")
def homepage():
    """
    Homepage endpoint.
    Displays application name, running status, and pipeline architecture.
    """
    return render_template_string(
        HOME_TEMPLATE,
        app_name=APP_NAME,
        current_year=datetime.now(timezone.utc).year
    ), 200


@app.route("/health")
def health_check():
    """
    Health check endpoint for monitoring and uptime probes.
    Returns standard JSON health response.
    """
    return jsonify({
        "status": "healthy",
        "application": APP_NAME
    }), 200


@app.route("/api/info")
def application_info():
    """
    Application information endpoint.
    Returns metadata about the running application and CI/CD environment.
    """
    return jsonify({
        "application": APP_NAME,
        "version": APP_VERSION,
        "status": "Running",
        "description": "Automated CI/CD Pipeline demonstration with GitHub Actions, Docker & Render",
        "environment": os.environ.get("FLASK_ENV", "production"),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "endpoints": {
            "homepage": "/",
            "health": "/health",
            "info": "/api/info"
        }
    }), 200


if __name__ == "__main__":
    # Support dynamic PORT configuration from environment (e.g. Render, Heroku)
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
