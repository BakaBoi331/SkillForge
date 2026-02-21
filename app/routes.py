from flask import Blueprint, request, jsonify
from .models import db, Skill, Session

api = Blueprint('api', __name__)

@api.route('/skills', methods=['POST'])
def create_skill():
    data = request.get_json()
    
    # 1. Interface Safety: Validate input early
    if not data or 'name' not in data:
        return jsonify({"error": "Skill 'name' is required"}), 400
        
    skill_name = data['name'].strip()
    if not skill_name:
        return jsonify({"error": "Skill 'name' cannot be empty"}), 400

    # 2. Prevent Invalid States: Check for duplicates
    existing_skill = Skill.query.filter_by(name=skill_name).first()
    if existing_skill:
        return jsonify({"error": f"Skill '{skill_name}' already exists"}), 409

    new_skill = Skill(name=skill_name)
    db.session.add(new_skill)
    db.session.commit()
    
    return jsonify({"id": new_skill.id, "name": new_skill.name, "current_level": new_skill.current_level}), 201


@api.route('/sessions', methods=['POST'])
def log_session():
    data = request.get_json()
    
    # 1. Strict Validation
    if not data or 'skill_id' not in data or 'duration_minutes' not in data:
        return jsonify({"error": "Both 'skill_id' and 'duration_minutes' are required"}), 400
        
    try:
        duration = int(data['duration_minutes'])
        if duration <= 0 or duration > 1440: # Max 24 hours in a single log
            return jsonify({"error": "Duration must be between 1 and 1440 minutes"}), 422
    except ValueError:
        return jsonify({"error": "Duration must be a valid integer"}), 422

    # 2. Verify Resource Exists
    skill = db.session.get(Skill, data['skill_id'])
    if not skill:
        return jsonify({"error": "Skill not found"}), 404

    # 3. Core Business Logic (Leveling Up)
    new_session = Session(skill_id=skill.id, duration_minutes=duration)
    db.session.add(new_session)
    
    # RPG Math: 1 minute = 1 XP. 100 XP = 1 Level.
    skill.total_xp += duration
    skill.current_level = 1 + (skill.total_xp // 100)
    
    db.session.commit()
    
    return jsonify({
        "message": "Session logged successfully",
        "new_total_xp": skill.total_xp,
        "new_level": skill.current_level
    }), 201