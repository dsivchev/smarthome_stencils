# SmartHome draw.io Library

Native, recolorable draw.io stencils for home-automation / IoT / smart-home diagramming (sensing & security, lighting & shading, infrastructure & buses). 44 shapes.

## Import into draw.io

1. Open draw.io (app.diagrams.net or the desktop app).
2. **File > Open Library from > Device...** and select `smarthome.library.xml`.

The library panel appears under Extras (or alongside existing libraries). Drag any shape onto the canvas.

## Notes
- All shapes are true draw.io stencils (not images) — recolor fill/stroke like any shape, resize freely.
- Shape names double as search keywords; the library is also tagged `smart home home-automation knx loxone iot sensor actuator` for search.
- Each entry renders at a default 80x80 with a label under the glyph.
- Regenerate with `python3 gen.py` (no dependencies; stdlib only).
