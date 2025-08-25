from flask import Flask, request, jsonify
from flask_swagger_ui import get_swaggerui_blueprint
from dotenv import load_dotenv
import os
load_dotenv()

app = Flask(__name__)

# Register blueprints
from routes.audio import audio_bp

# Swagger setup
SWAGGER_URL = os.getenv('SWAGGER_URL', '/docs')
API_URL = os.getenv('API_URL', '/static/swagger.json')
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={'app_name': os.getenv('APP_NAME')}
)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)
app.register_blueprint(audio_bp)



@app.route("/")
def home():
    return {"message": "AI Speaking Backend is running!"}

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_input = data.get("message", "")
    
    # Tạm thời chưa có AI, chỉ echo lại
    return jsonify({"response": f"You said: {user_input}"})

if __name__ == "__main__":
    app.run(debug=True, port=5000)
