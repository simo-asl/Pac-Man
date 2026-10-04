from mazegenerator import MazeGenerator
import pygame
import mlx


ml = mlx.Mlx()
ml_pointer = ml.mlx_init()
ml.mlx_loop(ml_pointer)
ml.mlx_new_window(ml_pointer, 5000, 1000, "hello")
ml.mlx_loop_exit(ml_pointer)
