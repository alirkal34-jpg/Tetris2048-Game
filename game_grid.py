import lib.stddraw as stddraw
from lib.color import Color
from point import Point
import numpy as np

class GameGrid:
   def __init__(self, grid_h, grid_w):
      self.grid_height = grid_h
      self.grid_width = grid_w
      self.tile_matrix = np.full((grid_h, grid_w), None)
      self.current_tetromino = None
      self.next_tetromino = None
      self.score = 0
      self.game_over = False
      self.won = False
      self.empty_cell_color = Color(42, 69, 99)
      self.line_color = Color(0, 100, 200)
      self.boundary_color = Color(0, 100, 200)
      self.line_thickness = 0.002
      self.box_thickness = 5 * self.line_thickness

   def display(self, pause_duration = 500):
      stddraw.clear(self.empty_cell_color)
      self.draw_grid()
      if self.current_tetromino is not None:
         self.current_tetromino.draw()
      self.draw_boundaries()
      self.draw_score()
      self.draw_next_tetromino()
      stddraw.show(pause_duration)

   def draw_grid(self):
      for row in range(self.grid_height):
         for col in range(self.grid_width):
            if self.tile_matrix[row][col] is not None:
               self.tile_matrix[row][col].draw(Point(col, row))
               
      stddraw.setPenColor(self.line_color)
      stddraw.setPenRadius(self.line_thickness)
      start_x, end_x = -0.5, self.grid_width - 0.5
      start_y, end_y = -0.5, self.grid_height - 0.5
      
      for x in np.arange(start_x + 1, end_x, 1):
         stddraw.line(x, start_y, x, end_y)
      for y in np.arange(start_y + 1, end_y, 1):
         stddraw.line(start_x, y, end_x, y)
         
      stddraw.setPenRadius()

   def draw_boundaries(self):
      stddraw.setPenColor(self.boundary_color)
      stddraw.setPenRadius(self.box_thickness)
      pos_x, pos_y = -0.5, -0.5
      stddraw.rectangle(pos_x, pos_y, self.grid_width, self.grid_height)
      stddraw.setPenRadius()

   def draw_score(self):
      panel_center_x = self.grid_width + 3
      stddraw.setPenColor(Color(255, 255, 255))
      stddraw.setFontFamily('Arial')
      stddraw.setFontSize(18)
      stddraw.boldText(panel_center_x, self.grid_height - 2, 'SCORE')
      stddraw.setFontSize(16)
      stddraw.text(panel_center_x, self.grid_height - 3, str(self.score))

   def draw_next_tetromino(self):
      if self.next_tetromino is None:
         return

      panel_width = 6
      panel_center_x = self.grid_width + panel_width / 2
      stddraw.setPenColor(Color(255, 255, 255))
      stddraw.setFontFamily('Arial')
      stddraw.setFontSize(18)
      stddraw.boldText(panel_center_x, self.grid_height - 6, 'NEXT')

      tile_matrix = self.next_tetromino.tile_matrix
      n = len(tile_matrix)
      preview_x = self.grid_width + (panel_width - n) / 2
      preview_y = self.grid_height - 11
      for row in range(n):
         for col in range(n):
            if tile_matrix[row][col] is not None:
               position = Point()
               position.x = preview_x + col
               position.y = preview_y + (n - 1) - row
               tile_matrix[row][col].draw(position)

   def is_occupied(self, row, col):
      if not self.is_inside(row, col):
         return False
      return self.tile_matrix[row][col] is not None

   def is_inside(self, row, col):
      if row < 0 or row >= self.grid_height:
         return False
      if col < 0 or col >= self.grid_width:
         return False
      return True

   def merge_tiles(self):
      merged = False
      for col in range(self.grid_width):
         for row in range(self.grid_height - 1):
            lower_tile = self.tile_matrix[row][col]
            upper_tile = self.tile_matrix[row + 1][col]
            if lower_tile is not None and upper_tile is not None:
               if lower_tile.number == upper_tile.number:
                  lower_tile.number *= 2
                  lower_tile.update_color()
                  self.tile_matrix[row + 1][col] = None
                  self.score += lower_tile.number
                  merged = True
      return merged

   def drop_tiles(self):
      moved = False
      for col in range(self.grid_width):
         lowest_empty_row = 0
         for row in range(self.grid_height):
            if self.tile_matrix[row][col] is not None:
               if row != lowest_empty_row:
                  self.tile_matrix[lowest_empty_row][col] = self.tile_matrix[row][col]
                  self.tile_matrix[row][col] = None
                  moved = True
               lowest_empty_row += 1
      return moved

   def clear_full_lines(self):
      cleared = False
      row = 0
      while row < self.grid_height:
         row_is_full = True
         for col in range(self.grid_width):
            if self.tile_matrix[row][col] is None:
               row_is_full = False
               break

         if row_is_full:
            for col in range(self.grid_width):
               self.score += self.tile_matrix[row][col].number
            for shifted_row in range(row, self.grid_height - 1):
               for col in range(self.grid_width):
                  self.tile_matrix[shifted_row][col] = self.tile_matrix[shifted_row + 1][col]
            for col in range(self.grid_width):
               self.tile_matrix[self.grid_height - 1][col] = None
            cleared = True
         else:
            row += 1
      return cleared

   def handle_free_tiles(self):
      connected = np.full((self.grid_height, self.grid_width), False)
      stack = []

      for col in range(self.grid_width):
         if self.tile_matrix[0][col] is not None:
            connected[0][col] = True
            stack.append((0, col))

      while len(stack) > 0:
         row, col = stack.pop()
         neighbors = [(row - 1, col), (row + 1, col),
                      (row, col - 1), (row, col + 1)]
         for neighbor_row, neighbor_col in neighbors:
            if self.is_inside(neighbor_row, neighbor_col):
               if self.tile_matrix[neighbor_row][neighbor_col] is not None:
                  if not connected[neighbor_row][neighbor_col]:
                     connected[neighbor_row][neighbor_col] = True
                     stack.append((neighbor_row, neighbor_col))

      removed = False
      for row in range(self.grid_height):
         for col in range(self.grid_width):
            if self.tile_matrix[row][col] is not None and not connected[row][col]:
               self.score += self.tile_matrix[row][col].number
               self.tile_matrix[row][col] = None
               removed = True
      return removed

   def check_win(self):
      for row in range(self.grid_height):
         for col in range(self.grid_width):
            tile = self.tile_matrix[row][col]
            if tile is not None and tile.number >= 2048:
               self.won = True
      return self.won

   def process_merges(self):
      self.drop_tiles()
      while True:
         merged = self.merge_tiles()
         if not merged:
            break
         self.drop_tiles()

   def update_grid(self, tiles_to_lock, blc_position):
      self.current_tetromino = None
      n_rows, n_cols = len(tiles_to_lock), len(tiles_to_lock[0])
      for col in range(n_cols):
         for row in range(n_rows):
            if tiles_to_lock[row][col] is not None:
               pos = Point()
               pos.x = blc_position.x + col
               pos.y = blc_position.y + (n_rows - 1) - row
               if self.is_inside(pos.y, pos.x):
                  self.tile_matrix[pos.y][pos.x] = tiles_to_lock[row][col]
               else:
                  self.game_over = True
                  
      self.process_merges()
      self.clear_full_lines()
      free_tiles_removed = self.handle_free_tiles()
      
      if free_tiles_removed:
         self.process_merges()
         
      self.check_win()
      return self.game_over
