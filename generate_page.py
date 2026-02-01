#!/usr/bin/env python3
"""
Static page generator for the Motivation Page.
Selects random quotes and poem based on the current date (deterministic daily selection).
Outputs index.html for GitHub Pages.
"""

import json
import random
from datetime import date
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).parent
DATA_FILE = BASE_DIR / "data" / "entries.json"
OUTPUT_FILE = BASE_DIR / "docs" / "index.html"

def load_data():
    """Load entries from JSON database."""
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def select_daily_content(data):
    """
    Select 3 quotes and 1 poem based on the current date.
    Uses the date as a seed for reproducible daily selection.
    """
    today = date.today()
    seed = int(today.strftime("%Y%m%d"))
    
    rng = random.Random(seed)
    
    quotes = data.get("quotes", [])
    poems = data.get("poems", [])
    
    # Select 3 random quotes (or fewer if not enough)
    selected_quotes = rng.sample(quotes, min(3, len(quotes)))
    
    # Select 1 random poem
    selected_poem = rng.choice(poems) if poems else None
    
    return selected_quotes, selected_poem

def generate_html(quotes, poem):
    """Generate the static HTML page."""
    today = date.today().strftime("%B %d, %Y")
    
    quotes_html = ""
    for q in quotes:
        images_html = ""
        if q.get("images"):
            images_html = '<div class="images">' + "".join(
                f'<img src="{img}" alt="Quote image">' for img in q["images"]
            ) + '</div>'
        
        quotes_html += f'''
        <div class="entry">
            <p class="entry-text">"{q["text"]}"</p>
            <p class="entry-author">— {q["author"]}</p>
            {images_html}
        </div>
        '''
    
    poem_html = ""
    if poem:
        poem_text = poem["text"].replace("\n", "<br>")
        images_html = ""
        if poem.get("images"):
            images_html = '<div class="images">' + "".join(
                f'<img src="{img}" alt="Poem image">' for img in poem["images"]
            ) + '</div>'
        
        poem_html = f'''
        <div class="entry">
            <p class="entry-text">{poem_text}</p>
            <p class="entry-author">— {poem["author"]}</p>
            {images_html}
        </div>
        '''
    
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Daily Inspiration</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap" rel="stylesheet">
    <style>
        :root {{
            --bg-color: #ffffff;
            --text-color: #2d3436;
            --secondary-color: #636e72;
            --border-color: #dfe6e9;
            --accent-color: #6c5ce7;
        }}
        
        @media (prefers-color-scheme: dark) {{
            :root {{
                --bg-color: #0d1117;
                --text-color: #e6edf3;
                --secondary-color: #8b949e;
                --border-color: #21262d;
                --accent-color: #a29bfe;
            }}
        }}
        
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            background-color: var(--bg-color);
            color: var(--text-color);
            line-height: 1.8;
            min-height: 100vh;
        }}
        
        .container {{
            max-width: 680px;
            margin: 0 auto;
            padding: 3rem 2rem;
        }}
        
        header {{
            text-align: center;
            margin-bottom: 4rem;
        }}
        
        h1 {{
            font-size: 1.5rem;
            font-weight: 300;
            letter-spacing: 0.1em;
            text-transform: uppercase;
            margin-bottom: 0.75rem;
            color: var(--secondary-color);
        }}
        
        .date {{
            font-size: 2.5rem;
            font-weight: 600;
            color: var(--text-color);
        }}
        
        h2 {{
            font-size: 0.75rem;
            font-weight: 500;
            margin: 3rem 0 1.5rem 0;
            color: var(--secondary-color);
            text-transform: uppercase;
            letter-spacing: 0.15em;
        }}
        
        .entry {{
            padding: 1.5rem;
            margin-bottom: 1.5rem;
        }}
        
        .entry-text {{
            font-size: 1.25rem;
            font-style: italic;
            margin-bottom: 1rem;
            line-height: 1.7;
        }}
        
        .entry-author {{
            color: var(--secondary-color);
            font-size: 0.9rem;
        }}
        
        .images {{
            margin-top: 1.5rem;
            display: flex;
            gap: 0.75rem;
            flex-wrap: wrap;
        }}
        
        .images img {{
            max-width: 200px;
            border-radius: 8px;
        }}
        
        footer {{
            margin-top: 4rem;
            text-align: center;
            color: var(--secondary-color);
            font-size: 0.8rem;
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>Daily Inspiration</h1>
            <p class="date">{today}</p>
        </header>
        
        <main>
            <h2>Today's Quotes</h2>
            {quotes_html}
            
            <h2>Today's Poem</h2>
            {poem_html}
        </main>
        
        <footer>
            <p>New inspiration every day</p>
        </footer>
    </div>
</body>
</html>
'''
    return html

def main():
    """Main entry point."""
    # Ensure output directory exists
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    
    # Load data and select content
    data = load_data()
    quotes, poem = select_daily_content(data)
    
    # Generate and write HTML
    html = generate_html(quotes, poem)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(html)
    
    print(f"Generated {OUTPUT_FILE}")
    print(f"Selected {len(quotes)} quotes and {'1 poem' if poem else 'no poem'}")

if __name__ == "__main__":
    main()
