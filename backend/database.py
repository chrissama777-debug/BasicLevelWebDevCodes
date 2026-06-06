from __future__ import annotations

import json
import os
from pathlib import Path

from flask import Flask

from .models import Phone, Review, SavedComparison, User, db

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = BASE_DIR / "data" / "phones.json"
DB_FILE = BASE_DIR / "instance" / "capstone.sqlite3"


def configure_database(app: Flask) -> None:
    app.config.setdefault("SQLALCHEMY_DATABASE_URI", f"sqlite:///{DB_FILE.as_posix()}")
    app.config.setdefault("SQLALCHEMY_TRACK_MODIFICATIONS", False)
    app.config.setdefault("JSON_SORT_KEYS", False)
    db.init_app(app)


def ensure_schema(app: Flask) -> None:
    with app.app_context():
        os.makedirs(DB_FILE.parent, exist_ok=True)
        db.create_all()
        seed_database()


def load_phone_seed_data() -> list[dict]:
    with open(DATA_FILE, "r", encoding="utf-8") as handle:
        return json.load(handle)


def seed_database() -> None:
    if Phone.query.count() == 0:
        for entry in load_phone_seed_data():
            db.session.add(Phone(**entry))
        db.session.commit()

    if not User.query.filter_by(email="admin@demo.com").first():
        import bcrypt

        password_hash = bcrypt.hashpw(b"Admin@123", bcrypt.gensalt()).decode("utf-8")
        db.session.add(User(name="Administrator", email="admin@demo.com", password_hash=password_hash, role="admin"))
        db.session.commit()
