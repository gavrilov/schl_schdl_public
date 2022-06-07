from app import create_app


app = create_app()
"""
that file we use for run local server for development
PyCharm configuration:
    Additional options: --host=0.0.0.0
    FLASK_ENV development
    FLASK_DEBUG True
"""

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)