from printcalc import create_app
from printcalc.config import HOST, PORT

# Create and configure the application
app = create_app()

if __name__ == "__main__":
    # Run the application using Waitress WSGI server
    print(f"Starting server on {HOST}:{PORT}")
    app.run(host=HOST, port=PORT)
