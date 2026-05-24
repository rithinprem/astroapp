import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'super-secret-astrology-key'
    JSON_SORT_KEYS = False  # Keeps your output JSON structured, not alphabetical