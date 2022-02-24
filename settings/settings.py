import os, secrets

class Base:
    SECRET_KEY = secrets.token_urlsafe(16)

class DEV(Base):
    FLASK_APP= os.environ.get("FLASK_APP")
    FLASK_ENV= os.environ.get("FLASK_ENV")