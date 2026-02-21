# Add this at the top of app/routes.py
import math

def calculate_level(total_xp):
    """Calculates level based on formula: XP = 100 * (Level - 1)^2"""
    if total_xp < 100:
        return 1
    # Inverse formula: Level = sqrt(XP / 100) + 1
    return math.floor(math.sqrt(total_xp / 100)) + 1

def xp_for_next_level(current_level):
    """Calculates total XP needed for the next level."""
    next_lvl = current_level + 1
    return 100 * ((next_lvl - 1) ** 2)

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
    existing_skill = Skill.query.filter(Skill.name.ilike(skill_name)).first()
    if existing_skill:
        return jsonify({"error": f"Skill '{skill_name}' already exists"}), 409

    new_skill = Skill(name=skill_name)
    db.session.add(new_skill)
    db.session.commit()
    
    return jsonify({"id": new_skill.id, "name": new_skill.name, "current_level": new_skill.current_level}), 201

@api.route('/skills', methods=['GET'])
def get_skills():
    skills = Skill.query.all()
    
    #Formatting for frontend
    skills_data = []
    for skill in skills:
        req_xp = xp_for_next_level(skill.current_level)
        skills_data.append({
            "id": skill.id, 
            "name": skill.name, 
            "current_level": skill.current_level, 
            "total_xp": skill.total_xp,
            # Calculate how much XP is needed for the next level
            "xp_to_next_level": req_xp - skill.total_xp,
            # Calculate progress into the current level for a future progress bar
            "progress_xp": skill.total_xp - (100 * ((skill.current_level - 1)**2))
        })

    return jsonify(skills_data), 200

@api.route('/skills/<int:skill_id>', methods=['DELETE'])
def delete_skill(skill_id):
    # 1. Find the skill by its primary key (ID)
    skill = Skill.query.get(skill_id)
    
    # 2. Guard Clause: What if the ID doesn't exist?
    if not skill:
        return jsonify({"error": "Skill not found"}), 404

    # 3. Delete it. The 'cascade' in models.py handles the sessions automatically.
    db.session.delete(skill)
    db.session.commit()
    
    return jsonify({"message": f"Skill '{skill.name}' and all its sessions have been deleted"}), 200

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
    
    # Add the new XP
    skill.total_xp += duration
    
    # Recalculate level using the new progressive formula
    skill.current_level = calculate_level(skill.total_xp)
    
    db.session.commit()
    
    return jsonify({
        "message": "Session logged successfully",
        "new_total_xp": skill.total_xp,
        "new_level": skill.current_level
    }), 201