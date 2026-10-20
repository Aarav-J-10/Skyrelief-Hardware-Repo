# Visual and source review
The three native schematic PDFs were rendered with Poppler and inspected at a complete A4-page view. Final text was enlarged before re-export. Native symbols, labels and wires remain distinct; no clipped drawing-sheet frame is used. KiCad exports use its stroke font, not an external font dependency.

All custom SVGs were rasterized with libvips/sharp and visually reviewed for font rendering, clipping and relationship direction. The detailed peripheral crosswalk has a separate FPV power association, not a wire to Pixhawk. Dashed role arrows represent unresolved implementation. SVG source retains editable text and vector elements with Arial/sans-serif fallback.

The new R01 dimension SVG/PDF and locked/released CAD preview were inspected. The profile is an independent keyhole/neck design, not traced historical geometry. Its drawing is nominal, not a tolerance or manufacturing qualification. Preview colours distinguish parts, not assigned materials.

Eight documentary photos were selected after individually inspecting all 38 source images. Original asset hashes and any metadata treatment are recorded; vendor diagrams/catalogue images are excluded. No object reconstruction or image-generation enhancement was used.
