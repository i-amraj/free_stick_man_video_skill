"""
step1_script_breakdown.py
Deconstructs raw script text into 2.0s-2.8s narrative beats with:
- Speaker & Dialogue extraction
- Character emotion & action tagging
- Camera movement choreography ("Camera Kabhi Rukta Nahi")
- Scene environment & prop allocation
"""

import json
import re
from typing import List, Dict, Any

def breakdown_script(script_text: str, target_duration: float = None) -> List[Dict[str, Any]]:
    # Split text into sentences
    sentences = [s.strip() for s in re.split(r'[.!?]+', script_text) if s.strip()]
    if not sentences:
        sentences = ["The mystery begins under the flickering streetlights.", "A shadowy figure makes their move."]
    
    beats = []
    current_time = 0.0
    
    camera_moves = [
        "drift_right_push_in",
        "creeping_zoom_hold",
        "whip_pan_reveal",
        "punch_in_shock",
        "slow_pull_back_climax",
        "drift_left_subtle"
    ]
    
    for i, sent in enumerate(sentences):
        # Estimate duration: ~3 words per second + 0.5s pause
        words = sent.split()
        dur = max(2.2, min(3.2, len(words) * 0.38 + 0.4))
        
        # Check speaker & dialogue tags
        speaker = "narrator"
        dialogue = sent
        is_speech = False
        
        # Detect character quotes or dialogue prefixes
        if ":" in sent:
            parts = sent.split(":", 1)
            speaker = parts[0].strip().lower()
            dialogue = parts[1].strip()
            is_speech = True
        elif '"' in sent or "'" in sent:
            is_speech = True
            speaker = "hero"
        
        # Tag props based on words
        lower_sent = sent.lower()
        props = []
        if any(w in lower_sent for w in ["chest", "treasure", "box", "gold"]):
            props.append("treasure_chest")
        if any(w in lower_sent for w in ["coin", "coins", "money"]):
            props.append("gold_coin")
        if any(w in lower_sent for w in ["shoe", "stinky", "smell", "boot"]):
            props.append("stinky_shoe")
        if any(w in lower_sent for w in ["crate", "wood", "firewood"]):
            props.append("crate")
        if any(w in lower_sent for w in ["light", "lantern", "lamp"]):
            props.append("lantern")
        if any(w in lower_sent for w in ["magnifier", "glass", "lens", "investigate"]):
            props.append("magnifier")
        
        # Determine actor action
        if any(w in lower_sent for w in ["walk", "approach", "enter"]):
            action = "walk"
        elif any(w in lower_sent for w in ["run", "sprint", "flee", "dash"]):
            action = "run"
        elif any(w in lower_sent for w in ["shock", "gasp", "wait", "what", "surprised"]):
            action = "shock_jump"
        elif any(w in lower_sent for w in ["dance", "celebrate", "victory"]):
            action = "disco_dance"
        elif any(w in lower_sent for w in ["point", "aha", "there"]):
            action = "point"
        elif any(w in lower_sent for w in ["facepalm", "sigh", "smell", "dirty"]):
            action = "facepalm"
        else:
            action = "idle_sway"
            
        cam_move = camera_moves[i % len(camera_moves)]
        if action == "shock_jump":
            cam_move = "punch_in_shock"
            
        beat = {
            "id": f"beat_{i+1:02d}",
            "time_start": round(current_time, 2),
            "time_end": round(current_time + dur, 2),
            "duration": round(dur, 2),
            "sentence": sent,
            "speaker": speaker,
            "dialogue": dialogue,
            "is_direct_speech": is_speech,
            "action": action,
            "camera_move": cam_move,
            "props": props
        }
        beats.append(beat)
        current_time += dur
        
    return beats

if __name__ == "__main__":
    sample = "Midnight in the narrow cobblestone alley. Detective Gary inspects the ground. Aha! The thief dropped a gold coin! Wait! It is just a dirty old shoe?!"
    res = breakdown_script(sample)
    print(json.dumps(res, indent=2))

