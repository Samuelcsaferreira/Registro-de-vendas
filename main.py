from flask import Flask
from app.routes.vendas_route import vendas_bp


app = Flask(__name__)

# Chamada do Blueprint de registro de vendas
app.register_blueprint(vendas_bp)


if __name__ == "__main__":
    app.run(debug=True)
