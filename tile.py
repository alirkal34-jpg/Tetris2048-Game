import random  
import lib.stddraw as stddraw  
from lib.color import Color  

class Tile:
   """
   Represents a single tile in the game grid.
   Each tile holds a specific value (e.g., 2, 4, 8) and updates its visual representation accordingly.
   """
   boundary_thickness = 0.004
   font_family, font_size = 'Arial', 16

   def __init__(self):
      self.number = random.choice([2, 4])
      self.update_color()

   def update_color(self):
      """
      Updates the background color of the tile based on its current number.
      The color palette gets progressively darker/warmer as the tile value increases.
      """
      if self.number == 2:
         self.background_color = Color(238, 228, 218)
      elif self.number == 4:
         self.background_color = Color(237, 224, 200)
      elif self.number == 8:
         self.background_color = Color(242, 177, 121)
      elif self.number == 16:
         self.background_color = Color(245, 149, 99)
      elif self.number == 32:
         self.background_color = Color(246, 124, 95)
      else:
         # Default color for higher values (64, 128, 256, etc.)
         self.background_color = Color(237, 207, 114)

      self.foreground_color = Color(0, 100, 200)
      self.box_color = Color(0, 100, 200)

   def draw(self, position, length=1):
      # Draw the filled background
      stddraw.setPenColor(self.background_color)
      stddraw.filledSquare(position.x, position.y, length / 2)
      
      # Draw the boundary box
      stddraw.setPenColor(self.box_color)
      stddraw.setPenRadius(Tile.boundary_thickness)
      stddraw.square(position.x, position.y, length / 2)
      stddraw.setPenRadius() # Reset pen radius
      
      # Draw the tile number
      stddraw.setPenColor(self.foreground_color)
      stddraw.setFontFamily(Tile.font_family)
      stddraw.setFontSize(Tile.font_size)
      stddraw.boldText(position.x, position.y, str(self.number))