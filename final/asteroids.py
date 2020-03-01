'''
This is Asteroids, a game in which you can pick up power ups and shoot/avoid enemies
to gain points and set new high scores!

Change log:
  - 0.0.5: Bullets move on left-mouse click
           Sorting enemies and bullets out now done by helper function
           Astronaut and enemies use different spawn timers
           New game over screen
           Added win condition; collecting 10 astronauts produces a victory condition
           Added a background for more flavor
  - 0.0.4: Bullets are now drown on left-mouse click, but do not move
  - 0.0.3: Added support for moving the spaceship via the keys W, A, S, and D
           The player model orients itself around the cursor while it's in the window
           Added support for drawing enemies
           Player can collide with enemies and the player and enemy models get replaced by an explosion
  - 0.0.2: Added support for handle_release
  - 0.0.1: Initial version
'''
__VERSION__ = '0.0.2'

import arcade, math, random
from cisc108_game import Cisc108Game

################################################################################
## Game Constants

WINDOW_WIDTH = 500
WINDOW_HEIGHT = 500
BACKGROUND_COLOR = arcade.color.BLACK
GAME_TITLE = "Asteroids!"

PLAYER = arcade.load_texture('player.png')
PLAYER_SIZE = 50
ENEMY = arcade.load_texture('foe.png')
ENEMY_SIZE = 50
DEATH = arcade.load_texture('pop.png')
ASTRONAUT = arcade.load_texture('astro.png')
GAME_OVER = arcade.load_texture('game over.png')
VICTORY = arcade.load_texture('win.png')

BULLET_SIZE = 10
BULLET = arcade.make_circle_texture(BULLET_SIZE, arcade.color.WHITE)
BULLET_SPEED = 10

CURSOR_SIZE = 10
SPAWN_TIMER = 100

BACKGROUND = arcade.load_texture('background.jpg')
################################################################################
## Record definitions

Position = {
    # A position is an X/Y coordinate pair.
    'x': float,
    'y': float
}

Bullet = {
    # The position of the bullet when it is fired
    'current': Position,
    # Position that the bullet is moving to
    'goal': Position
    }

Enemy = {
    # Whether or not the enemy is alive
    'alive?':bool,
    # The current position of the enemy
    'current':Position,
    # The goal position of the enemy (should chase the player)
    'goal':Position}

World = {
    'player':{
        # Whether or not the player is still alive
        'alive?': bool,
        # x and y coordinates of the player
        'location': Position,
        # Whether or not the player is moving
        'moving?': bool,
        # What direction the player is moving in
        'direction': str,
        # The angle at which the player is facing
    },
    # List of enemies that are in the world
    'enemies':[Enemy],
    # The astronaut that the player is trying to save
    'astronaut': {'saved?':bool,
                  'location': Position},
    # Position of the cursor
    'mouse':Position,
    # The current score
    'score': int,
    # List of bullets in the world
    'bullets':[Bullet],
    # Spawn/move timer for the astronaut
    'astronaut timer': int,
    # Spawn timer for enemies
    'enemy timer': int}

INITIAL_WORLD = {
    'player':{'alive?': True,
              'location':{'x': WINDOW_WIDTH / 2,
                          'y': WINDOW_HEIGHT / 2,},
              'moving?': False,
              'direction': ''},
    'enemies':[],
    'astronaut':{'saved?': False,
                'location':{'x': WINDOW_WIDTH - 100,
                            'y': WINDOW_HEIGHT - 75}},
    'mouse':{'x': WINDOW_WIDTH / 2,
             'y': WINDOW_HEIGHT / 2},
    'score': 0,
    'bullets':[],
    'astronaut timer': SPAWN_TIMER,
    'enemy timer': SPAWN_TIMER
}

################################################################################
# Helper Functions
def make_random_position() -> Position:
    '''
    Produce a new random position (random X/Y coordinate) within the
    bounds of the window.
    
    Returns:
        Position: The new random position.
    '''
    return {
        'x': random.randint(0, WINDOW_WIDTH),
        'y': random.randint(0, WINDOW_HEIGHT)
    }

def angle_between(p1: Position, p2: Position) -> float:
    '''
    Uses trigonometry to determine the angle (in radians) between
    two points. The result ranges from pi to -pi radians (which would be
    180 degrees and negative 180 degrees).
    
    Args:
        p1 (Position): The origin position
        p2 (Position): The target position
    Returns:
        float: The angle in radians between the origin and the target.
    '''
    return math.atan2(p2['y']-p1['y'], p2['x']-p1['x'])

def distance_between(p1: Position, p2: Position) -> float:
    '''
    Uses algebra to determine the distance between two points.
    
    Args:
        p1 (Position): The origin position
        p2 (Position): The target position
    Returns:
        float: The distance in pixels between the two points.
    '''
    return math.sqrt((p2['y']-p1['y'])**2+(p2['x']-p1['x'])**2)

def hit_detection(p1: Position, p2: Position, model_size) -> bool:
    '''
    Determines if two models at two positions are colliding with one another.
    
    Args:
        p1 (Position): The first models position
        p2 (Position): The second models position.
    Returns:
        bool: Whether the player is hitting the enemy
    '''
    return distance_between(p1, p2) < model_size

def x_from_angle_speed(angle: float, speed: float) -> float:
    """
    Determines the new X-coordinate when you move `speed` pixels
    in the `angle` direction. The angle is in radians.
    
    Args:
        angle (float): The angle to move in radians.
        speed (float): The number of pixels to move in that direction.
    Returns:
        float: The horizontal distance traveled
    """
    return math.cos(angle) * speed

def y_from_angle_speed(angle: float, speed: float) -> float:
    """
    Determines the new Y-coordinate when you move `speed` pixels
    in the `angle` direction. The angle is in radians.
    
    Args:
        angle (float): The angle to move in radians.
        speed (float): The number of pixels to move in that direction.
    Returns:
        float: The vertical distance traveled
    """
    return math.sin(angle) * speed

def make_bullet(world: World) -> Bullet:
    '''
    Produces a new bullet with the current position set to where the
    player is and the goal position set to where the mouse was.
    
    args:
        world (World): The current world.
    
    Returns:
        Bullet: the new bullet.
    '''
    current_x = world['player']['location']['x']
    current_y = world['player']['location']['y']
    goal_x = world['mouse']['x']
    goal_y = world['mouse']['y']
    
    return {
        'current':{'x':current_x, 'y':current_y},
        'goal': {'x':goal_x, 'y':goal_y}
    }

def move_bullet(bullet: Bullet):
    '''
    Moves the bullet towards its goal position.
    
    Args:
        bullet (Bullet): The bullet to be moving.
    '''
    angle = angle_between(bullet['current'], bullet['goal'])
    bullet['current']['x'] += x_from_angle_speed(angle, BULLET_SPEED)
    bullet['current']['y'] += y_from_angle_speed(angle, BULLET_SPEED)

def make_enemy(world: World) -> Enemy:
    '''
    Produces a new enemy to be added to the list of enemies in
    the world. Each enemy has a value indicating whether or not
    it is alive (bool), and current and goal positions.
    
    args:
        world (World): The current world.
    
    Returns:
        Enemy: the new enemy.
    '''
    position = make_random_position()
    x = position['x']
    y = position['y']
    goal_x = world['player']['location']['x']
    goal_y = world['player']['location']['y']
    
    return {
        'alive?': True,
        'current':{'x':x, 'y':y},
        'goal': {'x':goal_x, 'y':goal_y}
    }

def move_enemy(enemy: Enemy):
    '''
    Moves the enemy towards its goal position, which is also
    where the player was when the enemy was either spawned
    or redirected after hitting it's last goal position.
    
    Args:
        enemy (Enemy): The enemy to be moving.
    '''
    angle = angle_between(enemy['current'], enemy['goal'])
    enemy['current']['x'] += x_from_angle_speed(angle, 3)
    enemy['current']['y'] += y_from_angle_speed(angle, 3)
    
def sort_enemies_and_bullets(world: World):
    '''
    Removes enemies that have been hit by bullets and bullets that
    have hit enemies from the world.
    
    args:
        world (World): The current world.
    '''
    bullet_removal = []
    for enemy in world['enemies']:
        for bullet in world['bullets']:
            if hit_detection(enemy['current'], bullet['current'], ENEMY_SIZE) and bullet not in bullet_removal:
                bullet_removal.append(bullet)
    
    enemy_removal = []
    for bullet in world['bullets']:
        for enemy in world['enemies']:
            if hit_detection(enemy['current'], bullet['current'], ENEMY_SIZE) and enemy not in enemy_removal:
                enemy_removal.append(enemy)
                
    kept_enemies = []
    for enemy in world['enemies']:
        if enemy not in enemy_removal and enemy not in kept_enemies:
            kept_enemies.append(enemy)
            
    kept_bullets = []
    for bullet in world['bullets']:
        if bullet not in bullet_removal and bullet not in kept_bullets:
            kept_bullets.append(bullet)
    
    world['enemies'] = kept_enemies
    world['bullets'] = kept_bullets
    
################################################################################
# Drawing functions

def draw_score(score: int):
    '''
    Draw the given score in the bottom-left corner.
    
    Args:
        score (int): The score to draw.
    '''
    arcade.draw_text(str(score), 0, 0, arcade.color.WHITE, 20)
    
def draw_bullet(world: World):
    '''
    Draws each bullet from the world's list of bullets on the
    game window.
    
    Args:
        world (World): The current world.
    '''
    for bullet in world['bullets']:
        arcade.draw_texture_rectangle(bullet['current']['x'], bullet['current']['y'],
                                  BULLET_SIZE, BULLET_SIZE, BULLET)
    
def draw_enemy(world: World):
    '''
    Draws each enemy that's in the world's list of enemies.
    Also orients the enemies to face the player's position
    at all times.
    
    Args:
        world (World): The current world.
    '''
    for enemy in world['enemies']:
        angle = angle_between(enemy['current'], world['player']['location'])
        angle = math.degrees(angle)
        arcade.draw_texture_rectangle(enemy['current']['x'], enemy['current']['y'],
                                ENEMY.width/2, ENEMY.height/2, ENEMY, angle)

def draw_world(world: World):
    """
    Draws the background graphic, the player model as it moves around and
    spins to face the cursor position, the enemies in the world's list of
    enemies, the bullets in the world's list of bullets, the astronaut, and
    the score. It also draws the loss and win condition graphics.
    
    Args:
        world (World): The current world to draw
    """
    arcade.draw_texture_rectangle(WINDOW_WIDTH/2, WINDOW_HEIGHT/2, BACKGROUND.width, BACKGROUND.height, BACKGROUND)
    
    if world['player']['alive?']:
        angle = angle_between(world['mouse'], world['player']['location'])
        angle = math.degrees(angle)
        arcade.draw_texture_rectangle(world['player']['location']['x'], world['player']['location']['y'],
                                      PLAYER.width/2, PLAYER.height/2, PLAYER, angle)
        
    if not world['astronaut']['saved?'] and world['astronaut timer'] > 0:
        arcade.draw_texture_rectangle(world['astronaut']['location']['x'], world['astronaut']['location']['y'],
                                      ASTRONAUT.width/5, ASTRONAUT.height/5, ASTRONAUT)
    
    if not world['player']['alive?']:
        arcade.draw_texture_rectangle(world['player']['location']['x'], world['player']['location']['y'],
                                      DEATH.width/3, DEATH.height/3, DEATH)
        arcade.draw_texture_rectangle(WINDOW_WIDTH/2, WINDOW_HEIGHT/2, GAME_OVER.width, GAME_OVER.height, GAME_OVER)
    
    if world['score'] == 10:
        arcade.draw_texture_rectangle(WINDOW_WIDTH/2, WINDOW_HEIGHT/2,
                                      VICTORY.width, VICTORY.height, VICTORY)
    
    for enemy in world['enemies']:
        draw_enemy(world)
        
    for bullet in world['bullets']:
        draw_bullet(world)
    
    draw_score(world['score'])
    
################################################################################
# World manipulating functions

def update_world(world: World):
    """
    Makes control input changes and checks for win/loss and other key conditions within
    the game world. Keeps the player from moving outside of the window, moves the player
    model around the game world, updates the score, checks for and moves enemies and bullets,
    and counts down the spawn timers for enemies and the astronaut.
    
    Args:
        world (World): The current world to update.
    """
    if not world['player']['alive?']:
        world['astronaut']['location'] = {'x':-10000, 'y':-10000}
        
    if world['player']['moving?'] and world['player']['alive?']:
        if world['player']['direction'] == 'up':
            world['player']['location']['y'] += 7
        if world['player']['direction'] == 'left':
            world['player']['location']['x'] -= 7
        if world['player']['direction'] == 'down':
            world['player']['location']['y'] -= 7
        if world['player']['direction'] == 'right':
            world['player']['location']['x'] += 7
   
    if world['player']['location']['x'] <= 30 or world['player']['location']['x'] >= 470 or world['player']['location']['y'] <= 30 or world['player']['location']['y'] >= 470:
        world['player']['moving?'] = False
    
    if world['astronaut']['saved?']:
        world['astronaut']['location'] = make_random_position()
        world['astronaut']['saved?'] = False
        
    if hit_detection(world['player']['location'], world['astronaut']['location'], PLAYER_SIZE):
        world['astronaut']['saved?'] = True
        world['score'] += 1
        
    for enemy in world['enemies']:
        move_enemy(enemy)
        if hit_detection(enemy['current'], world['player']['location'], PLAYER_SIZE):
            world['player']['alive?'] = False
            world['player']['moving?'] = False
            world['bullets'] = []
            world['enemies'] = []
            world['astronaut timer'] = 300000
            world['enemy timer'] = 300000
            
    for enemy in world['enemies']:
        if hit_detection(enemy['current'], enemy['goal'], ENEMY_SIZE):
            enemy['goal'] = world['player']['location']
     
    for bullet in world['bullets']:
        move_bullet(bullet)
        if hit_detection(bullet['current'], bullet['goal'], BULLET_SIZE):
            world['bullets'].remove(bullet)
    
    if world['player']['alive?']:
        if world['enemy timer'] > 0:
            world['enemy timer'] -= 1
        if world['enemy timer'] == 0:
            world['enemies'].append(make_enemy(world))
            world['enemy timer'] = 100
        if world['astronaut timer'] > 0:
            world['astronaut timer'] -= 1
        if world['astronaut timer'] == 0:
            world['astronaut']['location'] = make_random_position()
            world['astronaut timer'] = 300
    
    if world['score'] == 10:
        world['player']['alive?'] = False
        world['player']['moving?'] = False
        world['bullets'] = []
        world['enemies'] = []
        world['astronaut timer'] = 300000
        world['enemy timer'] = 3000000
            
    sort_enemies_and_bullets(world)
            
def handle_key(world: World, key: int):
    """
    The games uses standard WASD controls: W moves the player upward,
    A moves the player left, S moves the player down, and D moves the
    player right.
    
    Args:
        world (World): Current state of the world.
        key (int): The ASCII value of the pressed keyboard key (use ord and chr).
    """
    if chr(key) == 'w' or chr(key) == 'a' or chr(key) == 's' or chr(key) == 'd':
        world['player']['moving?'] = True
        
    if chr(key) == 'w':
        world['player']['direction'] = 'up'
    elif chr(key) == 'a':
        world['player']['direction'] = 'left'
    elif chr(key) == 's':
        world['player']['direction'] = 'down'
    elif chr(key) == 'd':
        world['player']['direction'] = 'right'
            
            
def handle_mouse(world: World, x: int, y: int, button: str):
    """
    When the left mouse button is clicked, the game will create a bullet and add it
    the list of bullets within the game world so it can be drawn, moved, and collide
    with enemies.
    
    Args:
        world (World): Current state of the world.
        x (int): The x-coordinate of the mouse when the button was clicked.
        y (int): The y-coordinate of the mouse when the button was clicked.
        button (str): The button that was clicked ('left', 'right', 'middle')
    """
    if button == 'left':
        world['bullets'].append(make_bullet(world))
    
def handle_motion(world: World, x: int, y: int):
    """
    The player model will alway face towards the cursor while it is on the game
    window. The player is still free to move about as they please but this will
    determine where they are aiming.
    
    Args:
        world (World): Current state of the world.
        x (int): The x-coordinate of where the mouse was moved to.
        y (int): The y-coordinate of where the mouse was moved to.
    """
    angle = angle_between(world['mouse'], world['player']['location'])
    angle = math.degrees(angle)
    world['mouse']['x'] = x
    world['mouse']['y'] = y
    
def handle_release(world: World, key: int):
    """
    If the key being pressed isn't a movement key (W, A, S, D) the player model will
    not move.
    
    Args:
        world (World): Current state of the world.
        key (int): The ASCII value of the released keyboard key (use ord and chr).
    """
    if chr(key) != 'w' or chr(key) != 'a' or chr(key) != 's' or chr(key) != 'd':
        world['player']['moving?'] = False
        
############################################################################
# Set up the game
# Don't need to change any of this

if __name__ == '__main__':
    Cisc108Game(World, WINDOW_WIDTH, WINDOW_HEIGHT, GAME_TITLE, INITIAL_WORLD,
                draw_world, update_world, handle_key, handle_mouse,
                handle_motion, handle_release)
    arcade.set_background_color(BACKGROUND_COLOR)
    arcade.run()
