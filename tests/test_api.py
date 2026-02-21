def test_create_skill(client):
    """Test that we can create a skill successfully."""
    response = client.post('/api/skills', json={"name": "React Hooks"})
    assert response.status_code == 201
    assert response.get_json()["name"] == "React Hooks"

def test_prevent_duplicate_skill(client):
    """Test that the API rejects duplicate skill names."""
    client.post('/api/skills', json={"name": "Docker"})
    response = client.post('/api/skills', json={"name": "Docker"})
    
    assert response.status_code == 409
    assert "already exists" in response.get_json()["error"]

def test_log_session_level_up_math(client):
    """Test the RPG math: 150 mins should equal 150 XP and Level 2."""
    # 1. Forge a skill
    skill_res = client.post('/api/skills', json={"name": "Testing"})
    skill_id = skill_res.get_json()["id"]

    # 2. Log a 150 min session
    response = client.post('/api/sessions', json={
        "skill_id": skill_id,
        "duration_minutes": 150
    })
    
    assert response.status_code == 201
    data = response.get_json()
    
    # 3. Verify the math is perfectly calculated
    assert data["new_total_xp"] == 150
    assert data["new_level"] == 2

def test_reject_negative_duration(client):
    """Test that the API guards against impossible data (negative time)."""
    skill_res = client.post('/api/skills', json={"name": "Hacking"})
    skill_id = skill_res.get_json()["id"]

    response = client.post('/api/sessions', json={
        "skill_id": skill_id,
        "duration_minutes": -50
    })
    
    assert response.status_code == 422
    assert "Duration must be between" in response.get_json()["error"]