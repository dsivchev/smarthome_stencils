#!/usr/bin/env python3
# Generates smarthome.library.xml : an importable draw.io (mxlibrary)
# of generic SmartHome / home-automation stencils (native, recolorable).
import base64, zlib, urllib.parse, json, html, re

# ---------------- stencil DSL (100x100 grid) ----------------
def M(x, y): return f'<move x="{x}" y="{y}"/>'
def L(x, y): return f'<line x="{x}" y="{y}"/>'
def Q(cx, cy, x, y): return f'<quad x1="{cx}" y1="{cy}" x="{x}" y="{y}"/>'
def CU(c1x,c1y,c2x,c2y,x,y): return f'<curve x1="{c1x}" y1="{c1y}" x2="{c2x}" y2="{c2y}" x="{x}" y="{y}"/>'
def A(rx, ry, x, y, rot=0, laf=0, sf=1):
    return f'<arc rx="{rx}" ry="{ry}" x-axis-rotation="{rot}" large-arc-flag="{laf}" sweep-flag="{sf}" x="{x}" y="{y}"/>'
def RECT(x, y, w, h): return f'<rect x="{x}" y="{y}" w="{w}" h="{h}"/>'
def RR(x, y, w, h, arc=8): return f'<roundrect x="{x}" y="{y}" w="{w}" h="{h}" arcsize="{arc}"/>'
def ELL(x, y, w, h): return f'<ellipse x="{x}" y="{y}" w="{w}" h="{h}"/>'
def P(*ops): return '<path>' + ''.join(ops) + '</path>'
def CIRC(cx, cy, r): return ELL(cx-r, cy-r, 2*r, 2*r)
STROKE = '<stroke/>'; FILL = '<fill/>'; FS = '<fillstroke/>'
def SW(w): return f'<strokewidth width="{w}"/>'
CLOSE = '<close/>'
SAVE = '<save/>'; RESTORE = '<restore/>'

def conns():
    pts = [('N',.5,0),('S',.5,1),('W',0,.5),('E',1,.5),
           ('NW',0,0),('NE',1,0),('SW',0,1),('SE',1,1)]
    return '<connections>' + ''.join(
        f'<constraint name="{n}" perimeter="0" x="{x}" y="{y}"/>' for n,x,y in pts) + '</connections>'

def shape_xml(name, bg, fg):
    s = f'<shape name="{html.escape(name)}" h="100" w="100" aspect="variable" strokewidth="inherit">'
    s += conns()
    if bg:
        s += '<background>' + ''.join(bg) + '</background>'
    s += '<foreground>' + ''.join(fg) + '</foreground></shape>'
    return s

# ---------------- encoding ----------------
def b64deflate(text):
    co = zlib.compressobj(9, zlib.DEFLATED, -15)
    data = co.compress(urllib.parse.quote(text, safe='').encode('utf-8')) + co.flush()
    return base64.b64encode(data).decode('ascii')

# style presets
ICON  = 'fillColor=none;strokeColor=#4D4D4D;strokeWidth=1;'
BLOCK = 'fillColor=#dae8fc;strokeColor=#6c8ebf;strokeWidth=1;'
BUS   = 'fillColor=#4D4D4D;strokeColor=#4D4D4D;strokeWidth=1;'

SHAPES = []
def add(name, tags, style, bg, fg):
    SHAPES.append((name, tags, style, bg, fg))

# =====================================================================
# SENSING & SECURITY
# =====================================================================
add("Motion Sensor (PIR)", "pir motion detector presence", ICON, [], [
    SW(4),
    P(M(22,70), Q(50,18,78,70), STROKE),
    P(M(16,70), L(84,70), STROKE),
    CIRC(50,58,8), STROKE,
    P(M(82,54), Q(92,44,82,34), STROKE),
    P(M(88,60), Q(99,44,88,28), STROKE),
])
add("Door / Window Contact", "door window contact reed magnetic", ICON, [], [
    SW(4),
    RR(14,32,32,36,4), STROKE,
    RR(56,36,28,28,3), STROKE,
    CIRC(50,50,2.5), FS,
    P(M(80,30), Q(90,22,96,30), STROKE),
    P(M(83,24), Q(92,15,99,22), STROKE),
])
add("Smoke Detector", "smoke detector fire alarm", ICON, [], [
    SW(4),
    CIRC(50,46,29), STROKE,
    CIRC(50,46,11), STROKE,
    P(M(50,17), L(50,6), STROKE), P(M(79,46), L(90,46), STROKE),
    P(M(21,46), L(10,46), STROKE), P(M(50,75), L(50,86), STROKE),
    CIRC(50,46,3.5), FS,
])
add("Water Leak Sensor", "water leak flood moisture", ICON, [], [
    SW(4),
    P(M(50,16), Q(76,52,50,78), Q(24,52,50,16), STROKE),
    P(M(24,88), Q(37,83,50,88), Q(63,93,76,88), STROKE),
])
add("Temperature Sensor", "temperature thermometer heat", ICON, [], [
    SW(4),
    RR(43,14,14,54,7), STROKE,
    CIRC(50,78,13), STROKE,
    P(M(50,28), L(50,78), STROKE),
    P(M(60,24), L(66,24), STROKE), P(M(60,36), L(66,36), STROKE), P(M(60,48), L(66,48), STROKE),
])
add("Humidity Sensor", "humidity moisture rh percent", ICON, [], [
    SW(4),
    P(M(50,12), Q(78,50,50,84), Q(22,50,50,12), STROKE),
    CIRC(42,44,4.5), STROKE, CIRC(58,62,4.5), STROKE,
    P(M(38,66), L(62,40), STROKE),
])
add("Brightness / Lux Sensor", "lux brightness light illuminance sun", ICON, [], [
    SW(4),
    CIRC(50,50,15), STROKE,
    P(M(50,20), L(50,8), STROKE), P(M(50,80), L(50,92), STROKE),
    P(M(20,50), L(8,50), STROKE), P(M(80,50), L(92,50), STROKE),
    P(M(29,29), L(20,20), STROKE), P(M(71,29), L(80,20), STROKE),
    P(M(29,71), L(20,80), STROKE), P(M(71,71), L(80,80), STROKE),
])
add("Air Quality / CO2 Sensor", "air quality co2 voc gas wind", ICON, [], [
    SW(4),
    P(M(16,38), Q(32,30,48,38), Q(64,46,84,38), STROKE),
    P(M(16,54), Q(32,46,48,54), Q(64,62,84,54), STROKE),
    CIRC(66,72,5), STROKE, CIRC(78,82,3.5), STROKE,
])
add("Siren / Alarm", "siren alarm sound horn buzzer", ICON, [], [
    SW(4),
    RR(26,38,16,24,3), STROKE,
    P(M(42,38), L(64,22), L(64,78), L(42,62), CLOSE, STROKE),
    P(M(70,42), Q(80,50,70,58), STROKE),
    P(M(77,34), Q(92,50,77,66), STROKE),
])
add("Camera (CCTV)", "camera cctv surveillance video", ICON, [], [
    SW(4),
    RR(18,32,48,26,6), STROKE,
    CIRC(66,45,8), STROKE,
    P(M(30,58), L(30,74), L(46,74), STROKE),
    P(M(24,28), L(30,32), STROKE),
])
add("Door Lock", "lock door lock security access", ICON, [], [
    SW(4),
    P(M(34,46), L(34,32), Q(50,14,66,32), L(66,46), STROKE),
    RR(27,46,46,38,5), STROKE,
    CIRC(50,61,5.5), STROKE, P(M(50,66), L(50,76), STROKE),
])
add("Glass Break Sensor", "glass break impact vibration window", ICON, [], [
    SW(4),
    RECT(20,20,60,60), STROKE,
    P(M(50,50), L(34,30), STROKE), P(M(50,50), L(66,28), STROKE),
    P(M(50,50), L(74,54), STROKE), P(M(50,50), L(62,74), STROKE),
    P(M(50,50), L(32,70), STROKE),
])
add("Panic Button", "panic emergency button alarm", ICON, [], [
    SW(4),
    CIRC(50,50,32), STROKE, CIRC(50,50,23), STROKE,
    P(M(50,32), L(50,54), STROKE), CIRC(50,64,3.5), FS,
])
add("Keypad", "keypad code pin access panel", ICON, [], [
    SW(4),
    RR(24,14,52,72,6), STROKE,
    RECT(32,22,36,12), STROKE,
    *[CIRC(cx, cy, 4.5) + STROKE for cy in (50,64,78) for cx in (36,50,64)],
])

# =====================================================================
# LIGHTING & SHADING
# =====================================================================
add("Light Switch", "switch light toggle rocker", ICON, [], [
    SW(4),
    RR(30,12,40,76,7), STROKE,
    RR(38,20,24,60,4), STROKE,
    P(M(38,44), L(62,44), STROKE),
])
add("Dimmer", "dimmer dim light level brightness", ICON, [], [
    SW(4),
    P(M(12,50), L(74,50), STROKE),
    CIRC(30,50,10), STROKE,
    P(M(74,48), L(88,48), STROKE),
    P(M(80,62), L(88,70), STROKE), P(M(88,62), L(80,70), STROKE),
])
add("Light Bulb", "bulb lamp light lighting", ICON, [], [
    SW(4),
    CIRC(50,40,22), STROKE,
    P(M(40,58), L(40,68), STROKE), P(M(60,58), L(60,68), STROKE),
    P(M(40,72), L(60,72), STROKE), P(M(42,78), L(58,78), STROKE),
    P(M(43,48), Q(50,40,57,48), STROKE),
])
add("RGB / LED Strip", "led strip rgb color lighting tape", ICON, [], [
    SW(4),
    RR(12,42,76,16,6), STROKE,
    CIRC(28,50,5), STROKE, CIRC(50,50,5), STROKE, CIRC(72,50,5), STROKE,
    P(M(28,32), L(28,24), STROKE), P(M(50,30), L(50,20), STROKE), P(M(72,32), L(72,24), STROKE),
])
add("Blind / Shutter", "blind shutter roller cover slats", ICON, [], [
    SW(4),
    RECT(22,14,56,72), STROKE,
    P(M(22,28), L(78,28), STROKE), P(M(22,40), L(78,40), STROKE),
    P(M(22,52), L(78,52), STROKE), P(M(22,64), L(78,64), STROKE),
    P(M(22,74), L(78,74), STROKE),
])
add("Curtain", "curtain drape window shading", ICON, [], [
    SW(4),
    P(M(12,22), L(88,22), STROKE),
    CIRC(12,22,3.5), STROKE, CIRC(88,22,3.5), STROKE,
    P(M(34,24), Q(20,54,34,84), L(48,84), Q(44,54,50,24), CLOSE, STROKE),
    P(M(66,24), Q(80,54,66,84), L(52,84), Q(56,54,50,24), CLOSE, STROKE),
])
add("Thermostat", "thermostat temperature dial hvac control", ICON, [], [
    SW(4),
    CIRC(50,50,30), STROKE, CIRC(50,50,21), STROKE,
    P(M(50,50), L(64,38), STROKE),
    P(M(50,20), L(50,14), STROKE), P(M(50,86), L(50,80), STROKE),
    P(M(20,50), L(14,50), STROKE), P(M(86,50), L(80,50), STROKE),
])
add("HVAC / Radiator", "radiator hvac valve heating", ICON, [], [
    SW(4),
    RR(16,42,52,42,4), STROKE,
    P(M(29,42), L(29,84), STROKE), P(M(42,42), L(42,84), STROKE), P(M(55,42), L(55,84), STROKE),
    CIRC(80,50,10), STROKE, P(M(80,40), L(80,20), STROKE), P(M(72,26), L(88,26), STROKE),
])
add("Fan / Ventilation", "fan ventilation air extractor", ICON, [], [
    SW(4),
    CIRC(50,50,9), STROKE,
    P(M(50,50), Q(24,24,50,20), Q(62,36,50,50), CLOSE, STROKE),
    P(M(50,50), Q(76,24,80,50), Q(64,62,50,50), CLOSE, STROKE),
    P(M(50,50), Q(24,76,50,80), Q(38,64,50,50), CLOSE, STROKE),
    P(M(50,50), Q(76,76,80,50), Q(62,38,50,50), CLOSE, STROKE),
])
add("Heating Circuit", "heating circuit pump floor water", ICON, [], [
    SW(4),
    P(M(12,42), L(88,42), STROKE), P(M(12,62), L(88,62), STROKE),
    CIRC(50,52,13), STROKE, P(M(46,45), L(57,52), L(46,59), CLOSE, STROKE),
    P(M(30,30), Q(36,24,42,30), STROKE), P(M(58,30), Q(64,24,70,30), STROKE),
])
add("Power Outlet", "outlet socket power plug", ICON, [], [
    SW(4),
    RR(28,14,44,72,10), STROKE,
    CIRC(42,42,4.5), FS, CIRC(58,42,4.5), FS,
    P(M(50,62), L(50,70), STROKE), CIRC(50,73,3.5), STROKE,
])
add("Relay Output", "relay output contact switch actuator", ICON, [], [
    SW(4),
    RR(18,28,64,44,5), STROKE,
    P(M(30,58), L(30,42), L(62,42), STROKE),
    CIRC(30,58,3.5), FS, CIRC(70,58,3.5), FS,
    P(M(70,58), L(58,44), STROKE),
])

# =====================================================================
# INFRASTRUCTURE & BUSES
# =====================================================================
add("Gateway / Hub", "gateway hub bridge central", BLOCK, [RR(18,34,64,48,7)], [
    FS, SW(4),
    P(M(64,34), L(72,14), STROKE), CIRC(72,12,3.5), STROKE,
    P(M(38,56), L(38,66), STROKE), L(62,66), STROKE, L(62,56), STROKE,
    P(M(30,56), L(30,66), STROKE),
])
add("Miniserver / Controller", "miniserver controller plc cpu logic", BLOCK, [RR(16,20,68,60,7)], [
    FS, SW(4),
    RECT(34,38,32,26), STROKE,
    P(M(34,44), L(26,44), STROKE), P(M(34,52), L(26,52), STROKE), P(M(34,60), L(26,60), STROKE),
    P(M(66,44), L(74,44), STROKE), P(M(66,52), L(74,52), STROKE), P(M(66,60), L(74,60), STROKE),
    P(M(42,28), L(42,38), STROKE), P(M(58,28), L(58,38), STROKE),
])
add("Actuator", "actuator switch drive output relay", BLOCK, [RR(16,24,68,52,7)], [
    FS, SW(4),
    CIRC(36,50,10), STROKE,
    P(M(46,50), L(72,50), STROKE),
    P(M(72,50), L(64,44), STROKE), P(M(72,50), L(64,56), STROKE),
    P(M(36,34), L(36,26), STROKE),
])
add("Sensor Module", "sensor input module io", BLOCK, [RR(16,24,68,52,7)], [
    FS, SW(4),
    P(M(16,38), L(44,38), STROKE), P(M(44,38), L(38,33), STROKE), P(M(44,38), L(38,43), STROKE),
    P(M(16,62), L(44,62), STROKE), P(M(44,62), L(38,57), STROKE), P(M(44,62), L(38,67), STROKE),
    RECT(54,34,22,32), STROKE,
])
add("KNX Bus Line", "knx bus line tp cable pair", BUS, [], [
    SW(4),
    P(M(8,44), L(92,44), STROKE), P(M(8,56), L(92,56), STROKE),
    P(M(26,44), L(26,30), STROKE), P(M(50,44), L(50,30), STROKE), P(M(74,44), L(74,30), STROKE),
    CIRC(26,26,5), FS, CIRC(50,26,5), FS, CIRC(74,26,5), FS,
])
add("Bus Power Supply", "power supply knx bus 24v psu", BLOCK, [RR(16,28,68,44,6)], [
    FS, SW(4),
    CIRC(44,50,15), STROKE, P(M(44,42), L(44,58), STROKE),
    P(M(58,42), L(70,42), STROKE), P(M(58,58), L(70,58), STROKE),
    P(M(20,50), L(8,50), STROKE),
])
add("IP Router", "ip router interface network knx", BLOCK, [RR(18,30,64,46,7)], [
    FS, SW(4),
    P(M(30,42), L(70,42), STROKE), P(M(62,36), L(70,42), STROKE), P(M(62,48), L(70,42), STROKE),
    P(M(70,64), L(30,64), STROKE), P(M(38,58), L(30,64), STROKE), P(M(38,70), L(30,64), STROKE),
])
add("Line Coupler", "line coupler area knx backbone", BUS, [], [
    SW(4),
    P(M(8,34), L(92,34), STROKE), P(M(8,66), L(92,66), STROKE),
    RECT(40,42,20,16), STROKE,
    P(M(50,34), L(50,42), STROKE), P(M(50,58), L(50,66), STROKE),
])
add("Extension I/O", "extension io module ports expand", BLOCK, [RR(16,26,68,48,7)], [
    FS, SW(4),
    *[RECT(24+ i*14, 38, 9, 24) + STROKE for i in range(4)],
])
add("Wall Push Button", "push button wall switch taster", ICON, [], [
    SW(4),
    RR(24,16,52,68,7), STROKE,
    RR(34,26,32,48,5), STROKE,
])
add("Touch Panel / Visualisation", "touch panel display visualisation hmi", BLOCK, [RR(16,20,68,60,7)], [
    FS, SW(4),
    RECT(24,28,52,44), STROKE,
    P(M(30,40), L(58,40), STROKE), P(M(30,50), L(70,50), STROKE),
    CIRC(34,62,3.5), FS, P(M(44,62), L(70,62), STROKE),
])
add("Relay Module", "relay module shelly inching sonoff", BLOCK, [RR(24,22,52,56,7)], [
    FS, SW(4),
    RECT(36,40,28,20), STROKE,
    P(M(50,28), L(50,40), STROKE), CIRC(50,25,3.5), STROKE,
    P(M(36,32), L(28,32), STROKE), P(M(64,32), L(72,32), STROKE),
])
add("DALI Gateway", "dali gateway lighting control", BLOCK, [RR(16,24,68,52,7)], [
    FS, SW(4),
    CIRC(36,40,9), STROKE, CIRC(36,60,9), STROKE,
    P(M(45,40), L(70,50), STROKE), P(M(45,60), L(70,50), STROKE),
])
add("Bus Terminator", "terminator resistor end bus knx", BUS, [], [
    SW(4),
    P(M(8,50), L(38,50), STROKE),
    RECT(38,40,24,20), STROKE,
    P(M(62,50), L(92,50), STROKE),
    P(M(44,44), L(56,44), STROKE), P(M(44,40), L(44,48), STROKE),
])
add("Server / Rack", "server rack host it network", BLOCK, [RR(26,12,48,76,6)], [
    FS, SW(4),
    *[P(M(34,y), L(66,y), STROKE) + CIRC(62,y+9,3) + STROKE for y in (24,40,56,72)],
])
add("Network Switch", "switch ethernet lan ports network", BLOCK, [RR(14,34,72,34,6)], [
    FS, SW(4),
    *[RECT(20+i*13, 52, 9, 10) + STROKE for i in range(5)],
    P(M(24,44), L(40,44), STROKE), P(M(34,40), L(40,44), STROKE), P(M(34,48), L(40,44), STROKE),
    P(M(60,44), L(76,44), STROKE), P(M(70,40), L(76,44), STROKE), P(M(70,48), L(76,44), STROKE),
])
add("Power Supply", "power supply psu ac dc transformer", BLOCK, [RR(16,30,68,42,6)], [
    FS, SW(4),
    P(M(28,42), Q(36,36,44,44), Q(52,52,60,44), STROKE),
    P(M(30,60), L(48,60), STROKE), P(M(30,66), L(48,66), STROKE),
    P(M(58,54), L(70,54), STROKE), P(M(58,66), L(70,66), STROKE),
])
add("Cloud / Remote Access", "cloud remote access vpn internet", ICON, [], [
    SW(4),
    P(M(28,66), Q(10,66,12,52), Q(12,40,28,41), Q(32,24,52,27), Q(70,26,74,44),
      Q(90,45,88,56), Q(90,66,74,66), CLOSE, STROKE),
    P(M(36,82), L(50,74), L(50,82), STROKE), P(M(64,82), L(50,74), STROKE),
])

# ---------------- emit library ----------------
def cell_for(name, style):
    sx = shape_xml(name, *bg_fg[name])
    payload = b64deflate(sx)
    cellstyle = f'shape=stencil({payload});verticalLabelPosition=bottom;verticalAlign=top;html=1;whiteSpace=wrap;{style}'
    model = ('<mxGraphModel><root><mxCell id="0"/><mxCell id="1" parent="0"/>'
             f'<mxCell id="2" value="" style="{cellstyle}" vertex="1" parent="1">'
             '<mxGeometry width="80" height="80" as="geometry"/></mxCell></root></mxGraphModel>')
    return b64deflate(model)

# build lookup
bg_fg = {name: (bg, fg) for name, tags, style, bg, fg in SHAPES}

entries = []
for name, tags, style, bg, fg in SHAPES:
    entries.append({
        "title": name,
        "tags": tags,
        "xml": cell_for(name, style),
        "w": 80, "h": 80,
    })

lib = '<mxlibrary tags="smart home home-automation knx loxone iot sensor actuator">' + json.dumps(entries) + '</mxlibrary>'
open('smarthome.library.xml', 'w', encoding='utf-8').write(lib)
print("shapes:", len(entries), "bytes:", len(lib))
