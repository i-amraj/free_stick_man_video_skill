"""
Standalone skeleton pose screenshot capture — no external JS deps.
Directly renders all bones using SVG coordinates from each pose definition.
"""
from playwright.sync_api import sync_playwright
import os, shutil, time

out_dir  = 'projects/mystery_333am/output/previews'
artifact = 'C:/Users/iamra/.gemini/antigravity/brain/c9b9d424-5a3c-4adf-aabc-2078a51c8ad6'

BONE_COLOR = '#f8fafc'
EYE_COLOR  = '#38bdf8'
SW = 7
FILL = '#090e1a'

def line_svg(x1,y1,x2,y2,sw=SW,color=BONE_COLOR,extra=''):
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{sw}" stroke-linecap="round" {extra}/>'

def circle_svg(cx,cy,r,fill,stroke=BONE_COLOR,sw=2,extra=''):
    return f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" {extra}/>'

def path_svg(d,sw=SW,color=BONE_COLOR,fill='none',extra=''):
    return f'<path d="{d}" stroke="{color}" stroke-width="{sw}" fill="{fill}" stroke-linecap="round" stroke-linejoin="round" {extra}/>'

POSES = {
  'idle': dict(
    sp_l=(0,60,0,10), sp_m=(0,10,0,-50), sp_u=(0,-50,0,-115), neck=(0,-115,0,-128),
    sh_l=(0,-100,-28,-105), sh_r=(0,-100,28,-105),
    ua_l=(-28,-105,-60,-60), fa_l=(-60,-60,-85,-15),
    ua_r=(28,-105,60,-60),   fa_r=(60,-60,85,-15),
    hi_l=(0,60,-18,72), th_l=(-18,72,-40,160), sh_l2=(-40,160,-48,255),
    hi_r=(0,60,18,72),  th_r=(18,72,40,160),   sh_r2=(40,160,48,255),
    fo_l='M -48 255 L -48 265 L -72 265', fo_r='M 48 255 L 48 265 L 72 265',
    mouth='M -10 -150 Q 0 -144 10 -150',
    eb_l='M -20 -178 L -6 -180', eb_r='M 6 -180 L 20 -178',
  ),
  'phone_call': dict(
    sp_l=(0,60,0,10), sp_m=(0,10,0,-50), sp_u=(0,-50,0,-115), neck=(0,-115,0,-128),
    sh_l=(0,-100,-28,-105), sh_r=(0,-100,28,-105),
    ua_l=(-28,-105,-50,-55), fa_l=(-50,-55,-55,-5),
    ua_r=(28,-105,55,-125),  fa_r=(55,-125,68,-155),
    hi_l=(0,60,-18,72), th_l=(-18,72,-40,160), sh_l2=(-40,160,-48,255),
    hi_r=(0,60,18,72),  th_r=(18,72,40,160),   sh_r2=(40,160,48,255),
    fo_l='M -48 255 L -48 265 L -72 265', fo_r='M 48 255 L 48 265 L 72 265',
    mouth='M -8 -150 L 8 -150',
    eb_l='M -20 -182 L -6 -184', eb_r='M 6 -184 L 20 -182',
  ),
  'shocked': dict(
    sp_l=(0,60,0,10), sp_m=(0,10,0,-50), sp_u=(0,-50,0,-115), neck=(0,-115,0,-128),
    sh_l=(0,-100,-28,-105), sh_r=(0,-100,28,-105),
    ua_l=(-28,-105,-60,-140), fa_l=(-60,-140,-40,-190),
    ua_r=(28,-105,60,-140),   fa_r=(60,-140,40,-190),
    hi_l=(0,60,-18,72), th_l=(-18,72,-60,155), sh_l2=(-60,155,-80,250),
    hi_r=(0,60,18,72),  th_r=(18,72,60,155),   sh_r2=(60,155,80,250),
    fo_l='M -80 250 L -80 262 L -105 262', fo_r='M 80 250 L 80 262 L 105 262',
    mouth='M -8 -148 A 7 10 0 1 0 8 -148 A 7 10 0 1 0 -8 -148',
    eb_l='M -20 -182 L -6 -187', eb_r='M 6 -187 L 20 -182',
  ),
  'thinking': dict(
    sp_l=(0,60,0,10), sp_m=(0,10,0,-50), sp_u=(0,-50,0,-115), neck=(0,-115,0,-128),
    sh_l=(0,-100,-28,-105), sh_r=(0,-100,28,-105),
    ua_l=(-28,-105,-45,-55), fa_l=(-45,-55,-20,-50),
    ua_r=(28,-105,50,-65),   fa_r=(50,-65,25,-145),
    hi_l=(0,60,-18,72), th_l=(-18,72,-40,160), sh_l2=(-40,160,-48,255),
    hi_r=(0,60,18,72),  th_r=(18,72,40,160),   sh_r2=(40,160,48,255),
    fo_l='M -48 255 L -48 265 L -72 265', fo_r='M 48 255 L 48 265 L 72 265',
    mouth='M -8 -150 L 8 -152',
    eb_l='M -20 -178 L -6 -180', eb_r='M 6 -183 L 20 -179',
  ),
  'crouching': dict(
    sp_l=(0,60,0,10), sp_m=(0,10,0,-50), sp_u=(0,-50,-15,-105), neck=(-15,-105,-20,-120),
    sh_l=(0,-100,-28,-105), sh_r=(0,-100,28,-105),
    ua_l=(-28,-100,-58,-55), fa_l=(-58,-55,-78,-10),
    ua_r=(28,-100,58,-55),   fa_r=(58,-55,78,-10),
    hi_l=(0,60,-18,72), th_l=(-18,72,-55,130), sh_l2=(-55,130,-30,215),
    hi_r=(0,60,18,72),  th_r=(18,72,55,130),   sh_r2=(55,130,30,215),
    fo_l='M -30 215 L -28 228 L -55 228', fo_r='M 30 215 L 28 228 L 55 228',
    mouth='M -10 -150 Q 0 -145 10 -150',
    eb_l='M -20 -178 L -6 -180', eb_r='M 6 -180 L 20 -178',
  ),
  'frozen_horror': dict(
    sp_l=(0,60,0,10), sp_m=(0,10,0,-50), sp_u=(0,-50,0,-115), neck=(0,-115,0,-128),
    sh_l=(0,-100,-28,-105), sh_r=(0,-100,28,-105),
    ua_l=(-28,-105,-55,-65), fa_l=(-55,-65,-72,-20),
    ua_r=(28,-105,55,-65),   fa_r=(55,-65,72,-20),
    hi_l=(0,60,-18,72), th_l=(-18,72,-20,160), sh_l2=(-20,160,-22,255),
    hi_r=(0,60,18,72),  th_r=(18,72,20,160),   sh_r2=(20,160,22,255),
    fo_l='M -22 255 L -22 265 L -46 265', fo_r='M 22 255 L 22 265 L 46 265',
    mouth='M -6 -150 A 5 7 0 1 0 6 -150 A 5 7 0 1 0 -6 -150',
    eb_l='M -20 -186 L -6 -188', eb_r='M 6 -188 L 20 -186',
  ),
}

POSE_LABELS = {
  'idle':'😶 Idle (Natural Stand)',
  'phone_call':'📞 Phone Call',
  'shocked':'😱 Shocked',
  'thinking':'🤔 Thinking',
  'crouching':'🦵 Crouching',
  'frozen_horror':'🥶 Frozen Horror',
}

GROUP_LABELS = {
  'idle':{'sp_l':'spine_lower','sp_m':'spine_mid','sp_u':'spine_upper','neck':'neck','sh_l':'shoulder_l','sh_r':'shoulder_r','ua_l':'upperarm_l','fa_l':'forearm_l','ua_r':'upperarm_r','fa_r':'forearm_r','hi_l':'hip_l','th_l':'thigh_l','sh_l2':'shin_l','hi_r':'hip_r','th_r':'thigh_r','sh_r2':'shin_r'},
}

def build_skeleton_svg(pose_key):
    p = POSES[pose_key]
    # Build all bone SVG elements
    bones_svg = f'''
    <!-- Spine chain -->
    {line_svg(*p['sp_l'], SW+1)}
    {line_svg(*p['sp_m'], SW)}
    {line_svg(*p['sp_u'], SW)}
    <!-- Neck -->
    {line_svg(*p['neck'], SW-1)}
    <!-- Shoulders -->
    {line_svg(*p['sh_l'], SW-1)}
    {line_svg(*p['sh_r'], SW-1)}
    <!-- Left Arm -->
    {line_svg(*p['ua_l'], SW)}
    {line_svg(*p['fa_l'], SW-1)}
    {circle_svg(-85, int(p['fa_l'][3]), 7, FILL, BONE_COLOR, SW-2)}
    <!-- Left Fingers -->
    {line_svg(int(p['fa_l'][2]), int(p['fa_l'][3]), int(p['fa_l'][2])-11, int(p['fa_l'][3])-9, 3)}
    {line_svg(int(p['fa_l'][2]), int(p['fa_l'][3]), int(p['fa_l'][2])-7,  int(p['fa_l'][3])+10, 3)}
    <!-- Right Arm -->
    {line_svg(*p['ua_r'], SW)}
    {line_svg(*p['fa_r'], SW-1)}
    {circle_svg(int(p['fa_r'][2]), int(p['fa_r'][3]), 7, FILL, BONE_COLOR, SW-2)}
    <!-- Right Fingers -->
    {line_svg(int(p['fa_r'][2]), int(p['fa_r'][3]), int(p['fa_r'][2])+11, int(p['fa_r'][3])-9, 3)}
    {line_svg(int(p['fa_r'][2]), int(p['fa_r'][3]), int(p['fa_r'][2])+7,  int(p['fa_r'][3])+10, 3)}
    <!-- Left Leg -->
    {line_svg(*p['hi_l'], SW)}
    {line_svg(*p['th_l'], SW+1)}
    {line_svg(*p['sh_l2'], SW)}
    {path_svg(p['fo_l'], SW)}
    <!-- Right Leg -->
    {line_svg(*p['hi_r'], SW)}
    {line_svg(*p['th_r'], SW+1)}
    {line_svg(*p['sh_r2'], SW)}
    {path_svg(p['fo_r'], SW)}
    <!-- Head -->
    {circle_svg(0, -165, 40, FILL, BONE_COLOR, SW)}
    <!-- Eyes -->
    {circle_svg(-13, -168, 5, EYE_COLOR, 'none', 0)}
    {circle_svg(13,  -168, 5, EYE_COLOR, 'none', 0)}
    <!-- Eyebrows -->
    {path_svg(p['eb_l'], 3, BONE_COLOR)}
    {path_svg(p['eb_r'], 3, BONE_COLOR)}
    <!-- Mouth -->
    {path_svg(p['mouth'], 4, BONE_COLOR)}
    <!-- Sweat bead (hidden on non-horror) -->
    {circle_svg(35, -180, 4.5, EYE_COLOR, 'none', 0, 'opacity="' + ('1' if pose_key=='frozen_horror' else '0') + '"')}
    '''
    return bones_svg

HTML_TEMPLATE = '''<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>
* {{ box-sizing:border-box; margin:0; padding:0; }}
body {{ background:#020617; display:flex; align-items:center; justify-content:center;
        height:100vh; font-family:monospace; }}
.frame {{
  width:400px; height:700px;
  background:radial-gradient(circle at 50% 55%, #060f1e, #020617);
  border:1px solid rgba(56,189,248,0.2);
  border-radius:16px;
  display:flex; flex-direction:column; align-items:center; justify-content:center;
  gap:20px; padding:30px;
}}
.label {{
  color:#38bdf8; font-size:15px; font-weight:700;
  letter-spacing:1.5px; text-transform:uppercase;
  background:rgba(15,23,42,0.9);
  border:1px solid rgba(56,189,248,0.3);
  border-radius:20px; padding:8px 20px;
}}
svg {{ overflow:visible; }}
</style>
</head>
<body>
<div class="frame">
  <div class="label">{label}</div>
  <svg width="300" height="580" viewBox="-150 -300 300 600">
    {bones}
  </svg>
</div>
</body>
</html>'''

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={'width': 500, 'height': 760})

    for pose_key in POSES:
        bones = build_skeleton_svg(pose_key)
        html  = HTML_TEMPLATE.format(label=POSE_LABELS[pose_key], bones=bones)
        page.set_content(html)
        time.sleep(0.3)
        fname = f'{out_dir}/skeleton_{pose_key}.jpg'
        page.screenshot(path=fname, type='jpeg', quality=92)
        shutil.copy2(fname, f'{artifact}/skeleton_{pose_key}.jpg')
        print(f'[OK] {pose_key}')

    browser.close()
print('All 6 skeleton poses captured!')
