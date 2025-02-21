

from flask import Blueprint, jsonify,current_app
from api.models.program import Program
from api.db.database import init_db
from api.extentions import cache

programs_bp = Blueprint('programs', __name__)
@programs_bp.route('/programs/<program_id>', methods=['GET'])
@cache.cached(timeout=50)
async def get_program(program_id: str):
    await init_db()
    try:
        program_id_int = int(program_id) 
    except ValueError:
        return jsonify({"error": "program_id must be a number"}), 400

    try:
        program = await Program.find_one(
            {"program_id": program_id_int},
            fetch_links=True, 
        ) 
        if not program:
            return jsonify({"error": "Program not found"}), 404
        program_dict = program.dict()
        current_app.logger.info(program_dict)
        program_dict["id"] = str(program_dict["id"]) 
        return jsonify(program_dict)
    except Exception as e:
        current_app.logger.error(f"Error: {str(e)}", exc_info=True)
        return jsonify({"error": "Server error"}), 500