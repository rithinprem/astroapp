# run.py
from app import create_app

# Execute the factory function to build the server instance
app = create_app()

if __name__ == "__main__":
    app.run()