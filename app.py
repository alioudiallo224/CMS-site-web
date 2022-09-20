from flask import Flask
from database import Database
from flask import Flask, request, render_template, g, redirect
import datetime

app = Flask(__name__)


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        g._database = Database()
    return g._database


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.disconnect()


@app.route("/")
def acceuil():
    articles = get_db().get_5derniers_articles()
    if len(articles) == 0:
        return render_template("recherche.html", error="Aucun article!")
    return render_template("acceuil.html", articles=articles)


@app.route("/article/<int:id>", methods=['GET', 'POST'])
def article(id):
    article = get_db().get_article_by_id(id)
    if article is None:
        return Response(status=404)
    return render_template("article.html", article=article[0])


@app.route("/confirmation", methods=['GET', 'POST'])
def confirmation():
    personnes = get_db().get_all_articles()
    return render_template("confirmation.html", personnes=personnes)


@app.route("/admin")
def admin():
    articles = get_db().get_all_articles()
    if len(articles) == 0:
        return render_template("recherche.html", error="Aucun article!")
    return render_template("admin.html", articles=articles)


@app.route("/recherche", methods=['GET', 'POST'])
def recherche():
    recherche = request.form["recherche"]
    articles = get_db().get_search(recherche)
    if recherche == "" or len(articles) == 0:
        return render_template("recherche.html",
                               error="Aucun article ne correspond "
                               "à votre recherche!")
    return render_template("recherche.html", articles=articles)


@app.route('/admin-nouveau', methods=['GET', 'POST'])
def home():
    if request.method == 'GET':
        return render_template("admin-nouveau.html")
    else:
        auteur = request.form["auteur"]
        titre = request.form["titre"]
        identifiant = request.form["identifiant"]
        date_publication = request.form["date_publication"]
        paragraphe = request.form["paragraphe"]
    if (titre == "" or auteur == "" or paragraphe == ""
                 or date_publication == "" or identifiant == ""):
        return render_template("admin-nouveau.html",
                               error="Tous les champs sont"
                               " obligatoires!")
    elif date_publication < str(datetime.date.today()):
        return render_template("admin-nouveau.html",
                               error="La date est invalide")
    else:
        get_db().add_article(titre, identifiant, auteur,
                             date_publication, paragraphe)
        return redirect("/confirmation")


@app.route("/modification-article/<int:id>", methods=['GET', 'POST'])
def modification_article(id):
    if request.method == 'GET':
        return render_template("modification-article.html", id=id)
    else:
        titre = request.form["titrer"]
        paragraphe = request.form["paragraphe"]

    if titre == "" or paragraphe == "":
        return render_template("modification-article",
                               error="Tous les champs sont"
                               " obligatoires!")
    else:
        get_db().modifie_article(titre, paragraphe, id)
        return redirect("/confirmation")
