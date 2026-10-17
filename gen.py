#!/usr/bin/env python3
# Generates draw.io mxlibrary files:
# - smarthome.library.xml : IEC 60617 style (generic home automation)
# - knx.library.xml : ISO/IEC 14543-3 (KNX) style
import base64, zlib, urllib.parse, json, html

# ---------------- stencil DSL (100x100) ----------------
def M(x,y): return f'<move x="{x}" y="{y}"/>'
def L(x,y): return f'<line x="{x}" y="{y}"/>'
def Q(cx,cy,x,y): return f'<quad x1="{cx}" y1="{cy}" x="{x}" y="{y}"/>'
def RR(x,y,w,h,arc=8): return f'<roundrect x="{x}" y="{y}" w="{w}" h="{h}" arcsize="{arc}"/>'
def RECT(x,y,w,h): return f'<rect x="{x}" y="{y}" w="{w}" h="{h}"/>'
def ELL(x,y,w,h): return f'<ellipse x="{x}" y="{y}" w="{w}" h="{h}"/>'
def CIRC(cx,cy,r): return ELL(cx-r,cy-r,2*r,2*r)
def P(*ops): return '<path>'+''.join(ops)+'</path>'
STROKE='<stroke/>'; FILL='<fill/>'; FS='<fillstroke/>'
def SW(w): return f'<strokewidth width="{w}"/>'
CLOSE='<close/>'

def conns():
    pts = [('N',.5,0),('S',.5,1),('W',0,.5),('E',1,.5),
           ('NW',0,0),('NE',1,0),('SW',0,1),('SE',1,1)]
    s='<connections>'
    for n,x,y in pts: s+=f'<constraint name="{n}" perimeter="0" x="{x}" y="{y}"/>'
    s+='</connections>'
    return s

def shape_xml(name, bg, fg):
    s=f'<shape name="{html.escape(name)}" h="100" w="100" aspect="variable" strokewidth="inherit">'
    s+=conns()
    if bg: s+='<background>'+''.join(bg)+'</background>'
    s+='<foreground>'+''.join(fg)+'</foreground></shape>'
    return s

def b64deflate(text):
    co=zlib.compressobj(9,zlib.DEFLATED,-15)
    d=co.compress(urllib.parse.quote(text,safe='').encode('utf-8'))+co.flush()
    return base64.b64encode(d).decode('ascii')

# styles
ICON='fillColor=none;strokeColor=#4D4D4D;strokeWidth=1;'
BLOCK='fillColor=#f5f5f5;strokeColor=#4D4D4D;strokeWidth=1;'
BUS='fillColor=#4D4D4D;strokeColor=#4D4D4D;strokeWidth=1;'

def write_lib(filename, title_tags, entries):
    lib='<mxlibrary tags="'+title_tags+'">'+json.dumps(entries)+'</mxlibrary>'
    open(filename,'w',encoding='utf-8').write(lib)
    return len(entries), len(lib)

def cell_for(name, style, bgfg):
    bg,fg=bgfg
    sx=shape_xml(name,bg,fg)
    p=b64deflate(sx)
    cs=f'shape=stencil({p});verticalLabelPosition=bottom;verticalAlign=top;html=1;whiteSpace=wrap;{style}'
    m=('''<mxGraphModel><root><mxCell id="0"/><mxCell id="1" parent="0"/>'''
       f'''<mxCell id="2" value="" style="{cs}" vertex="1" parent="1">'''
       '''<mxGeometry width="80" height="80" as="geometry"/></mxCell></root></mxGraphModel>''')
    return b64deflate(m)

# ================= IEC 60617 set =================
IEC=[]
def iec_add(name,tags,style,bg,fg):
    IEC.append((name,tags,style,(bg,fg)))

# Sensing/Security (IEC)
iec_add('Presence Detector (PIR)','pir presence detection',ICON,[],[
    SW(4), P(M(20,70),Q(50,20,80,70),STROKE), P(M(14,70),L(86,70),STROKE),
    CIRC(50,58,7),STROKE, P(M(84,54),Q(94,44,84,34),STROKE), P(M(90,60),Q(100,44,90,28),STROKE),
])
iec_add('Door/Window Contact','contact reed magnetic binary',ICON,[],[
    SW(4), RECT(16,36,28,28),STROKE, RECT(56,40,24,20),STROKE,
    P(M(44,50),L(56,50),STROKE), CIRC(46,50,2),FS, CIRC(54,50,2),FS,
])
iec_add('Smoke Detector','smoke fire detector',ICON,[],[
    SW(4), CIRC(50,46,28),STROKE, CIRC(50,46,10),STROKE,
    P(M(50,18),L(50,8),STROKE), P(M(78,46),L(88,46),STROKE), P(M(22,46),L(12,46),STROKE), P(M(50,74),L(50,84),STROKE),
])
iec_add('Water Leak Detector','leak water flood',ICON,[],[
    SW(4), P(M(50,16),Q(76,52,50,78),Q(24,52,50,16),STROKE),
    P(M(24,88),Q(37,84,50,88),Q(63,92,76,88),STROKE),
])
iec_add('Temperature Sensor','temperature t sensor',ICON,[],[
    SW(4), CIRC(50,74,12),STROKE, P(M(50,20),L(50,74),STROKE),
    P(M(46,28),L(54,28),STROKE), P(M(46,42),L(54,42),STROKE), P(M(46,56),L(54,56),STROKE),
])
iec_add('Humidity Sensor','humidity rh sensor',ICON,[],[
    SW(4), P(M(50,14),Q(78,50,50,84),Q(22,50,50,14),STROKE),
    P(M(38,44),Q(46,38,54,44),Q(62,50,70,44),STROKE),
])
iec_add('Illuminance Sensor (Lux)','lux light illuminance',ICON,[],[
    SW(4), CIRC(50,50,14),STROKE,
    P(M(50,20),L(50,10),STROKE),P(M(50,90),L(50,80),STROKE),P(M(20,50),L(10,50),STROKE),P(M(90,50),L(80,50),STROKE),
    P(M(30,30),L(22,22),STROKE),P(M(70,30),L(78,22),STROKE),P(M(30,70),L(22,78),STROKE),P(M(70,70),L(78,78),STROKE),
])
iec_add('Gas/Air Quality Sensor','air co2 gas quality',ICON,[],[
    SW(4), CIRC(50,50,26),STROKE, CIRC(50,50,12),STROKE,
    P(M(50,24),L(50,14),STROKE),P(M(76,50),L(86,50),STROKE),P(M(24,50),L(14,50),STROKE),P(M(50,76),L(50,86),STROKE),
])
iec_add('Alarm/Siren','alarm siren sound',ICON,[],[
    SW(4), P(M(28,40),L(28,60),L(60,72),L(60,28),CLOSE,STROKE),
    P(M(68,42),Q(78,50,68,58),STROKE), P(M(74,36),Q(88,50,74,64),STROKE),
])
iec_add('Camera','camera video surveillance',ICON,[],[
    SW(4), RR(18,38,44,24,4),STROKE, CIRC(64,50,8),STROKE, P(M(28,62),L(28,74),L(42,74),STROKE),
])
iec_add('Lock','lock security',ICON,[],[
    SW(4), P(M(36,44),L(36,32),Q(50,16,64,32),L(64,44),STROKE), RR(28,44,44,36,4),STROKE, CIRC(50,60,5),STROKE,P(M(50,65),L(50,72),STROKE),
])
iec_add('Glass Break Detector','glass break vibration',ICON,[],[
    SW(4), RECT(22,22,56,56),STROKE, P(M(50,50),L(36,30),STROKE),P(M(50,50),L(64,28),STROKE),P(M(50,50),L(72,54),STROKE),P(M(50,50),L(60,72),STROKE),P(M(50,50),L(34,68),STROKE),
])
iec_add('Emergency Button (Panic)','panic emergency',ICON,[],[
    SW(4), CIRC(50,50,30),STROKE, CIRC(50,50,22),STROKE, P(M(50,32),L(50,56),STROKE), CIRC(50,64,3),FS,
])
iec_add('Keypad/Access Control','keypad access code',ICON,[],[
    SW(4), RR(24,18,52,64,5),STROKE, RECT(32,26,36,10),STROKE,
    *[CIRC(cx,cy,4)+STROKE for cy in (48,62,76) for cx in (36,50,64)],
])
iec_add('Generic Sensor','sensor input',ICON,[],[
    SW(4), CIRC(50,40,20),STROKE, P(M(50,60),L(50,80),STROKE), P(M(40,70),L(60,70),STROKE),
])
# Lighting
iec_add('Switch (General)','switch',ICON,[],[
    SW(4), P(M(24,30),L(76,70),STROKE), CIRC(24,30,4),STROKE, CIRC(76,70,4),STROKE,
])
iec_add('Dimmer','dimmer',ICON,[],[
    SW(4), P(M(20,34),L(80,66),STROKE), CIRC(20,34,4),STROKE, CIRC(80,66,4),STROKE, P(M(70,50),L(86,42),L(86,58),CLOSE,STROKE),
])
iec_add('Lamp/Light','lamp light',ICON,[],[
    SW(4), CIRC(50,44,20),STROKE, P(M(36,58),L(64,58),STROKE), P(M(40,64),L(60,64),STROKE), P(M(44,70),L(56,70),STROKE),
])
iec_add('RGB/Colour Light','rgb colour light',ICON,[],[
    SW(4), CIRC(50,44,20),STROKE, P(M(36,58),L(64,58),STROKE), P(M(40,64),L(60,64),STROKE),
    CIRC(38,38,3),STROKE, CIRC(62,38,3),STROKE, CIRC(50,30,3),STROKE,
])
iec_add('Blind/Shutter','blind shutter',ICON,[],[
    SW(4), RECT(22,18,56,64),STROKE, P(M(22,30),L(78,30),STROKE),P(M(22,42),L(78,42),STROKE),P(M(22,54),L(78,54),STROKE),P(M(22,66),L(78,66),STROKE),
])
iec_add('Curtain','curtain',ICON,[],[
    SW(4), P(M(14,24),L(86,24),STROKE), P(M(30,26),Q(20,56,32,82),L(48,82),Q(44,54,50,26),STROKE), P(M(70,26),Q(80,56,68,82),L(52,82),Q(56,54,50,26),STROKE),
])
iec_add('Thermostat','thermostat',ICON,[],[
    SW(4), CIRC(50,50,28),STROKE, CIRC(50,50,20),STROKE, P(M(50,50),L(64,38),STROKE), P(M(50,22),L(50,16),STROKE), P(M(22,50),L(16,50),STROKE), P(M(78,50),L(84,50),STROKE),
])
iec_add('Radiator/Valve','valve radiator',ICON,[],[
    SW(4), RR(20,46,40,28,3),STROKE, P(M(28,46),L(28,74),STROKE),P(M(40,46),L(40,74),STROKE),P(M(52,46),L(52,74),STROKE), CIRC(76,46,10),STROKE,P(M(76,36),L(76,20),STROKE),P(M(70,26),L(82,26),STROKE),
])
iec_add('Fan','fan ventilation',ICON,[],[
    SW(4), CIRC(50,50,8),STROKE,
    P(M(50,50),Q(22,22,48,20),Q(60,34,50,50),CLOSE,STROKE), P(M(50,50),Q(78,22,82,50),Q(64,60,50,50),CLOSE,STROKE),
    P(M(50,50),Q(22,78,48,80),Q(36,64,50,50),CLOSE,STROKE), P(M(50,50),Q(78,78,82,50),Q(60,38,50,50),CLOSE,STROKE),
])
iec_add('Heating Circuit','heating',ICON,[],[
    SW(4), P(M(12,42),L(88,42),STROKE),P(M(12,58),L(88,58),STROKE), CIRC(50,50,12),STROKE, P(M(46,44),L(56,50),L(46,56),CLOSE,STROKE),
])
iec_add('Socket/Outlet','outlet socket',ICON,[],[
    SW(4), RR(30,16,40,68,8),STROKE, CIRC(40,44,4),FS, CIRC(60,44,4),FS, P(M(50,60),L(50,68),STROKE), CIRC(50,70,3),STROKE,
])
iec_add('Relay/Contactor','relay contactor',ICON,[],[
    SW(4), RECT(20,30,60,40),STROKE, P(M(30,56),L(30,44),L(64,44),STROKE), CIRC(30,56,3),FS, CIRC(70,56,3),FS, P(M(70,56),L(58,46),STROKE),
])
# Infra
iec_add('Controller/Gateway','controller gateway',BLOCK,[RR(18,28,64,48,6)],[FS,SW(4), RECT(34,40,32,24),STROKE, P(M(18,44),L(34,44),STROKE),P(M(18,60),L(34,60),STROKE),P(M(66,44),L(82,44),STROKE),P(M(66,60),L(82,60),STROKE),
])
iec_add('Actuator','actuator output',BLOCK,[RR(18,32,64,40,6)],[FS,SW(4), CIRC(36,52,8),STROKE, P(M(44,52),L(70,52),STROKE), P(M(70,52),L(64,48),STROKE),P(M(70,52),L(64,56),STROKE),
])
iec_add('Bus Line','bus line',BUS,[],[SW(5), P(M(8,42),L(92,42),STROKE),P(M(8,58),L(92,58),STROKE), CIRC(26,36,4),FS,CIRC(50,36,4),FS,CIRC(74,36,4),FS,
])
iec_add('Power Supply','power supply psu',BLOCK,[RR(18,30,64,40,6)],[FS,SW(4), CIRC(44,50,14),STROKE, P(M(44,43),L(44,57),STROKE), P(M(58,44),L(70,44),STROKE),P(M(58,56),L(70,56),STROKE),
])
iec_add('Line Coupler','line coupler',BLOCK,[RR(22,38,56,24,5)],[FS,SW(4), P(M(8,42),L(22,42),STROKE),P(M(8,58),L(22,58),STROKE),P(M(78,42),L(92,42),STROKE),P(M(78,58),L(92,58),STROKE), P(M(50,38),L(50,30),STROKE),P(M(50,62),L(50,70),STROKE),
])
iec_add('I/O Module','io module',BLOCK,[RR(18,32,64,40,6)],[FS,SW(4), RECT(26,44,12,16),STROKE, RECT(46,44,8,16),STROKE, RECT(62,44,12,16),STROKE,
])
iec_add('User Interface/Panel','hmi panel touch',BLOCK,[RR(20,24,60,52,6)],[FS,SW(4), RECT(26,32,48,36),STROKE, CIRC(34,58,3),FS,P(M(44,58),L(68,58),STROKE),
])
iec_add('Network/Router','router network',BLOCK,[RR(18,32,64,40,6)],[FS,SW(4), P(M(32,46),L(68,46),STROKE),P(M(62,42),L(68,46),STROKE),P(M(62,50),L(68,46),STROKE), P(M(68,58),L(32,58),STROKE),P(M(38,54),L(32,58),STROKE),P(M(38,62),L(32,58),STROKE),
])
iec_add('Cloud/Remote','cloud remote',ICON,[],[SW(4), P(M(26,64),Q(10,64,12,52),Q(12,40,28,42),Q(32,26,52,28),Q(70,28,74,44),Q(90,46,88,56),Q(90,64,74,64),CLOSE,STROKE), P(M(36,80),L(50,72),L(50,80),STROKE),P(M(64,80),L(50,72),STROKE),
])
iec_add('Bus Terminator','terminator',BUS,[],[SW(4), P(M(8,50),L(36,50),STROKE), RECT(36,42,20,16),STROKE, P(M(44,46),L(52,46),STROKE), P(M(44,42),L(44,50),STROKE), P(M(56,50),L(92,50),STROKE),
])
iec_add('Generic Device','device',BLOCK,[RR(18,32,64,40,6)],[FS,SW(4),
])

# ================= KNX (ISO/IEC 14543-3) set =================
KNX=[]
def knx_add(name,tags,style,bg,fg):
    KNX.append((name,tags,style,(bg,fg)))

# KNX style: functional blocks, bus double line, arrows in/out
knx_add('KNX Bus (TP)','knx bus tp twisted pair',BUS,[],[
    SW(5), P(M(6,40),L(94,40),STROKE), P(M(6,60),L(94,60),STROKE),
    CIRC(24,34,4),FS,CIRC(50,34,4),FS,CIRC(76,34,4),FS,
])
knx_add('KNX Sensor (Binary Input)','knx sensor input binary',BLOCK,[RR(16,26,68,48,6)],[FS,SW(4),
    P(M(6,40),L(16,40),STROKE), P(M(6,60),L(16,60),STROKE),  # bus tap
    P(M(16,40),L(28,40),STROKE), P(M(28,40),L(24,36),STROKE),P(M(28,40),L(24,44),STROKE),  # input arrow
    RECT(40,38,24,24),STROKE, CIRC(46,50,4),STROKE,CIRC(58,50,4),STROKE,
])
knx_add('KNX Presence/Motion Sensor','knx pir motion presence',BLOCK,[RR(16,26,68,48,6)],[FS,SW(4),
    P(M(6,40),L(16,40),STROKE),P(M(6,60),L(16,60),STROKE),
    P(M(16,40),L(28,40),STROKE),P(M(28,40),L(24,36),STROKE),P(M(28,40),L(24,44),STROKE),
    P(M(42,56),Q(52,40,62,56),STROKE), P(M(38,56),L(66,56),STROKE), P(M(64,50),Q(72,42,64,34),STROKE),
])
knx_add('KNX Door/Window Contact','knx contact reed',BLOCK,[RR(16,26,68,48,6)],[FS,SW(4),
    P(M(6,40),L(16,40),STROKE),P(M(6,60),L(16,60),STROKE),
    P(M(16,40),L(28,40),STROKE),P(M(28,40),L(24,36),STROKE),P(M(28,40),L(24,44),STROKE),
    RECT(44,40,16,20),STROKE, RECT(60,42,12,16),STROKE, P(M(60,50),L(52,50),STROKE),
])
knx_add('KNX Temperature Sensor','knx temperature',BLOCK,[RR(16,26,68,48,6)],[FS,SW(4),
    P(M(6,40),L(16,40),STROKE),P(M(6,60),L(16,60),STROKE),
    P(M(16,40),L(28,40),STROKE),P(M(28,40),L(24,36),STROKE),P(M(28,40),L(24,44),STROKE),
    CIRC(58,64,8),STROKE, P(M(58,30),L(58,64),STROKE), P(M(54,36),L(62,36),STROKE),P(M(54,46),L(62,46),STROKE),P(M(54,56),L(62,56),STROKE),
])
knx_add('KNX Humidity Sensor','knx humidity rh',BLOCK,[RR(16,26,68,48,6)],[FS,SW(4),
    P(M(6,40),L(16,40),STROKE),P(M(6,60),L(16,60),STROKE),
    P(M(16,40),L(28,40),STROKE),P(M(28,40),L(24,36),STROKE),P(M(28,40),L(24,44),STROKE),
    P(M(50,32),Q(70,52,50,72),Q(30,52,50,32),STROKE), P(M(42,48),Q(48,44,54,48),Q(62,52,70,48),STROKE),
])
knx_add('KNX Lux Sensor','knx lux brightness',BLOCK,[RR(16,26,68,48,6)],[FS,SW(4),
    P(M(6,40),L(16,40),STROKE),P(M(6,60),L(16,60),STROKE),
    P(M(16,40),L(28,40),STROKE),P(M(28,40),L(24,36),STROKE),P(M(28,40),L(24,44),STROKE),
    CIRC(56,50,10),STROKE, P(M(56,30),L(56,24),STROKE),P(M(56,76),L(56,70),STROKE),P(M(36,50),L(30,50),STROKE),P(M(76,50),L(82,50),STROKE),
])
knx_add('KNX Smoke Detector','knx smoke fire',BLOCK,[RR(16,26,68,48,6)],[FS,SW(4),
    P(M(6,40),L(16,40),STROKE),P(M(6,60),L(16,60),STROKE),
    P(M(16,40),L(28,40),STROKE),P(M(28,40),L(24,36),STROKE),P(M(28,40),L(24,44),STROKE),
    CIRC(56,50,16),STROKE, CIRC(56,50,7),STROKE, P(M(56,34),L(56,28),STROKE),P(M(72,50),L(78,50),STROKE),P(M(40,50),L(34,50),STROKE),P(M(56,66),L(56,72),STROKE),
])
knx_add('KNX Water Leak Detector','knx leak water',BLOCK,[RR(16,26,68,48,6)],[FS,SW(4),
    P(M(6,40),L(16,40),STROKE),P(M(6,60),L(16,60),STROKE),
    P(M(16,40),L(28,40),STROKE),P(M(28,40),L(24,36),STROKE),P(M(28,40),L(24,44),STROKE),
    P(M(56,32),Q(72,54,56,70),Q(40,54,56,32),STROKE), P(M(40,76),Q(48,72,56,76),Q(64,80,72,76),STROKE),
])
knx_add('KNX Push Button/Keypad','knx button keypad',BLOCK,[RR(16,26,68,48,6)],[FS,SW(4),
    P(M(6,40),L(16,40),STROKE),P(M(6,60),L(16,60),STROKE),
    P(M(16,40),L(28,40),STROKE),P(M(28,40),L(24,36),STROKE),P(M(28,40),L(24,44),STROKE),
    RR(44,36,24,20,3),STROKE, P(M(48,44),L(64,44),STROKE), P(M(48,48),L(64,48),STROKE),
])
knx_add('KNX Actuator (Switching)','knx actuator switch output',BLOCK,[RR(16,26,68,48,6)],[FS,SW(4),
    P(M(6,40),L(16,40),STROKE),P(M(6,60),L(16,60),STROKE),
    P(M(68,40),L(84,40),STROKE),P(M(84,40),L(80,36),STROKE),P(M(84,40),L(80,44),STROKE),  # output
    P(M(68,60),L(84,60),STROKE),P(M(84,60),L(80,56),STROKE),P(M(84,60),L(80,64),STROKE),
    RECT(44,38,16,24),STROKE, P(M(44,50),L(60,50),STROKE), P(M(52,46),L(60,50),L(52,54),STROKE),
])
knx_add('KNX Dimming Actuator','knx dimmer actuator',BLOCK,[RR(16,26,68,48,6)],[FS,SW(4),
    P(M(6,40),L(16,40),STROKE),P(M(6,60),L(16,60),STROKE),
    P(M(68,40),L(84,40),STROKE),P(M(84,40),L(80,36),STROKE),P(M(84,40),L(80,44),STROKE),
    P(M(68,60),L(84,60),STROKE),P(M(84,60),L(80,56),STROKE),P(M(84,60),L(80,64),STROKE),
    P(M(40,50),L(68,50),STROKE), CIRC(40,50,5),STROKE, P(M(68,46),L(76,50),L(68,54),STROKE),
])
knx_add('KNX Blind/Shutter Actuator','knx blind shutter actuator',BLOCK,[RR(16,26,68,48,6)],[FS,SW(4),
    P(M(6,40),L(16,40),STROKE),P(M(6,60),L(16,60),STROKE),
    P(M(68,40),L(84,40),STROKE),P(M(84,40),L(80,36),STROKE),P(M(84,40),L(80,44),STROKE),
    P(M(68,60),L(84,60),STROKE),P(M(84,60),L(80,56),STROKE),P(M(84,60),L(80,64),STROKE),
    RECT(40,38,24,24),STROKE, P(M(46,42),L(58,42),STROKE),P(M(46,48),L(58,48),STROKE),P(M(46,54),L(58,54),STROKE), P(M(62,46),L(70,50),L(62,54),STROKE),
])
knx_add('KNX Heating/Radiator Actuator','knx heating valve actuator',BLOCK,[RR(16,26,68,48,6)],[FS,SW(4),
    P(M(6,40),L(16,40),STROKE),P(M(6,60),L(16,60),STROKE),
    P(M(68,40),L(84,40),STROKE),P(M(84,40),L(80,36),STROKE),P(M(84,40),L(80,44),STROKE),
    P(M(68,60),L(84,60),STROKE),P(M(84,60),L(80,56),STROKE),P(M(84,60),L(80,64),STROKE),
    RR(42,42,20,16,2),STROKE, CIRC(68,42,8),STROKE,P(M(68,34),L(68,22),STROKE),P(M(64,26),L(72,26),STROKE),
])
knx_add('KNX Power Supply (PSU)','knx power supply psu',BLOCK,[RR(16,26,68,48,6)],[FS,SW(4),
    P(M(6,40),L(16,40),STROKE),P(M(6,60),L(16,60),STROKE),  # feeds bus
    CIRC(48,50,14),STROKE, P(M(48,43),L(48,57),STROKE), P(M(62,44),L(72,44),STROKE),P(M(62,56),L(72,56),STROKE),
])
knx_add('KNX Line Coupler (LC)','knx line coupler lc area backbone',BLOCK,[RR(16,26,68,48,6)],[FS,SW(4),
    P(M(6,40),L(16,40),STROKE),P(M(6,60),L(16,60),STROKE),
    P(M(68,40),L(84,40),STROKE),P(M(84,40),L(80,36),STROKE),P(M(84,40),L(80,44),STROKE),
    P(M(68,60),L(84,60),STROKE),P(M(84,60),L(80,56),STROKE),P(M(84,60),L(80,64),STROKE),
    RECT(40,40,24,20),STROKE, P(M(42,38),L(42,32),STROKE),P(M(62,38),L(62,32),STROKE),P(M(42,62),L(42,68),STROKE),P(M(62,62),L(62,68),STROKE),
])
knx_add('KNX IP Router / Interface','knx ip router interface',BLOCK,[RR(16,26,68,48,6)],[FS,SW(4),
    P(M(6,40),L(16,40),STROKE),P(M(6,60),L(16,60),STROKE),
    P(M(68,40),L(84,40),STROKE),P(M(84,40),L(80,36),STROKE),P(M(84,40),L(80,44),STROKE),
    P(M(68,60),L(84,60),STROKE),P(M(84,60),L(80,56),STROKE),P(M(84,60),L(80,64),STROKE),
    P(M(34,46),L(66,46),STROKE),P(M(60,42),L(66,46),STROKE),P(M(60,50),L(66,46),STROKE),
    P(M(66,58),L(34,58),STROKE),P(M(40,54),L(34,58),STROKE),P(M(40,62),L(34,58),STROKE),
])
knx_add('KNX Binary Output/Relay','knx relay output',BLOCK,[RR(16,26,68,48,6)],[FS,SW(4),
    P(M(6,40),L(16,40),STROKE),P(M(6,60),L(16,60),STROKE),
    P(M(68,40),L(84,40),STROKE),P(M(84,40),L(80,36),STROKE),P(M(84,40),L(80,44),STROKE),
    P(M(68,60),L(84,60),STROKE),P(M(84,60),L(80,56),STROKE),P(M(84,60),L(80,64),STROKE),
    RECT(42,40,16,20),STROKE, P(M(42,50),L(58,50),STROKE), P(M(50,46),L(58,50),L(50,54),STROKE),
])
knx_add('KNX Gateway (Bidirectional)','knx gateway bridge',BLOCK,[RR(16,26,68,48,6)],[FS,SW(4),
    P(M(6,40),L(16,40),STROKE),P(M(6,60),L(16,60),STROKE),
    P(M(68,40),L(84,40),STROKE),P(M(84,40),L(80,36),STROKE),P(M(84,40),L(80,44),STROKE),
    P(M(68,60),L(84,60),STROKE),P(M(84,60),L(80,56),STROKE),P(M(84,60),L(80,64),STROKE),
    P(M(34,46),L(66,46),STROKE),P(M(60,42),L(66,46),STROKE),P(M(60,50),L(66,46),STROKE),
    P(M(66,58),L(34,58),STROKE),P(M(40,54),L(34,58),STROKE),P(M(40,62),L(34,58),STROKE),
])
knx_add('KNX Touch Panel/HMI','knx hmi touch panel',BLOCK,[RR(16,24,68,52,6)],[FS,SW(4),
    P(M(6,40),L(16,40),STROKE),P(M(6,60),L(16,60),STROKE),
    RECT(24,30,52,40),STROKE, CIRC(32,58,3),FS,P(M(40,58),L(68,58),STROKE),
])
knx_add('KNX Bus Terminator','knx terminator',BUS,[],[
    SW(4), P(M(6,40),L(32,40),STROKE),P(M(6,60),L(32,60),STROKE), RECT(32,38,20,24),STROKE, P(M(38,44),L(46,44),STROKE),P(M(38,38),L(38,46),STROKE), P(M(52,40),L(94,40),STROKE),P(M(52,60),L(94,60),STROKE),
])

# write IEC
iec_entries=[]
bgfg_map={}
for name,tags,style,bf in IEC:
    bgfg_map[name]=bf
for name,tags,style,bf in IEC:
    iec_entries.append({"title":name,"tags":tags,"xml":cell_for(name,style,bf),"w":80,"h":80})
n1,s1=write_lib('/home/delyan/Work/smarthome-drawio/smarthome.library.xml','smart home home-automation iec60617 electrical symbols',iec_entries)

# write KNX
knx_entries=[]
bgfg_map_k={}
for name,tags,style,bf in KNX:
    bgfg_map_k[name]=bf
for name,tags,style,bf in KNX:
    knx_entries.append({"title":name,"tags":tags,"xml":cell_for(name,style,bf),"w":80,"h":80})
n2,s2=write_lib('/home/delyan/Work/smarthome-drawio/knx.library.xml','knx iso iec 14543-3 home automation building automation',knx_entries)

print('IEC:',n1,'KNX:',n2)
