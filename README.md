# SmartHome & KNX draw.io Libraries

Two native, recolorable draw.io stencil sets for home/ building automation.

## Libraries
- `smarthome.library.xml` — IEC 60617 style (general electrical/home-automation symbols). 38 shapes.
- `knx.library.xml` — ISO/IEC 14543-3 (KNX) style (functional blocks with bus I/O arrows). 21 shapes.

## Import
1. Open draw.io (app.diagrams.net or desktop).
2. **File → Open Library from → Device...** and select one of the `.xml` files above.
3. Library appears in Extras; drag shapes onto canvas.

## Notes
- True native stencils (`shape=stencil(...)`) — recolorable, scalable.
- Labels placed under each glyph (`verticalLabelPosition=bottom;verticalAlign=top`).
- Regenerate both with `python3 gen.py`.
