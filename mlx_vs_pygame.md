mlx_init()	pygame.init()
mlx_new_window()	pygame.display.set_mode()
mlx_clear_window()	screen.fill()
mlx_pixel_put()	screen.set_at()
mlx_new_image()	pygame.Surface()
mlx_get_data_addr()	pygame.PixelArray() / Surface.get_view()
mlx_put_image_to_window()	screen.blit()
mlx_destroy_image()	usually just del surface / garbage collection
mlx_destroy_window()	pygame.display.quit() / pygame.quit()
mlx_loop()	your own while running: loop
mlx_loop_exit()	set running = False
mlx_key_hook()	pygame.event.get() + KEYDOWN/KEYUP
mlx_mouse_hook()	MOUSEBUTTONDOWN/UP
mlx_expose_hook()	normally unnecessary; redraw every frame
mlx_loop_hook()	code inside your game loop
mlx_hook()	pygame.event.get()
mlx_string_put()	pygame.font.Font().render() + blit()
mlx_png_file_to_image()	pygame.image.load()
mlx_xpm_file_to_image()	pygame.image.load() if format supported
mlx_mouse_hide()	pygame.mouse.set_visible(False)
mlx_mouse_show()	pygame.mouse.set_visible(True)
mlx_mouse_move()	pygame.mouse.set_pos()
mlx_mouse_get_pos()	pygame.mouse.get_pos()
mlx_get_screen_size()	pygame.display.Info()
mlx_do_sync()	pygame.display.flip() / update()
mlx_sync()	roughly pygame.display.update()
