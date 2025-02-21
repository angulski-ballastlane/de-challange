from flask import Flask
import asyncio


from api.routes.programs import programs_bp
from api.routes.health import health_bp
from api.db.database import init_db
from api.extentions import cache

app = Flask(__name__)

cache.init_app(app)

app.register_blueprint(programs_bp)
app.register_blueprint(health_bp)
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(init_db())
    cache.run(debug=True, host="0.0.0.0", use_reloader=False)
