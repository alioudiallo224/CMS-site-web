import sqlite3
import datetime


class Database():
    def __init__(self):
        self.connection = None

    def get_connection(self):
        if self.connection is None:
            self.connection = sqlite3.connect('db/article.db')
        return self.connection

    def disconnect(self):
        if self.connection is not None:
            self.connection.close()

    def get_all_articles(self):
        cursor = self.get_connection().cursor()
        cursor.execute("SELECT * FROM article ORDER BY date_publication")
        articles = cursor.fetchall()
        return articles

    def add_article(self, titre, identifiant, auteur,
                    date_publication, paragraphe):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute("INSERT INTO article(auteur, titre, identifiant,"
                       "date_publication, paragraphe)"
                       "VALUES(?,?,?,?,?)", (titre,  identifiant, auteur,
                                             date_publication, paragraphe))
        connection.commit()

    def get_article_by_id(self, id):
        cursor = self.get_connection().cursor()
        cursor.execute("SELECT * FROM article WHERE id = %d" % id)
        article = cursor.fetchall()
        return article

    def get_5derniers_articles(self):
        cursor = self.get_connection().cursor()
        date_today = datetime.date.today()
        cursor.execute("select * from article where date_publication"
                       "<= ? limit 5", (date_today,))
        cinq_derniers_articles = cursor.fetchall()
        return cinq_derniers_articles

    def get_search(self, texte):
        cursor = self.get_connection().cursor()
        cursor.execute(("select * from article where titre like ?"
                        "or paragraphe like ?"), ('%'+texte+'%',
                                                  '%'+texte+'%'))
        articles_cherches = cursor.fetchall()
        return articles_cherches

    def modifie_article(self, titre, paragraphe, identifiant):
        connection = self.get_connection()
        cursor = connection.cursor()
        cursor.execute("UPDATE article SET titre = ?, paragraphe = ?"
                       "WHERE id = ?",
                       (titre,  paragraphe, identifiant))
        connection.commit()
