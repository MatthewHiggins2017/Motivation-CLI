#!/usr/bin/env python3
"""
Local Flask app for managing the Motivation Page database.
Run locally to add new quotes and poems via a web form.
"""

import json
import uuid
from pathlib import Path
from flask import Flask, render_template_string, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = "motivation-page-local-dev"

# Paths
BASE_DIR = Path(__file__).parent
DATA_FILE = BASE_DIR / "data" / "entries.json"

def load_data():
    """Load entries from JSON database."""
    if not DATA_FILE.exists():
        return {"quotes": [], "poems": []}
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_data(data):
    """Save entries to JSON database."""
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Daily Inspiration</title>
    <style>
        :root {
            --bg-color: #ffffff;
            --text-color: #2d3436;
            --secondary-color: #636e72;
            --border-color: #dfe6e9;
            --accent-color: #6c5ce7;
            --success-color: #00b894;
            --error-color: #d63031;
            --card-bg: #f8f9fa;
        }
        
        @media (prefers-color-scheme: dark) {
            :root {
                --bg-color: #0d1117;
                --text-color: #e6edf3;
                --secondary-color: #8b949e;
                --border-color: #21262d;
                --accent-color: #a29bfe;
                --card-bg: #161b22;
            }
        }
        
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            background-color: var(--bg-color);
            color: var(--text-color);
            line-height: 1.8;
            min-height: 100vh;
        }
        
        .container {
            max-width: 680px;
            margin: 0 auto;
            padding: 3rem 2rem;
        }
        
        .admin-icon {
            position: fixed;
            top: 1.5rem;
            right: 1.5rem;
            width: 40px;
            height: 40px;
            display: flex;
            align-items: center;
            justify-content: center;
            background: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: 50%;
            color: var(--secondary-color);
            text-decoration: none;
            transition: all 0.2s ease;
            z-index: 100;
        }
        
        .admin-icon:hover {
            background: var(--accent-color);
            color: white;
            border-color: var(--accent-color);
            transform: scale(1.05);
        }
        
        .admin-icon svg {
            width: 18px;
            height: 18px;
        }
        
        .back-link {
            position: fixed;
            top: 1.5rem;
            left: 1.5rem;
            display: flex;
            align-items: center;
            gap: 0.5rem;
            color: var(--secondary-color);
            text-decoration: none;
            font-size: 0.875rem;
            transition: color 0.2s ease;
        }
        
        .back-link:hover {
            color: var(--accent-color);
        }
        
        header {
            text-align: center;
            margin-bottom: 4rem;
        }
        
        h1 {
            font-size: 1.5rem;
            font-weight: 300;
            letter-spacing: 0.1em;
            text-transform: uppercase;
            margin-bottom: 0.75rem;
            color: var(--secondary-color);
        }
        
        .date {
            font-size: 2.5rem;
            font-weight: 600;
            color: var(--text-color);
        }
        
        h2 {
            font-size: 0.75rem;
            font-weight: 500;
            margin: 3rem 0 1.5rem 0;
            color: var(--secondary-color);
            text-transform: uppercase;
            letter-spacing: 0.15em;
        }
        
        .flash {
            padding: 1rem 1.25rem;
            border-radius: 12px;
            margin-bottom: 1.5rem;
            font-size: 0.9rem;
        }
        
        .flash.success {
            background: rgba(0, 184, 148, 0.1);
            border: 1px solid var(--success-color);
            color: var(--success-color);
        }
        
        .flash.error {
            background: rgba(214, 48, 49, 0.1);
            border: 1px solid var(--error-color);
            color: var(--error-color);
        }
        
        form {
            background: var(--card-bg);
            padding: 2rem;
            border-radius: 16px;
            border: 1px solid var(--border-color);
        }
        
        .form-group {
            margin-bottom: 1.5rem;
        }
        
        label {
            display: block;
            font-weight: 500;
            margin-bottom: 0.5rem;
            font-size: 0.875rem;
            color: var(--secondary-color);
        }
        
        input[type="text"],
        textarea,
        select {
            width: 100%;
            padding: 0.875rem 1rem;
            border: 1px solid var(--border-color);
            border-radius: 10px;
            background: var(--bg-color);
            color: var(--text-color);
            font-family: inherit;
            font-size: 1rem;
            transition: border-color 0.2s ease, box-shadow 0.2s ease;
        }
        
        input[type="text"]:focus,
        textarea:focus,
        select:focus {
            outline: none;
            border-color: var(--accent-color);
            box-shadow: 0 0 0 3px rgba(108, 92, 231, 0.1);
        }
        
        textarea {
            min-height: 120px;
            resize: vertical;
        }
        
        button {
            background: var(--accent-color);
            color: white;
            border: none;
            padding: 0.875rem 2rem;
            border-radius: 10px;
            font-size: 1rem;
            cursor: pointer;
            font-weight: 500;
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }
        
        button:hover {
            transform: translateY(-1px);
            box-shadow: 0 4px 12px rgba(108, 92, 231, 0.3);
        }
        
        .entry {
            padding: 1.5rem;
            margin-bottom: 1.5rem;
        }
        
        .entry-text {
            font-size: 1.25rem;
            font-style: italic;
            margin-bottom: 1rem;
            line-height: 1.7;
        }
        
        .entry-author {
            color: var(--secondary-color);
            font-size: 0.9rem;
        }
        
        .stats {
            display: flex;
            gap: 2rem;
            margin-bottom: 2rem;
            justify-content: center;
        }
        
        .stat {
            text-align: center;
            padding: 1.5rem 2rem;
            background: var(--card-bg);
            border-radius: 12px;
            border: 1px solid var(--border-color);
        }
        
        .stat-value {
            font-size: 2.5rem;
            font-weight: 600;
            color: var(--accent-color);
        }
        
        .stat-label {
            font-size: 0.8rem;
            color: var(--secondary-color);
            text-transform: uppercase;
            letter-spacing: 0.1em;
        }
    </style>
</head>
<body>
    <div class="container">
    {% with messages = get_flashed_messages(with_categories=true) %}
        {% for category, message in messages %}
            <div class="flash {{ category }}">{{ message }}</div>
        {% endfor %}
    {% endwith %}
    
    {% block content %}{% endblock %}
    </div>
</body>
</html>
'''

INDEX_TEMPLATE = '''
{% extends "base" %}
{% block content %}
    <a href="{{ url_for('add_page') }}" class="admin-icon" title="Add new entry">
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
            <path stroke-linecap="round" stroke-linejoin="round" d="M12 4v16m8-8H4" />
        </svg>
    </a>
    
    <header>
        <h1>Daily Inspiration</h1>
        <p class="date">{{ today }}</p>
    </header>
    
    <h2>Today's Quotes</h2>
    {% for quote in quotes %}
    <div class="entry">
        <p class="entry-text">"{{ quote.text }}"</p>
        <p class="entry-author">— {{ quote.author }}</p>
    </div>
    {% endfor %}
    
    <h2>Today's Poem</h2>
    {% if poem %}
    <div class="entry">
        <p class="entry-text">{{ poem.text|replace('\n', '<br>')|safe }}</p>
        <p class="entry-author">— {{ poem.author }}</p>
    </div>
    {% else %}
    <p style="color: var(--secondary-color); text-align: center;">No poem available</p>
    {% endif %}
{% endblock %}
'''

ADD_TEMPLATE = '''
{% extends "base" %}
{% block content %}
    <a href="{{ url_for('index') }}" class="back-link">
        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
            <path stroke-linecap="round" stroke-linejoin="round" d="M15 19l-7-7 7-7" />
        </svg>
        Back
    </a>
    
    <header>
        <h1>Add Entry</h1>
        <p class="date" style="font-size: 1rem; font-weight: 400;">Add a new quote or poem</p>
    </header>
    
    <div class="stats">
        <div class="stat">
            <div class="stat-value">{{ quotes|length }}</div>
            <div class="stat-label">Quotes</div>
        </div>
        <div class="stat">
            <div class="stat-value">{{ poems|length }}</div>
            <div class="stat-label">Poems</div>
        </div>
    </div>
    
    <form method="POST" action="{{ url_for('add_entry') }}">
        <div class="form-group">
            <label for="type">Type</label>
            <select name="type" id="type" required>
                <option value="quote">Quote</option>
                <option value="poem">Poem</option>
            </select>
        </div>
        
        <div class="form-group">
            <label for="text">Text</label>
            <textarea name="text" id="text" required placeholder="Enter the quote or poem text..."></textarea>
        </div>
        
        <div class="form-group">
            <label for="author">Author</label>
            <input type="text" name="author" id="author" required placeholder="Author name">
        </div>
        
        <div class="form-group">
            <label for="history">History / Context (optional)</label>
            <textarea name="history" id="history" placeholder="Background information about this entry..."></textarea>
        </div>
        
        <div class="form-group">
            <label for="images">Image URLs (optional, comma-separated)</label>
            <input type="text" name="images" id="images" placeholder="https://example.com/image1.jpg">
        </div>
        
        <button type="submit">Add Entry</button>
    </form>
{% endblock %}
'''

PREVIEW_TEMPLATE = '''
{% extends "base" %}
{% block content %}
    <a href="{{ url_for('index') }}" class="back-link">
        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
            <path stroke-linecap="round" stroke-linejoin="round" d="M15 19l-7-7 7-7" />
        </svg>
        Back
    </a>
    
    <header>
        <h1>Regenerate Page</h1>
        <p class="date" style="font-size: 1rem; font-weight: 400;">
            <a href="{{ url_for('regenerate') }}" style="color: var(--accent-color); text-decoration: none;">Click to regenerate static page</a>
        </p>
    </header>
{% endblock %}
'''

def render_with_base(content_template):
    """Combine base template with content template."""
    content = content_template.replace('{% extends "base" %}', '').replace('{% block content %}', '').replace('{% endblock %}', '')
    return HTML_TEMPLATE.replace('{% block content %}{% endblock %}', content)

@app.route("/")
def index():
    import random
    from datetime import date
    
    data = load_data()
    today_date = date.today()
    seed = int(today_date.strftime("%Y%m%d"))
    rng = random.Random(seed)
    
    quotes = data.get("quotes", [])
    poems = data.get("poems", [])
    
    selected_quotes = rng.sample(quotes, min(3, len(quotes)))
    selected_poem = rng.choice(poems) if poems else None
    
    today = today_date.strftime("%B %d, %Y")
    
    return render_template_string(
        render_with_base(INDEX_TEMPLATE),
        quotes=selected_quotes,
        poem=selected_poem,
        today=today
    )

@app.route("/add")
def add_page():
    data = load_data()
    return render_template_string(
        render_with_base(ADD_TEMPLATE),
        quotes=data.get("quotes", []),
        poems=data.get("poems", [])
    )

@app.route("/add-entry", methods=["POST"])
def add_entry():
    entry_type = request.form.get("type")
    text = request.form.get("text", "").strip()
    author = request.form.get("author", "").strip()
    history = request.form.get("history", "").strip()
    images_raw = request.form.get("images", "").strip()
    
    if not text or not author:
        flash("Text and author are required", "error")
        return redirect(url_for("add_page"))
    
    images = [img.strip() for img in images_raw.split(",") if img.strip()] if images_raw else []
    
    entry = {
        "id": f"{'q' if entry_type == 'quote' else 'p'}{uuid.uuid4().hex[:8]}",
        "text": text,
        "author": author,
        "history": history,
        "images": images
    }
    
    data = load_data()
    key = "quotes" if entry_type == "quote" else "poems"
    data[key].append(entry)
    save_data(data)
    
    flash(f"Added new {entry_type}!", "success")
    return redirect(url_for("add_page"))

@app.route("/preview")
def preview():
    return render_template_string(
        render_with_base(PREVIEW_TEMPLATE)
    )

@app.route("/regenerate")
def regenerate():
    import subprocess
    try:
        subprocess.run(["python3", "generate_page.py"], cwd=BASE_DIR, check=True)
        flash("Static page regenerated successfully!", "success")
    except subprocess.CalledProcessError as e:
        flash(f"Error regenerating page: {e}", "error")
    return redirect(url_for("index"))

if __name__ == "__main__":
    print("Starting Motivation Page Admin...")
    print("Open http://localhost:5001 in your browser")
    app.run(debug=True, port=5001)
