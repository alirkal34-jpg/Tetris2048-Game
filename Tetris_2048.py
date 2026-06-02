import lib.stddraw as stddraw
from lib.picture import Picture
from lib.color import Color
import os
import sys
from game_grid import GameGrid
from tetromino import Tetromino
import random

def main():
   """
   Main entry point for the Tetris-2048 game.
   Initializes the canvas, handles the main game loop, and processes user inputs.
   """
   grid_height, grid_width = 20, 12
   side_panel_width = 6
   cell_size = 40
   
   # Setup canvas dimensions
   canvas_height = cell_size * grid_height
   canvas_width = cell_size * (grid_width + side_panel_width)
   stddraw.setCanvasSize(canvas_width, canvas_height)
   stddraw.setXscale(-0.5, grid_width + side_panel_width - 0.5)
   stddraw.setYscale(-0.5, grid_height - 0.5)
   
   Tetromino.grid_height = grid_height
   Tetromino.grid_width = grid_width
   display_game_menu(grid_height, grid_width)
   
   while True:  
      grid = GameGrid(grid_height, grid_width)
      current_tetromino = create_tetromino()
      next_tetromino = create_tetromino()
      
      grid.current_tetromino = current_tetromino
      grid.next_tetromino = next_tetromino

      restart_game = False
      paused = False
      display_delay = 500
      min_display_delay = 90
      speedup_per_piece = 12

      while True:  
         # Handle user keyboard inputs
         if stddraw.hasNextKeyTyped():
            key_typed = stddraw.nextKeyTyped()
            if key_typed == 'p':
               paused = not paused
            elif paused and key_typed == 'r':
               restart_game = True
            elif key_typed == 'left' and not paused:
               current_tetromino.move(key_typed, grid)
            elif key_typed == 'right' and not paused:
               current_tetromino.move(key_typed, grid)
            elif key_typed == 'down' and not paused:
               current_tetromino.move(key_typed, grid)
            elif key_typed == 'up' and not paused:
               current_tetromino.rotate(grid)
            elif key_typed == 'space' and not paused:
               current_tetromino.hard_drop(grid)
               
            stddraw.clearKeysTyped()
         
         if restart_game:
            break

         if not paused:
            success = current_tetromino.move('down', grid)
            if not success:
               tiles, pos = current_tetromino.get_min_bounded_tile_matrix(True)
               grid.update_grid(tiles, pos)
               
               # Progressively increase the game speed to raise difficulty
               display_delay = max(min_display_delay,
                                 display_delay - speedup_per_piece)
                                 
               if grid.won:
                  break
               if grid.game_over:
                  break
                  
               current_tetromino = next_tetromino
               next_tetromino = create_tetromino()
               grid.current_tetromino = current_tetromino
               grid.next_tetromino = next_tetromino

         if not paused:
            grid.display(display_delay)
         else:
            display_pause_message(grid_width + side_panel_width, grid_height)

      if restart_game:
         continue

      if grid.won:
         print('You win')
         action = display_end_screen(grid, grid_width + side_panel_width, grid_height, True)
      elif grid.game_over:
         print('Game over')
         action = display_end_screen(grid, grid_width + side_panel_width, grid_height, False)
      else:
         action = 'restart' 

      if action == 'exit':
         sys.exit(0)


def create_tetromino():
   """
   Generates and returns a Tetromino object with a randomly selected shape.
   """
   tetromino_types = ['I', 'O', 'T', 'J', 'L', 'S', 'Z']
   random_type = random.choice(tetromino_types)
   tetromino = Tetromino(random_type)
   return tetromino

def display_end_screen(grid, canvas_grid_width, grid_height, won):
   background_color = Color(42, 69, 99)
   button_color = Color(255, 195, 0)   
   exit_color = Color(180, 60, 60)   
   text_color = Color(1, 1, 1)
   white = Color(255, 255, 255)

   center_x = (canvas_grid_width - 1) / 2
   center_y = (grid_height - 1) / 2

   btn_w, btn_h = 5.0, 1.6
   gap = 0.6
   restart_x = center_x - btn_w / 2 - gap / 2
   exit_x    = center_x - btn_w / 2 - gap / 2
   btn_y     = center_y - 4.5   

   while True:
      stddraw.clear(background_color)
      stddraw.setPenColor(white)
      stddraw.setFontFamily('Arial')

      stddraw.setFontSize(32)
      if won:
         stddraw.boldText(center_x, center_y + 3, 'YOU WIN!')
      else:
         stddraw.boldText(center_x, center_y + 3, 'GAME OVER')

      stddraw.setFontSize(22)
      stddraw.text(center_x, center_y + 1, 'Final Score: ' + str(grid.score))

      stddraw.setPenColor(button_color)
      stddraw.filledRectangle(restart_x, btn_y, btn_w, btn_h)
      stddraw.setPenColor(text_color)
      stddraw.setFontSize(18)
      stddraw.boldText(restart_x + btn_w / 2, btn_y + btn_h / 2, 'Restart')

      stddraw.setPenColor(exit_color)
      stddraw.filledRectangle(exit_x, btn_y - 3, btn_w, btn_h)
      stddraw.setPenColor(white)
      stddraw.setFontSize(18)
      stddraw.boldText(exit_x + btn_w / 2, btn_y - 3 + btn_h / 2, 'Exit')

      stddraw.show(50)

      if stddraw.mousePressed():
         mx, my = stddraw.mouseX(), stddraw.mouseY()

         if (restart_x <= mx <= restart_x + btn_w and
               btn_y   <= my <= btn_y   + btn_h):
            return 'restart'

         if (exit_x <= mx <= exit_x + btn_w and
               btn_y - 3 <= my <= btn_y - 3 + btn_h):
            return 'exit'


def display_pause_message(canvas_grid_width, grid_height):
   background_color = Color(42, 69, 99)
   stddraw.clear(background_color)

   current_dir = os.path.dirname(os.path.realpath(__file__))
   img_file = os.path.join(current_dir, 'images/pause_image.png')

   center_x = (canvas_grid_width - 1) / 2
   center_y = (grid_height - 1) / 2

   pause_image = Picture(img_file)
   stddraw.picture(pause_image, center_x, center_y)

   stddraw.setPenColor(Color(255, 255, 255))
   stddraw.setFontFamily('Arial')
   stddraw.setFontSize(28)
   stddraw.boldText(center_x, center_y - 5, 'Press P to Resume')
   stddraw.text(center_x, center_y - 7, 'Press R to Restart')

   stddraw.show(50)

def display_game_menu(grid_height, grid_width):
   background_color = Color(1, 1, 1)
   button_color = Color(255, 195, 0)
   text_color = Color(1, 1, 1)
   
   stddraw.clear(background_color)
   current_dir = os.path.dirname(os.path.realpath(__file__))
   img_file = os.path.join(current_dir, 'images/menu_image.png')
   img_center_x, img_center_y = 8, 15

   image_to_display = Picture(img_file)
   stddraw.picture(image_to_display, img_center_x, img_center_y)
   
   button_w, button_h = grid_width - 1.5, 2
   button_blc_x, button_blc_y = img_center_x - button_w / 2, 4
   
   stddraw.setPenColor(button_color)
   stddraw.filledRectangle(button_blc_x, button_blc_y, button_w, button_h)
   stddraw.setFontFamily('Arial')
   stddraw.setFontSize(25)
   stddraw.setPenColor(text_color)
   stddraw.text(img_center_x, 5, 'Click Here to Start the Game')

   stddraw.setPenColor(button_color)
   stddraw.setFontFamily('Arial')
   stddraw.setFontSize(25)
   stddraw.setPenColor(button_color)
   control_text_to_display = ('Controls: Arrow keys to move/rotate,'
                              ' space for hard drop, P to pause')
   stddraw.text(button_blc_x + 6, 9, control_text_to_display)

   while True:
      stddraw.show(50)
      if stddraw.mousePressed():
         mouse_x, mouse_y = stddraw.mouseX(), stddraw.mouseY()
         if mouse_x >= button_blc_x and mouse_x <= button_blc_x + button_w:
            if mouse_y >= button_blc_y and mouse_y <= button_blc_y + button_h:
               break


main()