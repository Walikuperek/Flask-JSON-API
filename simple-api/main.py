from flask import Flask

from app.routes import bp as blog_posts_bp


def create_app():
    app = Flask(__name__)
    app.register_blueprint(blog_posts_bp)
    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
