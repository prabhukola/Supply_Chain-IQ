from flask import Flask, render_template

def create_app():
    app = Flask(__name__, template_folder="templates")

    # Register API Blueprints
    from app.api.routes_dashboard import routes_dashboard
    from app.api.routes_demand import routes_demand
    from app.api.routes_simulation import routes_simulation
    from app.api.routes_optimization import routes_optimization

    app.register_blueprint(routes_dashboard)
    app.register_blueprint(routes_demand)
    app.register_blueprint(routes_simulation)
    app.register_blueprint(routes_optimization)

    @app.route("/")
    def index():
        return render_template("index.html")

    return app
