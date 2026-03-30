from flask import Flask, redirect, url_for, session
from config import Config
from routes.auth import auth_bp
from routes.books import books_bp
from routes.admin import admin_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)          # loads ALL Config attrs at once
    app.secret_key = Config.SECRET_KEY      # kept explicit for clarity

    @app.before_request
    def make_session_permanent():
        session.permanent = True

    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(books_bp)
    app.register_blueprint(admin_bp)

    # Root redirect
    @app.route('/')
    def root():
        return redirect(url_for('auth.login'))

    # Handle corrupt/bad session cookies and bad requests
    @app.errorhandler(400)
    def bad_request(e):
        session.clear()
        from flask import flash
        flash('Your session expired or is invalid. Please log in again.', 'warning')
        return redirect(url_for('auth.login'))

    @app.errorhandler(500)
    def internal_error(e):
        session.clear()
        from flask import flash
        flash('An unexpected error occurred. Please try again.', 'danger')
        return redirect(url_for('auth.login'))

    return app

if __name__ == '__main__':
    app = create_app()
    print("\n🚀 Online Book Recommendation System is running!")
    print("📖 User Portal : http://127.0.0.1:5000/login")
    print("🔐 Admin Panel : http://127.0.0.1:5000/admin/login")
    print("   Admin Email : likhithanm2004@gmail.com")
    print("   Admin Pass  : 7019162414")
    print("\nPress CTRL+C to stop.\n")
    app.run(debug=True, host='0.0.0.0', port=5000)
