import { useState, useEffect } from 'react';
import { z } from 'zod';
import { Sword, PlusCircle, ShieldAlert, Trash2 } from 'lucide-react';

//Adding interface safety
interface Skill {
  id: number;
  name: string;
  current_level: number;
  total_xp: number;
}

//Zod validation
const sessionSchema = z.object({
  skill_id: z.number().min(1, "Please select a skill"),
  duration_minutes: z.number().min(1, "Must be at least 1 minute").max(1440, "Cannot exceed 24 hours"),
});

export default function App() {
  const [skills, setSkills] = useState<Skill[]>([]);
  const [newSkillName, setNewSkillName] = useState('');
  const [selectedSkill, setSelectedSkill] = useState<number>(0);
  const [duration, setDuration] = useState<number | ''>('');
  const [formError, setFormError] = useState<string>('');

  const API_BASE = 'http://127.0.0.1:5000/api';

  //Fetching data - skills from backend
  const fetchSkills = async () => {
    try {
      const response = await fetch(`${API_BASE}/skills`);
      const data = await response.json();
      setSkills(data);
    } catch (error) {
      console.error("Failed to fetch skills:", error);
    }
  };

  useEffect(() => {
    fetchSkills();
  }, []);

  const handleCreateSkill = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newSkillName.trim()) return;

    const res = await fetch(`${API_BASE}/skills`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name: newSkillName }),
    });

    if (res.ok) {
      setNewSkillName('');
      fetchSkills();
    }
  };

  const handleLogSession = async (e: React.FormEvent) => {
    e.preventDefault();
    setFormError('');

    // Zod Validation Check
    const validation = sessionSchema.safeParse({
      skill_id: selectedSkill,
      duration_minutes: Number(duration),
    });

    if (!validation.success) {
      setFormError(validation.error.errors[0].message);
      return;
    }

    const res = await fetch(`${API_BASE}/sessions`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(validation.data),
    });

    if (res.ok) {
      setDuration('');
      setSelectedSkill(0);
      fetchSkills(); // refresh the UI with new xp/levels
    } else {
      const errData = await res.json();
      setFormError(errData.error || "Failed to log session");
    }
  };

  const handleDeleteSkill = async (skillId: number) => {
    if (!confirm("Are you sure? This will delete the skill and all its history forever.")) {
      return;
    }

    const res = await fetch(`${API_BASE}/skills/${skillId}`, {
      method: 'DELETE',
    });

    if (res.ok) {
      // If successful, refresh the list to remove the deleted skill from the UI
      fetchSkills();
      // If the deleted skill was selected in the dropdown, reset the selection
      if (selectedSkill === skillId) {
        setSelectedSkill(0);
      }
    } else {
      console.error("Failed to delete skill");
    }
  };

  return (
    <div style={{ maxWidth: '800px', margin: '0 auto', fontFamily: 'system-ui, sans-serif', padding: '2rem' }}>
      <header style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '2rem' }}>
        <Sword size={32} color="#2563eb" />
        <h1 style={{ margin: 0 }}>SkillForge RPG</h1>
      </header>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '2rem' }}>
        {/*left column: Create & Log*/}
        <div>
          <section style={{ padding: '1.5rem', border: '1px solid #e5e7eb', borderRadius: '8px', marginBottom: '1rem' }}>
            <h3>Forge a New Skill</h3>
            <form onSubmit={handleCreateSkill} style={{ display: 'flex', gap: '10px' }}>
              <input
                value={newSkillName}
                onChange={(e) => setNewSkillName(e.target.value)}
                placeholder="e.g., Python Architecture"
                style={{ flex: 1, padding: '0.5rem' }}
              />
              <button type="submit" style={{ padding: '0.5rem 1rem', cursor: 'pointer' }}>Create</button>
            </form>
          </section>

          <section style={{ padding: '1.5rem', border: '1px solid #e5e7eb', borderRadius: '8px' }}>
            <h3>Log Training Session</h3>
            <form onSubmit={handleLogSession} style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
              <select
                value={selectedSkill}
                onChange={(e) => setSelectedSkill(Number(e.target.value))}
                style={{ padding: '0.5rem' }}
              >
                <option value={0}>-- Select a Skill --</option>
                {skills.map(s => (
                  <option key={s.id} value={s.id}>{s.name} (Lvl {s.current_level})</option>
                ))}
              </select>

              <input
                type="number"
                value={duration}
                onChange={(e) => setDuration(e.target.value ? Number(e.target.value) : '')}
                placeholder="Duration (minutes)"
                style={{ padding: '0.5rem' }}
              />

              {formError && (
                <div style={{ color: '#dc2626', display: 'flex', alignItems: 'center', gap: '5px', fontSize: '0.9rem' }}>
                  <ShieldAlert size={16} /> {formError}
                </div>
              )}

              <button type="submit" style={{ padding: '0.5rem', display: 'flex', justifyContent: 'center', gap: '5px', cursor: 'pointer' }}>
                <PlusCircle size={20} /> Log XP
              </button>
            </form>
          </section>
        </div>

        {/*right column: Character Stats*/}
        <div>
          <h2>Character Stats</h2>
          {skills.length === 0 ? (
            <p style={{ color: '#6b7280' }}>No skills forged yet. Start your journey.</p>
          ) : (
            <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
              {skills.map(skill => (
                <div key={skill.id} style={{ padding: '1rem', backgroundColor: '#f3f4f6', borderRadius: '8px' }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.5rem' }}>
                    <strong>{skill.name}</strong>
                    <span style={{ fontWeight: 'bold', color: '#2563eb' }}>Level {skill.current_level}</span>
                  </div>
                  <button
                    onClick={() => handleDeleteSkill(skill.id)}
                    style={{ border: 'none', background: 'none', cursor: 'pointer', color: '#dc2626' }}
                    title="Delete Skill"
                  >
                    <Trash2 size={18} />
                  </button>
                  <div style={{ fontSize: '0.85rem', color: '#4b5563' }}><span>Total XP: {skill.total_xp}</span></div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}