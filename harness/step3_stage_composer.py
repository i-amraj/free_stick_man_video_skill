"""
step3_stage_composer.py
Procedural Set & Character Staging:
- 100% SVG Procedural sets (Medieval Alley, Timber Shop, Detective Office)
- Forward Kinematics Stickman Rig instantiation (rig.js)
- Pure SVG Props injection (props.js)
- Multiplane 2.5D Parallax hierarchy
"""

def generate_procedural_background_svg(theme: str = "medieval_alley") -> str:
    """Returns pure SVG markup for rich procedural background."""
    if theme == "medieval_alley":
        return """
        <!-- Distant Night Sky & Moon -->
        <rect width="1080" height="1920" fill="#0A0D14" />
        <radialGradient id="moonGlow" cx="50%" cy="50%" r="50%">
            <stop offset="0%" stop-color="#E2E8F0" stop-opacity="0.9" />
            <stop offset="40%" stop-color="#94A3B8" stop-opacity="0.3" />
            <stop offset="100%" stop-color="#0A0D14" stop-opacity="0" />
        </radialGradient>
        <circle cx="820" cy="380" r="160" fill="url(#moonGlow)" />
        <circle cx="820" cy="380" r="70" fill="#F8FAFC" />
        
        <!-- Distant Gothic Rooftops -->
        <path d="M 0 950 L 180 820 L 360 960 L 520 780 L 720 920 L 880 740 L 1080 900 L 1080 1920 L 0 1920 Z" fill="#111827" />
        
        <!-- Midground Timber Buildings & Stone Walls -->
        <g id="bg-buildings">
            <rect x="0" y="880" width="380" height="1040" fill="#1E293B" stroke="#0F172A" stroke-width="4" />
            <rect x="700" y="850" width="380" height="1070" fill="#1E293B" stroke="#0F172A" stroke-width="4" />
            
            <!-- Stone Cobblestone Pattern -->
            <pattern id="cobble" width="80" height="40" patternUnits="userSpaceOnUse">
                <rect width="76" height="36" rx="6" fill="#161F30" stroke="#0B0F19" stroke-width="2" />
            </pattern>
            <rect x="0" y="1420" width="1080" height="500" fill="url(#cobble)" />
            <rect x="0" y="1420" width="1080" height="500" fill="black" opacity="0.25" />
            
            <!-- Glowing Streetlamp -->
            <g id="streetlamp" transform="translate(180, 1020)">
                <rect x="-8" y="0" width="16" height="480" fill="#0F172A" rx="4" />
                <path d="M -25 -20 L 25 -20 L 18 -60 L -18 -60 Z" fill="#334155" />
                <circle cx="0" cy="-40" r="16" fill="#FBBF24" />
                <radialGradient id="lampGlow" cx="50%" cy="50%" r="50%">
                    <stop offset="0%" stop-color="#F59E0B" stop-opacity="0.55" />
                    <stop offset="60%" stop-color="#F59E0B" stop-opacity="0.1" />
                    <stop offset="100%" stop-color="#F59E0B" stop-opacity="0" />
                </radialGradient>
                <circle cx="0" cy="-40" r="140" fill="url(#lampGlow)" />
            </g>
        </g>
        """
    else:
        # Default Detective Office
        return """
        <rect width="1080" height="1920" fill="#0F172A" />
        <!-- Wood wall paneling -->
        <rect x="60" y="200" width="960" height="1300" fill="#1E293B" stroke="#334155" stroke-width="8" rx="8" />
        <rect x="0" y="1460" width="1080" height="460" fill="#111827" />
        """

def get_character_setup_js(characters: list) -> str:
    """Generates JS initialization code for characters using rig.js."""
    lines = []
    for c in characters:
        var_name = c["id"]
        head_shape = c.get("head_shape", "round")
        beard = c.get("beard", "none")
        jacket = c.get("jacket", "none")
        skin = c.get("skin", "#F3C59A")
        shirt = c.get("shirt", "#FFFFFF")
        pants = c.get("pants", "#1F2937")
        shoes = c.get("shoes", "#111827")
        hat = c.get("hat", "none")
        scale = c.get("scale", 2.2)
        x = c.get("x", 540)
        y = c.get("y", 1460)
        
        lines.append(f"""
        const {var_name} = new StickmanRig('{var_name}-container', {{
            scale: {scale},
            headShape: '{head_shape}',
            beard: '{beard}',
            jacket: '{jacket}',
            skinColor: '{skin}',
            shirtColor: '{shirt}',
            pantsColor: '{pants}',
            shoeColor: '{shoes}',
            hat: '{hat}'
        }});
        {var_name}.setPosition({x}, {y});
        """)
    return "\n".join(lines)

