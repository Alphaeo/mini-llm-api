from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from .api.endpoints import router as api_router
import os

app = FastAPI()

# Mount static files (for favicon)
static_dir = os.path.join(os.path.dirname(__file__), "static")
app.mount("/static", StaticFiles(directory=static_dir), name="static")

@app.get("/", response_class=HTMLResponse)
async def root():
    return """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Mini LLM API</title>
    <link rel="icon" type="image/x-icon" href="/static/favicon.ico">
    <meta name="viewport" content="width=device-width, initial-scale=1">

    <style>
        :root {
            --bg: #0f172a;
            --card: #020617;
            --accent: #38bdf8;
            --text: #e5e7eb;
            --muted: #94a3b8;
            --border: #1e293b;
        }

        * { box-sizing: border-box; }

        body {
            margin: 0;
            font-family: system-ui, -apple-system, BlinkMacSystemFont, sans-serif;
            background: linear-gradient(180deg, #020617, #020617);
            color: var(--text);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
        }

        .container {
            max-width: 900px;
            width: 100%;
            padding: 2rem;
        }

        .card {
            background: var(--card);
            border: 1px solid var(--border);
            border-radius: 14px;
            padding: 2rem;
            box-shadow: 0 20px 40px rgba(0,0,0,0.4);
        }

        h1 {
            margin-top: 0;
            font-size: 1.8rem;
            margin-bottom: 0.5rem;
        }

        .subtitle {
            color: var(--muted);
            margin-bottom: 2rem;
        }

        label {
            display: block;
            margin-bottom: 1rem;
            font-size: 0.9rem;
            color: var(--muted);
        }

        textarea, input {
            width: 100%;
            margin-top: 0.4rem;
            padding: 0.6rem 0.7rem;
            font-size: 0.95rem;
            border-radius: 8px;
            border: 1px solid var(--border);
            background: #020617;
            color: var(--text);
        }

        textarea {
            resize: vertical;
            min-height: 80px;
        }

        .row {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 1rem;
            margin-bottom: 1rem;
        }

        button {
            margin-top: 1rem;
            padding: 0.7rem 1.2rem;
            font-size: 1rem;
            border-radius: 10px;
            border: none;
            background: linear-gradient(135deg, #38bdf8, #0ea5e9);
            color: #020617;
            font-weight: 600;
            cursor: pointer;
            transition: transform 0.05s ease, opacity 0.2s;
        }

        button:disabled {
            opacity: 0.6;
            cursor: not-allowed;
        }

        button:active {
            transform: scale(0.98);
        }

        .response {
            margin-top: 1.5rem;
            padding: 1rem;
            background: #020617;
            border: 1px solid var(--border);
            border-radius: 10px;
            min-height: 120px;
            white-space: pre-wrap;
            font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
            font-size: 0.9rem;
            line-height: 1.4;
        }

        .status {
            margin-top: 0.5rem;
            font-size: 0.85rem;
            color: var(--muted);
        }

        .cursor {
            display: inline-block;
            width: 8px;
            background: var(--accent);
            margin-left: 2px;
            animation: blink 1s infinite;
        }

        @keyframes blink {
            0%, 50%, 100% { opacity: 1; }
            25%, 75% { opacity: 0; }
        }

        footer {
            margin-top: 1rem;
            text-align: center;
            font-size: 0.8rem;
            color: var(--muted);
        }
    </style>
</head>
<body>
<div class="container">
    <div class="card">
        <h1>Mini LLM API</h1>
        <div class="subtitle">FastAPI · Streaming tokens · vLLM / mock backend</div>

        <form id="chat-form">
            <label>
                Prompt
                <textarea id="prompt" required placeholder="Ask something…"></textarea>
            </label>

            <div class="row">
                <label>
                    Temperature
                    <input type="number" step="0.01" min="0" max="1" id="temperature" value="0.7">
                </label>
                <label>
                    Max tokens
                    <input type="number" min="1" max="1024" id="max_tokens" value="100">
                </label>
            </div>

            <button id="send-btn" type="submit">Send (stream)</button>
        </form>

        <div class="response" id="response"></div>
        <div class="status" id="status"></div>
    </div>

    <footer>
        Streaming demo · No frontend framework · Pure FastAPI
    </footer>
</div>

<script>
document.getElementById('chat-form').onsubmit = async function(e) {
    e.preventDefault();

    const prompt = document.getElementById('prompt').value;
    const temperature = parseFloat(document.getElementById('temperature').value);
    const max_tokens = parseInt(document.getElementById('max_tokens').value);

    const responseDiv = document.getElementById('response');
    const statusDiv = document.getElementById('status');
    const button = document.getElementById('send-btn');

    responseDiv.innerText = "";
    statusDiv.innerText = "Streaming response…";
    button.disabled = true;

    const res = await fetch('/chat/stream', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({prompt, temperature, max_tokens})
    });

    if (!res.body) {
        responseDiv.innerText = "No response stream.";
        button.disabled = false;
        return;
    }

    const reader = res.body.getReader();
    const decoder = new TextDecoder();
    let done = false;

    while (!done) {
        const { value, done: doneReading } = await reader.read();
        done = doneReading;
        if (value) {
            responseDiv.innerText += decoder.decode(value);
        }
    }

    statusDiv.innerText = "Completed.";
    button.disabled = false;
};
</script>
</body>
</html>
"""


app.include_router(api_router)