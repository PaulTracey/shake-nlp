# Shakespeare NLP Explorer

A beginner-friendly Flask and spaCy portfolio project for exploring Shakespeare with natural language processing.

The included works are cleaned public-domain Shakespeare texts. The app includes routes for:

- Word frequency
- Named entities
- Part-of-speech counts
- Sentence search

## Setup

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m spacy download en_core_web_sm
python app.py
```

Open `http://127.0.0.1:5000`.

If `en_core_web_sm` is not installed, the app still runs with a small fallback pipeline. Installing the model gives better entity and part-of-speech results.

## Render Deployment

Use these settings for a Render web service:

```text
Build Command: pip install -r requirements.txt
Start Command: gunicorn app:app
```

The start command belongs in Render's dashboard, not in `requirements.txt`.

## Project Structure

```text
app.py                  Flask routes
nlp_utils.py            spaCy loading and analysis helpers
data/hamlet.txt         Original public-domain source text
data/hamlet_play.txt    Clean reading copy used by the app
data/macbeth_play.txt   Clean Macbeth text used by the app
templates/              Jinja templates
static/css/styles.css   Site styles
```
