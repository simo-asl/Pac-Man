ROYAL GOLD MAZE / PYGAME ASSET PACK
==================================
wall tiles: walls/0.png ... walls/15.png (256x256 transparent PNG)
0 empty; bit 1 north, 2 east, 4 south, 8 west.
The gold is generated using deterministic rendering so edges and layouts match your existing bitmask logic.
Background: hud_background_1800x1200.png
Maze area approx x=34..1425 and y=192..1157. HUD: top and right panels.
maze_hud_preview.png is only an illustrative layout; draw your actual maze on the background.

EXAMPLE LOADER (adapt to your own class):
    tiles = {i: pygame.transform.scale(
        pygame.image.load(f"src/game/assets/maze/{i}.png").convert_alpha(),
        (cell_size, cell_size)) for i in range(16)}
    screen.blit(tiles[cell], (x,y))

IMPORTANT: The HUD frame does NOT contain UI text. Add lives, score, time etc in pygame.
The sheet named glossy_gold_border_tile_sprite_sheet.png is an extra concept illustration, NOT the exact bitmask sprites.
