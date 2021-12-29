import random
import pygame

from static_game_info import *

# class for dynamic game info
class Game:
    def __init__(self):
        # game info
        self.txt_surface = None
        self.turn = 0
        self.phase = 1
        self.screen = pygame.display.set_mode((700,600))
        self.current_row = -1
        self.stomp = ""
        self.stomp_height = 0
        self.winners = []
        self.losers = []
        self.funny_guy = None
        self.ingredients = ""

        # tiles info
        self.start_tiles = []
        self.end_tiles = []
        self.tiles = []

        # player info
        self.players = []
        self.someoneDied = False
        self.finishedPlayers = 0
        self.names = []
        self.num_players = 0

# class for tile objects
class Tile:
    active = True
    size = 70

    def __init__(self, left, top, row, danger):
        self.left = left
        self.top = top
        self.row = row
        self.danger = danger

# class for player objects
class Player:
    def __init__(self, name, id):
        self.dead = False
        self.finished = False
        self.name = name
        self.id = id
        self.current_tile = None

    def set_start(self, left, top):
        self.x = left
        self.y = top

# initializing game object
game = Game()

# draw start screen
def draw_start():
    pygame.display.set_caption("Game Rules")
    game.screen.fill((0, 0, 0))
    game.screen.blit(header.render("These are the rules", True, (255, 0, 0)), (20, 20))
    for i, rule in enumerate(rules):
        if rule[0] == '-':
            game.screen.blit(font.render(rule, True, (255, 0, 0)), (20, 20 + (i + 1) * 30))
        else:
            game.screen.blit(font.render(rule, True, (255, 0, 0)), (20, 20 + (i + 1) * 30))
    game.screen.blit(
        font.render("Write ingredients for the delicious cocktail. Press enter when done!", True, (255, 0, 0)),
        (20, 330))
    pygame.draw.rect(game.screen, color_input_box, input_box, 2)
    game.txt_surface = typing.render(text, True, color_input_box)
    game.screen.blit(game.txt_surface, (input_box.x + 5, input_box.y + 5))
    pygame.display.update()

# draw individual player
def draw_player(p):
    name = font.render(p.name, True, (0, 255, 0))
    game.screen.blit(playerImg, (p.x,p.y))
    game.screen.blit(name, (p.x + 5, p.y + 55))

# draw register screen
def draw_register():
    pygame.display.set_caption("Register Players")
    game.screen.fill((0, 0, 0))
    game.screen.blit(header.render("Write player and press enter (max 12 players)", True, (255, 0, 0)), (20, 20))
    pygame.draw.rect(game.screen, color_input_box, name_box, 2)
    game.txt_surface = typing.render(name, True, color_input_box)
    game.screen.blit(game.txt_surface, (name_box.x + 5, name_box.y + 5))

    for p in game.players:
        draw_player(p)

    pygame.draw.rect(game.screen, button_color_light, button, button_active)
    game.txt_surface = typing.render(button_text, True, button_color_dark)
    game.screen.blit(game.txt_surface, (button.x + 10, button.y + 10))

    pygame.display.update()

# method for registering new player
def register_player(n):
    if game.num_players < 12 and len(n) > 0:
        p = Player(n, game.num_players)
        if p.id == 0 or p.id == 6:
            p.x = 20
        else:
            p.x = (p.id % 6) * (tile_size+40)
        if game.num_players <= 5:
            p.y = 150
        else:
            p.y = 250
        game.players.append(p)
        game.num_players += 1

        return True
    return False

def draw_game():
    game.screen.fill((0, 0, 0))
    game.screen.blit(background, (0,0))

    # print start tiles
    for tile in game.start_tiles:
        pygame.draw.rect(game.screen, (255, 0, 0), pygame.Rect(tile.left, tile.top, tile.size, tile.size))

    # print game tiles
    for tile in game.tiles:
        if tile[0].active:
            pygame.draw.rect(game.screen, (255, 0, 0), pygame.Rect(tile[0].left, tile[0].top, tile[0].size, tile[0].size))
        if tile[1].active:
            pygame.draw.rect(game.screen, (255, 0, 0), pygame.Rect(tile[1].left, tile[1].top, tile[1].size, tile[1].size))

    # print end tiles
    for tile in game.end_tiles:
        pygame.draw.rect(game.screen, (255, 0, 0), pygame.Rect(tile.left, tile.top, tile.size, tile.size))

    # print alive players
    for p in game.players:
        if not p.dead:
            draw_player(p)

    # delay when someones dies
    if game.someoneDied:
        delay()
        game.someoneDied = False

    pygame.display.update()

# method delaying game with 100 ms
def delay():
    pygame.time.wait(100)

# method to reset game
def reset():
    game.finishedPlayers = 0
    game.turn = 0
    game.current_row = -1
    game.winners = []
    game.losers = []
    game.funny_guy = None
    game.someoneDied = False

    # reset players
    for p in game.players:
        p.dead = False
        p.finished = False
        p.current_tile = None

    random.shuffle(game.players)

    # tiles info
    game.start_tiles = []
    game.end_tiles = []
    game.tiles = []


def initialize_game():
    game.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    game.phase = 3

    # reset game info
    reset()

    screen_width = pygame.display.Info().current_w
    screen_height = pygame.display.Info().current_h
    start_top = screen_height / 2 - tile_size

    # initialize start tiles
    for i in range(6):
        for j in range(0, 2):
            game.start_tiles.append(
                Tile(start_left + tile_size * j,
                     (screen_height - 420) / 2 + tile_size * i, 0, -1))

    # initialize players
    for i in range(game.num_players):
        tile = game.start_tiles[i]
        game.players[i].set_start(tile.left, tile.top)

    # initialize game tiles
    for row in range(0, game.num_players):
        r = random.randint(0, 9)
        game.tiles.append([Tile(start_left + ((tile_size + 15) * (row + 2)), start_top, row, r <= 4),
                           Tile(start_left + ((tile_size + 15) * (row + 2)), start_top + tile_size + 15, row, r > 4)])

    # initialize end tiles
    for i in range(6):
        for j in range(0, 2):
            game.end_tiles.append(
                Tile(start_left + (game.num_players + 2) * (tile_size + 15) + tile_size * j,
                     (screen_height - 420) / 2 + tile_size * i, 0, -1))

# method for moving player on event
def move_player(dir):
    player = game.players[game.turn]
    if game.current_row + 1 == game.num_players:
        player.x = game.end_tiles[game.finishedPlayers].left
        player.y = game.end_tiles[game.finishedPlayers].top
        player.finished = True
        game.finishedPlayers += 1
        game.turn += 1
        game.current_row = -1
        game.winners.append(player)
        return

    row_tiles = game.tiles[game.current_row + 1]

    if dir == "up":
        player.x = row_tiles[0].left
        player.y = row_tiles[0].top

        if row_tiles[0].danger:
            row_tiles[0].active = False
            player.dead = True
            game.turn += 1
            game.current_row = -1
            game.someoneDied = True
            game.losers.append(player)
        else:
            player.current_tile = row_tiles[0]
            game.current_row += 1
    elif dir == "down":
        player.x = row_tiles[1].left
        player.y = row_tiles[1].top

        if row_tiles[1].danger:
            row_tiles[1].active = False
            player.dead = True
            game.turn += 1
            game.current_row = -1
            game.someoneDied = True
            game.losers.append(player)
        else:
            player.current_tile = row_tiles[1]
            game.current_row += 1

# method for game over screen
def draw_game_over():
    pygame.display.set_caption("Vodka Time")
    game.screen.fill((0, 0, 0))

    game.screen.blit(header.render("The losers, take a shot", True, (255, 0, 0)), (20, 20))
    for i, p in enumerate(game.losers):
        p.x = 60 + (i % 6) * (tile_size)

        if i <= 5:
            p.y = 70
        else:
            p.y = 150
        draw_player(p)

    game.screen.blit(header.render("The Survivors!", True, (255, 0, 0)), (20, 220))
    for i, p in enumerate(game.winners):

        p.x = 60 + (i % 6) * (tile_size)

        if i <= 5:
            p.y = 280
        else:
            p.y = 350
        draw_player(p)

    if game.funny_guy is not None:
        game.screen.blit(header.render("The Funny Guy!", True, (255, 0, 0)), (20, 440))
        p = game.funny_guy
        p.x = 20
        p.y = 480
        draw_player(p)
        game.screen.blit(font.render("Enjoy your cocktail with", True, (255, 0, 0)), (20, 560))
        game.screen.blit(font.render(game.ingredients, True, (255, 0, 0)), (20, 580))
    game.screen.blit(header.render("Press space to repeat game", True, (255, 0, 0)), (20, 600))

    pygame.display.update()

while running:
    # get mouse position
    mouse_pos = pygame.mouse.get_pos()

    # determine which phase to draw
    if game.phase == 1:
        draw_start()
    elif game.phase == 2:
        draw_register()
        # check if mouse is inside button
        if button.x <= mouse_pos[0] <= button.x + button_width and \
                button.y <= mouse_pos[1] <= button.y + button_height:
            button_active = 0
        else:
            button_active = 2
    elif game.phase == 3:
        draw_game()
    else:
        game.screen = pygame.display.set_mode((700, 700))
        draw_game_over()


    # check for game over
    if game.turn >= game.num_players and game.phase == 3:
        game.phase += 1

    # animate stomp action
    if game.stomp == "up":
        game.players[game.turn].y -= delta
        game.stomp_height += delta

        if game.stomp_height >= 10:
            game.stomp = "down"
    if game.stomp == "down":
        game.players[game.turn].y += delta
        game.stomp_height -= delta

        if game.stomp_height <= 0:
            game.stomp = ""

            if game.current_row != -1 and game.current_row != game.num_players:
                player = game.players[game.turn]
                player.current_tile.active = False
                player.current_tile.danger = True
                player.dead = True
                game.turn += 1
                game.current_row = -1
                game.someoneDied = True
                game.losers.append(player)
                if game.funny_guy is None:
                    game.funny_guy = player

    # game events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            # check for player movement event
            if game.phase == 3:
                if event.key == pygame.K_UP:
                   move_player("up")
                elif event.key == pygame.K_DOWN:
                    move_player("down")
                elif event.key == pygame.K_SPACE:
                        game.stomp = "up"

            if game.phase == 4 and event.key == pygame.K_SPACE:
                initialize_game()

            # check for typing events
            if event.key == pygame.K_RETURN:
                if game.phase == 1:
                    game.phase += 1
                    game.ingredients = text
                elif game.phase == 2:
                    if register_player(name):
                        name = ''
            elif event.key == pygame.K_BACKSPACE:
                if game.phase == 1:
                    text = text[:-1]
                elif game.phase == 2:
                    name = name[:-1]
            else:
                if game.phase == 1:
                    if game.txt_surface.get_width() <= 590:
                        text += event.unicode
                elif game.phase == 2:
                    if game.txt_surface.get_width() <= 390:
                        name += event.unicode

        # check for mouse events
        if event.type == pygame.MOUSEBUTTONDOWN:
            if game.phase == 2 and event.button == 1 and button_active == 0:
                initialize_game()