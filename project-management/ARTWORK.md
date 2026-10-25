# Sprite quality and provenance

The player and ghosts retain their classic silhouettes and colors, remastered
from the original repository's 30×30 PNGs using the built-in imagegen tool.
The final transparent sprite-sheet cells were extracted into 314×314 PNGs in
`src/assets/arcade/`. Player directions are rotations of its right-facing image.
The game uses smooth scaling from these larger sources; the image count is unchanged.

Backgrounds are drawn at native window resolution by `src/ui/background.py`.
Walls use rounded geometry, rendered at double resolution and downsampled once
into the cached maze. Neither relies on enlarged low-resolution bitmap tiles.

## Generation prompt

Use case: identity-preserve game asset remaster. Edit target: the attached transparent 3-column 2-row sprite sheet. Produce a high-resolution, beautifully clean antialiased version of these EXACT six classic arcade characters, same identity and same visual design, replacing the low resolution stair-step pixel edges with smooth precise curves and fine clean shading. Maintain the same 3 columns by 2 rows grid of six equal-size cells, with one character centered in each cell and ample fully transparent padding between them. Top row left: the same yellow Pac-Man circle facing right, open triangular mouth, NO eye, no arms or legs. Top middle: the same red ghost with two white eyes, dark blue pupils looking right, round dome and scalloped lower edge. Top right: same pink ghost. Bottom left: same cyan ghost. Bottom middle: same orange ghost. Bottom right: same frightened cobalt blue ghost, two small white eyes and white zigzag mouth. Keep original flat arcade silhouettes and colors and tiny subtle upper-left shading; do not introduce black outlines, 3D plastic, glossy highlights, accessories, extra facial features or realistic textures. Maximum sharp vector-style image quality. All six characters have identical bounding-box dimensions, centered precisely in their cell. Transparent background and transparent Pac-Man mouth, no shadows, no checkerboard, no text, no decorations. Landscape 3:2 sheet, ideally 3072x2048 pixels. This is a clean higher-resolution remaster of the original artwork, not a redesign.

## Final correction prompt

Edit this 3-column by 2-row game sprite sheet. Make ONLY this correction: REMOVE ALL outer glow, bloom, shadows, halos, and shiny/glossy white highlights from all six characters. The background and every character's surroundings must be fully transparent, including inside Pac-Man's open mouth. Bodies must be clean solid color with at most a tiny subtle upper-left tone variation, no glossy shine, no blur. Preserve the exact six characters, their classic silhouettes, eyes, colors, cell layout, scale, positions, facial features and high resolution. Top left remains yellow Pac-Man facing right with triangular open mouth and NO eye. Crisp smooth antialiased outlines. Do not add or move any shapes. Transparent RGBA PNG.
