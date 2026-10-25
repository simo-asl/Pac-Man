# Graphics API comparison

The backend remains Pygame. This comparison uses both official headers:

- https://github.com/42Paris/minilibx-linux/blob/master/mlx.h
- https://github.com/codam-coding-college/MLX42/blob/master/include/MLX42/MLX42.h

| Operation used | Codam MLX42 | Paris MiniLibX |
| --- | --- | --- |
| Window initialization/title | `mlx_init`, `mlx_set_window_title` | `mlx_init`, `mlx_new_window` |
| Image allocation | `mlx_new_image` | `mlx_new_image` |
| PNG decoding | `mlx_load_png` | No PNG loader in the Linux header; XPM only |
| Image placement / frame presentation | `mlx_image_to_window`, `mlx_loop` | `mlx_put_image_to_window`, `mlx_loop` |
| Pixel writes and buffer access | `mlx_put_pixel`, image `pixels` | `mlx_pixel_put`, `mlx_get_data_addr` |
| Image dimensions | Image `width` and `height` | Dimensions retained when creating/loading images |
| Image resize (`pygame.transform.scale`) | `mlx_resize_image` | Implement through image-buffer writes |
| Key events | `mlx_key_hook` | `mlx_hook`, `mlx_key_hook` |
| Held key polling | `mlx_is_key_down` | Maintain state from key press/release hooks |
| Text input from key events | `mlx_char_hook` | Translate key events |
| Elapsed milliseconds | `mlx_get_time` converted to milliseconds | Standard-library clock |
| Close/cleanup | `mlx_close_hook`, `mlx_close_window`, `mlx_terminate` | Close event hook, destroy window/display |

`Draw.fill_rect` fills rows through the pixel buffer; line/circle/rectangle
rasterization also uses buffer/pixel operations. No Pygame shape drawing,
rotation, audio, collision helpers or font APIs are used. The frame limiter
uses Python `time.monotonic` and `time.sleep`, since neither library exposes
Pygame's `Clock.tick` operation. RGBA image placement follows Codam's image
model; this is not a claim of strict compatibility with Paris Linux MLX.

## Bitmap fonts

`bdfparser` loads the bundled Tamzen Bold BDF font. Each glyph already contains
its pixel bitmap in the file; no outline font rasterizer is used. `Draw` uses
two loops and fills one square for each set bit directly on the target.
Integer scales of 1, 2, 3, and so on determine the square size. This follows
Codam's bitmap-font approach (`mlx_get_font`, `mlx_get_texoffset`) using a custom
bitmap asset. Neither Pillow nor the Pygame font subsystem is required.
