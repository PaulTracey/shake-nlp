from flask import Flask, render_template, request

from nlp_utils import (
    WORKS,
    get_named_entities,
    get_pos_counts,
    get_work,
    search_work,
    word_frequencies,
)


app = Flask(__name__)


@app.context_processor
def inject_works():
    return {"works": WORKS}


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/works/<slug>")
def work_detail(slug):
    work = get_work(slug)
    return render_template("work.html", work=work)


@app.route("/works/<slug>/frequency")
def frequency(slug):
    work = get_work(slug)
    limit = request.args.get("limit", default=25, type=int)
    terms = word_frequencies(work["text"], limit=limit)
    return render_template("frequency.html", work=work, terms=terms, limit=limit)


@app.route("/works/<slug>/entities")
def entities(slug):
    work = get_work(slug)
    items = get_named_entities(work["text"])
    return render_template("entities.html", work=work, entities=items)


@app.route("/works/<slug>/pos")
def pos_counts(slug):
    work = get_work(slug)
    counts = get_pos_counts(work["text"])
    return render_template("pos.html", work=work, counts=counts)


@app.route("/works/<slug>/search")
def search(slug):
    work = get_work(slug)
    query = request.args.get("q", "").strip()
    results = search_work(work["text"], query)
    return render_template("search.html", work=work, query=query, results=results)


if __name__ == "__main__":
    app.run(debug=True)
