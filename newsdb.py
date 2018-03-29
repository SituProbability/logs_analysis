"""Database code for the reporting tool."""

import psycopg2

DBNAME = "news"


def get_popular_articles():
    """Return the most popular articles of all time, most popular first."""
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute("SELECT articles.title, count(*) AS num FROM articles,log "
              "WHERE log.path LIKE concat('%', articles.slug) "
              "GROUP BY articles.title ORDER BY num DESC LIMIT 3;")
    data = c.fetchall()
    db.close()
    return data


def get_popular_authors():
    """Return the most popular article authors of all time."""
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute("SELECT authors.name, count(*) AS num "
              "FROM articles, authors, log "
              "WHERE authors.id = articles.author "
              "AND log.path LIKE concat('%', articles.slug) "
              "GROUP BY authors.name ORDER BY num DESC;")
    data = c.fetchall()
    db.close()
    return data


def get_status_result():
    """Return the result of requests per day."""
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute("SELECT cast(time as date) AS date, count(*) AS num "
              "FROM log GROUP BY date ORDER BY date;")
    data = c.fetchall()
    db.close()
    return data


def get_not_found_result():
    """Return the NOT FOUND result of requests per day."""
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute("SELECT cast(time as date) AS date, count(*) AS num FROM log "
              "WHERE status = '404 NOT FOUND' GROUP BY date ORDER BY date;")
    data = c.fetchall()
    db.close()
    return data
