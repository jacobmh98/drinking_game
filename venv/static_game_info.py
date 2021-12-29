import pygame

# static game info
row_space = 15
tile_size = 70
start_left = 20
screen_width = 1920
screen_height = 1080

# stomp delta value
delta = 2.0

rules = ["- Each player is assigned in a line randomly",
          "- In each round move forward one plate by pressing arrow up or down",
          "- Half of the plates will break (50% chance), and when a player steps on these he will die",
          "- All dead players must at the end take a shot",
          "- A player can sabotage himself and everyone following him by stomping on a plate until it",
          "  breaks by pressing space. The consequence of doing this is you must drink the cocktail,",
          "  that can be defined with the ingredients below.",
          "  For example the first player can make everyone take a shot by stomping on the first plate,",
          "  however then he must drink the cocktail :)"]

# initialize pygame and create the screen
pygame.init()
#x, y = screen.get_size()
#start_top = y/2 - 80
#pygame.display.set_caption("TCD game with Jelly Beans")

# input box
input_box = pygame.Rect(20, 360, 600, 30)
color_input_box = pygame.Color("white")
text = "tabasco, vodka, whiskey, mayonnaise"

# name registration
name_box = pygame.Rect(20, 70, 400, 30)
name = ""

# background
background = pygame.image.load("bg.jpg")
background = pygame.transform.scale(background, (1920, 1080))
running = True

# defining fonts
header = pygame.font.Font("freesansbold.ttf", 30)
font = pygame.font.Font("freesansbold.ttf", 15)
typing = pygame.font.Font("freesansbold.ttf", 15)

# button
button_width = 100
button_height = 40
button = pygame.Rect(20, 350, button_width, button_height)
button_color_light = (255, 255, 255)
button_color_dark = (255, 0, 0)
button_text = "Let's go!!!"
button_active = 2

# player info
playerImg = pygame.image.load("ninja.png")
playerImg = pygame.transform.scale(playerImg, (55, 55))
