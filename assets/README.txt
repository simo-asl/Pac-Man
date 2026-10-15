PAC-MAN INSPIRED ASSET PACK — original generated artwork

Contents:
  ghosts/ - 4 colored ghosts x 4 facing directions + static aliases, eyes sprites, frightened blue, frightened flashing
  pacman/ - four directions x closed, half, open
  items/ - regular and super pacgums
  maze/ - 16 transparent tile overlays for bitmasks 0..15
  backgrounds/ - seamless 64x64 background textures
  ui/ - small life icon and HUD panel
  root blinky.png / pinky.png / inky.png / clyde.png for compatibility

All gameplay sprites are 30 x 30 pixels except background tile (64x64) and HUD panel (220x56).

IMPORTANT: Maze tile overlays have walls drawn on the tile's outer edges.
With a shared wall between cells, neighboring tiles may draw the same boundary twice.
The glowing edges are a visual starting point; if you see seam irregularities,
use one consistent edge owner or adjust drawing to only draw each wall once.

Original generated artwork for your project. No external game assets copied.
Not verified as pixel-perfect replicas of Namco arcade graphics.

Pygame usage examples:
 sprite = pygame.image.load("src/game/assets/ghosts/frightened_blue.png").convert_alpha()
 draw.draw_image(sprite, px - 15, py - 15)
 background = pygame.image.load("src/game/assets/backgrounds/clean_navy_tile_64.png").convert()

Your ghost asset path can stay src/game/assets/blinky.png if you copy the ZIP contents into src/game/assets/.
