import os
import json

from flask import Flask, request, jsonify
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from prometheus_flask_exporter import PrometheusMetrics

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://admin:admin@postgres:5432/database")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Movie(Base):
    __tablename__ = "movies"
    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String)
    ano = Column(Integer)
    diretor = Column(String)

Base.metadata.create_all(bind=engine)

app = Flask(__name__)
PrometheusMetrics(app)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.route("/", methods=["GET"])
def home():
    return jsonify({"mensagem": "Bem-vindo à API de Filmes!"})

@app.route("/movies/", methods=["POST"])
def create_movie():
    db = next(get_db())
    data = request.get_json()
    db_movie = Movie(**data)
    db.add(db_movie)
    db.commit()
    db.refresh(db_movie)
    return jsonify({"id": db_movie.id, "titulo": db_movie.titulo, "ano": db_movie.ano, "diretor": db_movie.diretor}), 201

@app.route("/movies/<int:movie_id>", methods=["GET"])
def read_movie(movie_id):
    db = next(get_db())
    movie = db.query(Movie).filter(Movie.id == movie_id).first()
    if not movie:
        return jsonify({"error": "Filme não encontrado"}), 404
    return jsonify({"id": movie.id, "titulo": movie.titulo, "ano": movie.ano, "diretor": movie.diretor})

@app.route("/movies/", methods=["GET"])
def list_movies():
    db = next(get_db())
    movies = db.query(Movie).all()
    return jsonify([{"id": movie.id, "titulo": movie.titulo, "ano": movie.ano, "diretor": movie.diretor} for movie in movies])

@app.route("/movies/<int:movie_id>", methods=["PUT"])
def update_movie(movie_id):
    db = next(get_db())
    movie = db.query(Movie).filter(Movie.id == movie_id).first()
    if not movie:
        return jsonify({"error": "Filme não encontrado"}), 404
    data = request.get_json()
    for key, value in data.items():
        setattr(movie, key, value)
    db.commit()
    db.refresh(movie)
    return jsonify({"id": movie.id, "titulo": movie.titulo, "ano": movie.ano, "diretor": movie.diretor})

@app.route("/movies/<int:movie_id>", methods=["DELETE"])
def delete_movie(movie_id):
    db = next(get_db())
    movie = db.query(Movie).filter(Movie.id == movie_id).first()
    if not movie:
        return jsonify({"error": "Filme não encontrado"}), 404
    db.delete(movie)
    db.commit()
    return jsonify({"mensagem": "Filme deletado com sucesso"}), 204

@app.route("/error", methods=["GET"])
def error():
    return jsonify({"error": "Erro"}), 500

@app.route("/report", methods=["GET"])
def report():
    db = next(get_db())
    movies = db.query(Movie).all()
    data = {
        "movies": [{"id": movie.id, "titulo": movie.titulo, "ano": movie.ano, "diretor": movie.diretor} for movie in movies]
    }
    try:
        with open("report.json", "w") as f:
            json.dump(data, f)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify({"mensagem": "Relatório gerado com sucesso"}), 200

@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "ok"})

@app.route("/ready", methods=["GET"])
def ready_check():
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    app.run()
