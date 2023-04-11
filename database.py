from sqlalchemy import create_engine, text

db_connection_string = "mysql+pymysql://cqdgsa810jsi46eqskeq:pscale_pw_iW0BmPRy2XIQ9PFdDXRFmIBgHp6eiiuxIPxW2cKRxKL@ap-south.connect.psdb.cloud/myapp?charset=utf8mb4"
engine = create_engine(db_connection_string,
                       connect_args={"ssl": {
                         "ssl_ca": "/etc/ssl/cert.pem"
                       }})


def load_jobs_from_db():
  with engine.connect() as con:
    result = con.execute(text("select * from job"))
    jobs = []
    for row in result.all():
      jobs.append(row._mapping)
    return jobs


def application_to_db(data):
  with engine.connect() as conn:
    query = text(
      "INSERT INTO job (title,Address,link,mob,category) VALUES (:title,:Address,:link,:mob,:category)"
    )

    conn.execute(
      query, {
        "title": data["title"],
        "Address": data["Address"],
        "link": data["link"],
        "mob": data["mob"],
        "category": data["category"]
      })
