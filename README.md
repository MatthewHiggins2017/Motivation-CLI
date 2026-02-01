# Daily Inspiration

A minimalist web app that displays daily inspirational quotes and poems. The content changes each day with a deterministic random selection, ensuring everyone sees the same inspiration on any given day.

## How It Works

### Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        GitHub Repository                         │
├─────────────────────────────────────────────────────────────────┤
│  data/entries.json     ← Your quotes & poems database           │
│  generate_page.py      ← Static page generator                  │
│  docs/index.html       ← Generated static page (GitHub Pages)   │
│  app.py                ← Local Flask admin interface            │
└─────────────────────────────────────────────────────────────────┘
                                │
                    ┌───────────┴───────────┐
                    ▼                       ▼
           GitHub Actions            GitHub Pages
           (Daily at 4am UTC)        (Hosts docs/)
           Regenerates page          Serves to visitors
```

### Public Website (GitHub Pages)

The public-facing site is a **static HTML page** hosted on GitHub Pages from the `docs/` folder. It displays:
- 3 randomly selected quotes
- 1 randomly selected poem

The selection is deterministic based on the date—everyone sees the same content on the same day.

### Daily Regeneration (GitHub Actions)

A GitHub Action automatically regenerates the static page every day:

- **Schedule**: Runs at 4:00 AM UTC daily
- **Process**: 
  1. Checks out the repository
  2. Runs `python generate_page.py`
  3. Commits and pushes the updated `docs/index.html`
- **Manual Trigger**: Can also be run manually via the Actions tab

You don't need any separate process—GitHub Actions handles everything automatically.

### Local Admin Interface (Flask)

Run the Flask app locally to manage your content:

```bash
# Install dependencies
pip install -r requirements.txt

# Run the admin interface
python app.py
```

Open http://localhost:5001 to:
- **Home page**: Preview today's inspiration (same as public site)
- **Add page**: Click the `+` icon to add new quotes or poems

## Setup

### 1. Enable GitHub Pages

1. Go to your repository → Settings → Pages
2. Set Source to "Deploy from a branch"
3. Select `main` branch and `/docs` folder
4. Save

### 2. Verify GitHub Actions

The workflow file at `.github/workflows/daily-update.yml` is already configured. Ensure Actions are enabled in your repository settings.

### 3. Add Content

Run the local Flask app and use the add form, or edit `data/entries.json` directly.

## File Structure

```
├── app.py                 # Flask admin interface (run locally)
├── generate_page.py       # Static page generator script
├── requirements.txt       # Python dependencies
├── data/
│   └── entries.json       # Quote & poem database
├── docs/
│   └── index.html         # Generated static page (served by GitHub Pages)
└── .github/
    └── workflows/
        └── daily-update.yml  # Daily regeneration workflow
```

## Data Format

Entries are stored in `data/entries.json`:

```json
{
  "quotes": [
    {
      "id": "q1",
      "text": "Your quote text here",
      "author": "Author Name",
      "history": "Optional context or history",
      "images": []
    }
  ],
  "poems": [
    {
      "id": "p1", 
      "text": "Poem text\nwith line breaks",
      "author": "Poet Name",
      "history": "Optional context",
      "images": []
    }
  ]
}
```

## FAQ

**Q: Do I need to manually regenerate the page?**  
A: No. GitHub Actions automatically regenerates it daily at 4 AM UTC. You can also trigger it manually from the Actions tab.

**Q: How do I add new quotes/poems?**  
A: Either run `python app.py` locally and use the web form, or edit `data/entries.json` directly and push to GitHub.

**Q: Why is the Flask app not deployed?**  
A: The Flask app is for local administration only. The public site is purely static HTML for simplicity and free hosting on GitHub Pages. 