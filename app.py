import os
import importlib.util
from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///app.db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)


def load_us_module(filename, app, session):
    spec = importlib.util.spec_from_file_location(
        filename,
        os.path.join(os.getcwd(), filename)
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    if hasattr(module, "register"):
        module.register(app, session)
    else:
        print(f"⚠️  {filename} skipped (no register function)")


def create_app():
    app = Flask(__name__)
    session = SessionLocal()

    # Load all US-XX.py files
    for file in os.listdir():
        if file.startswith("US-") and file.endswith(".py"):
            load_us_module(file, app, session)

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
