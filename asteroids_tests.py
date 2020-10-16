'''
Tests for my CISC108 final project.

Change log:
  - 0.0.4: Added tests for world manipulation functions
  - 0.0.3: Added tests for helper functions
  - 0.0.2: Fixed typo with assert_equal
  - 0.0.1: Initial version
'''

__VERSION__ = '0.0.2'

from cisc108 import assert_equal
from cisc108_game import assert_type

################################################################################
# Game import
# Rename this to the name of your project file.
from asteroids import *

################################################################################
## Testing helper functions
# Testing make_random_position()
random.seed(0)

for i in range(4):
    point = make_random_position()
    # Test the function produces values in the expected range
    assert_equal(0 <= point['x'] <= WINDOW_WIDTH, True)
    assert_equal(0 <= point['y'] <= WINDOW_HEIGHT, True)

# Testing angle_between()
ORIGIN = {'x': 0, 'y': 0}
TOP_RIGHT = {'x': WINDOW_WIDTH, 'y': WINDOW_HEIGHT}
TOP_LEFT = {'x': 0, 'y': WINDOW_HEIGHT}
BOTTOM_RIGHT = {'x': WINDOW_WIDTH, 'y': 0}
CENTER = {'x': WINDOW_WIDTH/2, 'y': WINDOW_HEIGHT/2}
CENTER_LEFT = {'x': 0, 'y': WINDOW_HEIGHT/2}
CENTER_RIGHT = {'x': WINDOW_WIDTH, 'y': WINDOW_HEIGHT/2}
CENTER_BOTTOM = {'x': WINDOW_WIDTH/2, 'y': 0}
CENTER_TOP = {'x': WINDOW_WIDTH/2, 'y': WINDOW_HEIGHT}
assert_equal(angle_between(CENTER, TOP_RIGHT), math.pi/4)
assert_equal(angle_between(CENTER, CENTER_TOP), math.pi/2)
assert_equal(angle_between(CENTER, TOP_LEFT), 3*math.pi/4)
assert_equal(angle_between(CENTER, CENTER_LEFT), math.pi)
assert_equal(angle_between(CENTER, ORIGIN), -3*math.pi/4)
assert_equal(angle_between(CENTER, CENTER_BOTTOM), -math.pi/2)
assert_equal(angle_between(CENTER, BOTTOM_RIGHT), -math.pi/4)
assert_equal(angle_between(CENTER, CENTER_RIGHT), 0.0)

# Testing distance_between
# Cardinal directions from center
assert_equal(distance_between(CENTER, TOP_RIGHT), math.sqrt(125000))
assert_equal(distance_between(CENTER, CENTER_TOP), 250.0)
assert_equal(distance_between(CENTER, TOP_LEFT), math.sqrt(125000))
assert_equal(distance_between(CENTER, CENTER_LEFT), 250.0)
assert_equal(distance_between(CENTER, ORIGIN), math.sqrt(125000))
assert_equal(distance_between(CENTER, CENTER_BOTTOM), 250.0)
assert_equal(distance_between(CENTER, BOTTOM_RIGHT), math.sqrt(125000))
assert_equal(distance_between(CENTER, CENTER_RIGHT), 250.0)
# And also some weirder angles
assert_equal(distance_between(CENTER_LEFT, BOTTOM_RIGHT), math.sqrt(312500))
assert_equal(distance_between(ORIGIN, TOP_RIGHT), math.sqrt(500000))
# And a classic Pythagorean Triple
assert_equal(distance_between(ORIGIN, {'x': 3, 'y': 4}), 5.0)

# Testing hit_detection()
MODEL_SIZE = 50
FIRST_POSITION = {'x': 50, 'y': 50}
SECOND_POSITION = {'x': 60, 'y': 60}
THIRD_POSITION = {'x': 70, 'y': 70}
assert_equal(hit_detection(FIRST_POSITION, FIRST_POSITION, MODEL_SIZE), True)
assert_equal(hit_detection(FIRST_POSITION, SECOND_POSITION, MODEL_SIZE), True)
assert_equal(hit_detection(FIRST_POSITION, THIRD_POSITION, MODEL_SIZE), True)
assert_equal(hit_detection(SECOND_POSITION, THIRD_POSITION, MODEL_SIZE), True)

## Testing x_from_angle_speed
assert_equal(x_from_angle_speed(0, 5), 5.0)
assert_equal(x_from_angle_speed(math.pi/3, 5), 2.5)
assert_equal(x_from_angle_speed(math.pi/2, 5), 0.0)
assert_equal(x_from_angle_speed(2*math.pi/3, 5), -2.5)
assert_equal(x_from_angle_speed(math.pi, 5), -5.0)
assert_equal(x_from_angle_speed(-math.pi/3, 5), 2.5)
assert_equal(x_from_angle_speed(-math.pi/2, 5), 0.0)
assert_equal(x_from_angle_speed(-2*math.pi/3, 5), -2.5)

## Testing y_from_angle_speed
assert_equal(y_from_angle_speed(0, 5), 0.0)
assert_equal(y_from_angle_speed(math.pi/6, 5), 2.5)
assert_equal(y_from_angle_speed(math.pi/2, 5), 5.0)
assert_equal(y_from_angle_speed(5*math.pi/6, 5), 2.5)
assert_equal(y_from_angle_speed(math.pi, 5), 0.0)
assert_equal(y_from_angle_speed(-math.pi/6, 5), -2.5)
assert_equal(y_from_angle_speed(-math.pi/2, 5), -5.0)
assert_equal(y_from_angle_speed(-5*math.pi/6, 5), -2.5)

## Testing move_bullet
ORIGIN = {'x': 0, 'y': 0}
CENTER = {'x': WINDOW_WIDTH/2, 'y': WINDOW_HEIGHT/2}
CENTER_RIGHT = {'x': WINDOW_WIDTH, 'y': WINDOW_HEIGHT/2}
GOAL_POSITION = {'x': 3, 'y': 4}
MOVING_BULLET = {'current': ORIGIN, 'goal': GOAL_POSITION}
move_bullet(MOVING_BULLET)
assert_equal(MOVING_BULLET['current']['x'], 6.000000000000001)
assert_equal(MOVING_BULLET['current']['y'], 7.999999999999999)
move_bullet(MOVING_BULLET)
assert_equal(MOVING_BULLET['current']['x'], -8.881784197001252e-16)
assert_equal(MOVING_BULLET['current']['y'], 8.881784197001252e-16)
move_bullet(MOVING_BULLET)
assert_equal(MOVING_BULLET['current']['x'], 6.000000000000001)
assert_equal(MOVING_BULLET['current']['y'], 7.999999999999999)
move_bullet(MOVING_BULLET)
assert_equal(MOVING_BULLET['current']['x'], -8.881784197001252e-16)
assert_equal(MOVING_BULLET['current']['y'], 8.881784197001252e-16)
move_bullet(MOVING_BULLET)
assert_equal(MOVING_BULLET['current']['x'], 6.000000000000001)
assert_equal(MOVING_BULLET['current']['y'], 7.999999999999999)

## Testing make_bullet
WORLD = {
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
assert_equal(make_bullet(WORLD), {'current': {'x': 250.0, 'y': 250.0}, 'goal': {'x': 250.0, 'y': 250.0}})
NEW_WORLD = {
    'player':{'alive?': True,
              'location':{'x': 374,
                          'y': 123,},
              'moving?': False,
              'direction': ''},
    'enemies':[],
    'astronaut':{'saved?': False,
                'location':{'x': WINDOW_WIDTH - 100,
                            'y': WINDOW_HEIGHT - 75}},
    'mouse':{'x': 101,
             'y': 420},
    'score': 0,
    'bullets':[],
    'astronaut timer': SPAWN_TIMER,
    'enemy timer': SPAWN_TIMER
}
assert_equal(make_bullet(NEW_WORLD), {'current': {'x': 374, 'y': 123}, 'goal': {'x': 101, 'y': 420}})

## Testing make_enemy
WORLD = {
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
assert_equal(make_enemy(WORLD), {'alive?': True, 'current': {'x': 261, 'y': 248}, 'goal': {'x': 250.0, 'y': 250.0}})
NEW_WORLD = {
    'player':{'alive?': True,
              'location':{'x': 374,
                          'y': 123,},
              'moving?': False,
              'direction': ''},
    'enemies':[],
    'astronaut':{'saved?': False,
                'location':{'x': WINDOW_WIDTH - 100,
                            'y': WINDOW_HEIGHT - 75}},
    'mouse':{'x': 101,
             'y': 420},
    'score': 0,
    'bullets':[],
    'astronaut timer': SPAWN_TIMER,
    'enemy timer': SPAWN_TIMER
}
assert_equal(make_enemy(WORLD), {'alive?': True, 'current': {'x': 207, 'y': 470}, 'goal': {'x': 250.0, 'y': 250.0}})

## Testing move_enemy
ENEMY = {'alive?': True, 'current':{'x': 400, 'y':23}, 'goal':{'x':133, 'y':123}}
ORIGIN = {'x': 0, 'y': 0}
CENTER = {'x': WINDOW_WIDTH/2, 'y': WINDOW_HEIGHT/2}
CENTER_RIGHT = {'x': WINDOW_WIDTH, 'y': WINDOW_HEIGHT/2}
GOAL_POSITION = {'x': 3, 'y': 4}
ENEMY = {'alive?': True, 'current':ORIGIN, 'goal':GOAL_POSITION}
move_enemy(ENEMY)
assert_equal(ENEMY['current']['x'], 1.8000000000000003)
assert_equal(ENEMY['current']['y'], 2.4)
move_enemy(ENEMY)
assert_equal(ENEMY['current']['x'], 3.5999999999999996)
assert_equal(ENEMY['current']['y'], 4.800000000000001)
move_enemy(ENEMY)
assert_equal(ENEMY['current']['x'], 1.8000000000000012)
assert_equal(ENEMY['current']['y'], 2.3999999999999995)
move_enemy(ENEMY)
assert_equal(ENEMY['current']['x'], 3.5999999999999996)
assert_equal(ENEMY['current']['y'], 4.800000000000001)
move_enemy(ENEMY)
assert_equal(ENEMY['current']['x'], 1.8000000000000012)
assert_equal(ENEMY['current']['y'], 2.3999999999999995)

## Testing sort_enemies_and_bullets
WORLD = {
    'player':{'alive?': True,
              'location':{'x': WINDOW_WIDTH / 2,
                          'y': WINDOW_HEIGHT / 2,},
              'moving?': False,
              'direction': ''},
    'enemies':[{'alive?': True, 'current':{'x':30, 'y':30}, 'goal':{'x':200, 'y':200}}],
    'astronaut':{'saved?': False,
                'location':{'x': WINDOW_WIDTH - 100,
                            'y': WINDOW_HEIGHT - 75}},
    'mouse':{'x': WINDOW_WIDTH / 2,
             'y': WINDOW_HEIGHT / 2},
    'score': 0,
    'bullets':[{'current':{'x':30, 'y':30}, 'goal':{'x':100, 'y':100}}],
    'astronaut timer': SPAWN_TIMER,
    'enemy timer': SPAWN_TIMER
}
WORLD['enemies'].append(make_enemy(WORLD))
WORLD['bullets'] = [make_bullet(WORLD)]
sort_enemies_and_bullets(WORLD)
assert_equal(WORLD['enemies'], [{'alive?': True, 'current': {'x': 30, 'y': 30}, 'goal': {'x': 200, 'y': 200}}, {'alive?': True, 'current': {'x': 401, 'y': 424}, 'goal': {'x': 250.0, 'y': 250.0}}])
assert_equal(WORLD['bullets'], [{'current': {'x': 250.0, 'y': 250.0}, 'goal': {'x': 250.0, 'y': 250.0}}])
NEW_WORLD = {
    'player':{'alive?': True,
              'location':{'x': 374,
                          'y': 123,},
              'moving?': False,
              'direction': ''},
    'enemies':[{'alive?': True, 'current':{'x':30, 'y':30}, 'goal':{'x':200, 'y':200}}],
    'astronaut':{'saved?': False,
                'location':{'x': WINDOW_WIDTH - 100,
                            'y': WINDOW_HEIGHT - 75}},
    'mouse':{'x': 101,
             'y': 420},
    'score': 0,
    'bullets':[{'current':{'x':30, 'y':30}, 'goal':{'x':100, 'y':100}}],
    'astronaut timer': SPAWN_TIMER,
    'enemy timer': SPAWN_TIMER
}
sort_enemies_and_bullets(NEW_WORLD)
assert_equal(NEW_WORLD['enemies'], [])
assert_equal(NEW_WORLD['bullets'], [])

###################################################################
## Testing world manipulation functions
###################################################################
## Testing update_world
# separate actions within this function are marked by a single '#'
# Testing INITIAL_WORLD generation
WORLD = {
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
update_world(WORLD)
assert_equal(WORLD, {'player': {'alive?': True, 'location': {'x': 250.0, 'y': 250.0}, 'moving?': False, 'direction': ''}, 'enemies': [], 'astronaut': {'saved?': False, 'location': {'x': 400, 'y': 425}}, 'mouse': {'x': 250.0, 'y': 250.0}, 'score': 0, 'bullets': [], 'astronaut timer': 99, 'enemy timer': 99})

# Using a different world to test gameplay scenarios
NEW_WORLD = {
    'player':{'alive?': True,
              'location':{'x': 374,
                          'y': 123,},
              'moving?': False,
              'direction': ''},
    'enemies':[],
    'astronaut':{'saved?': False,
                'location':{'x': WINDOW_WIDTH - 100,
                            'y': WINDOW_HEIGHT - 75}},
    'mouse':{'x': 101,
             'y': 420},
    'score': 0,
    'bullets':[],
    'astronaut timer': SPAWN_TIMER,
    'enemy timer': SPAWN_TIMER
}
NEW_WORLD['enemies'] = [make_enemy(NEW_WORLD), make_enemy(NEW_WORLD)]
NEW_WORLD['bullets'] = [make_bullet(NEW_WORLD)]
update_world(NEW_WORLD)
assert_equal(NEW_WORLD, {'player': {'alive?': True, 'location': {'x': 374, 'y': 123}, 'moving?': False, 'direction': ''}, 'enemies': [{'alive?': True, 'current': {'x': 156.5219714207416, 'y': 492.41473347709643}, 'goal': {'x': 374, 'y': 123}}, {'alive?': True, 'current': {'x': 246.72387815350135, 'y': 181.74282546761475}, 'goal': {'x': 374, 'y': 123}}], 'astronaut': {'saved?': False, 'location': {'x': 400, 'y': 425}}, 'mouse': {'x': 101, 'y': 420}, 'score': 0, 'bullets': [{'current': {'x': 367.23265745518205, 'y': 130.36227375754916}, 'goal': {'x': 101, 'y': 420}}], 'astronaut timer': 99, 'enemy timer': 99})

# Testing win condition (player saving 10 astronauts)
NEW_WORLD['score'] = 10
update_world(NEW_WORLD)
assert_equal(NEW_WORLD, {'player': {'alive?': False, 'location': {'x': 374, 'y': 123}, 'moving?': False, 'direction': ''}, 'enemies': [], 'astronaut': {'saved?': False, 'location': {'x': 400, 'y': 425}}, 'mouse': {'x': 101, 'y': 420}, 'score': 10, 'bullets': [], 'astronaut timer': 300000, 'enemy timer': 3000000})

# Testing movement updates
NEW_WORLD['player']['alive?'] = True
NEW_WORLD['player']['moving?'] = True
NEW_WORLD['player']['direction'] = 'up'
update_world(NEW_WORLD)
assert_equal(NEW_WORLD['player']['location'], {'x': 374, 'y': 130})

NEW_WORLD['player']['alive?'] = True
NEW_WORLD['player']['moving?'] = True
NEW_WORLD['player']['direction'] = 'down'
update_world(NEW_WORLD)
assert_equal(NEW_WORLD['player']['location'], {'x': 374, 'y': 123})

NEW_WORLD['player']['alive?'] = True
NEW_WORLD['player']['moving?'] = True
NEW_WORLD['player']['direction'] = 'left'
update_world(NEW_WORLD)
assert_equal(NEW_WORLD['player']['location'], {'x': 367, 'y': 123})

NEW_WORLD['player']['alive?'] = True
NEW_WORLD['player']['moving?'] = True
NEW_WORLD['player']['direction'] = 'right'
update_world(NEW_WORLD)
assert_equal(NEW_WORLD['player']['location'], {'x': 374, 'y': 123})

# Testing movement barriers that keep the player model within the game window
NEW_WORLD['player']['location']['x'] = 470
update_world(NEW_WORLD)
assert_equal(NEW_WORLD['player']['moving?'], False)

NEW_WORLD['player']['location']['x'] = 30
update_world(NEW_WORLD)
assert_equal(NEW_WORLD['player']['moving?'], False)

NEW_WORLD['player']['location']['y'] = 470
update_world(NEW_WORLD)
assert_equal(NEW_WORLD['player']['moving?'], False)

NEW_WORLD['player']['location']['y'] = 30
update_world(NEW_WORLD)
assert_equal(NEW_WORLD['player']['moving?'], False)

# Making sure that when the astronaut is saved a new random position is set and world['astronaut']['saved?'] is made False
NEW_WORLD['astronaut']['saved?'] = True
update_world(NEW_WORLD)
assert_equal(NEW_WORLD['astronaut']['location'], {'x': 298, 'y': 456})
assert_equal(NEW_WORLD['astronaut']['saved?'], False)

# Making sure the score is updated when the player collides with the astronaut
NEW_WORLD['player']['alive?'] = True
NEW_WORLD['score'] = 4
NEW_WORLD['player']['location'] = NEW_WORLD['astronaut']['location']
update_world(NEW_WORLD)
assert_equal(NEW_WORLD['astronaut']['saved?'], True)
assert_equal(NEW_WORLD['score'], 5)

# Testing death conditions (when enemy hits player)
NEW_WORLD['enemies'].append(make_enemy(NEW_WORLD))
NEW_WORLD['player']['location'] = NEW_WORLD['enemies'][0]['current']
update_world(NEW_WORLD)
assert_equal(NEW_WORLD, {'player': {'alive?': False, 'location': {'x': 462.69925997931375, 'y': 113.70334522371544}, 'moving?': False, 'direction': 'right'}, 'enemies': [], 'astronaut': {'saved?': False, 'location': {'x': 258, 'y': 71}}, 'mouse': {'x': 101, 'y': 420}, 'score': 5, 'bullets': [], 'astronaut timer': 300000, 'enemy timer': 300000})

# Testing enemy redirection after it hits original goal position
NEW_WORLD['player']['alive?'] = True
NEW_WORLD['enemies'].append(make_enemy(NEW_WORLD))
NEW_WORLD['enemies'][0]['current'] = NEW_WORLD['enemies'][0]['goal']
NEW_WORLD['player']['location'] = make_random_position()
update_world(NEW_WORLD)
assert_equal(NEW_WORLD['enemies'][0]['goal'], NEW_WORLD['player']['location'])

# Making sure bullets are removed once they hit their goal
NEW_WORLD['bullets'].append(make_bullet(NEW_WORLD))
NEW_WORLD['bullets'][0]['current'] = NEW_WORLD['bullets'][0]['goal']
update_world(NEW_WORLD)
assert_equal(NEW_WORLD['bullets'], [])

# Testing enemy spawn timer (world['enemy timer'])
NEW_WORLD['enemies'] = []
NEW_WORLD['enemy timer'] = 0
update_world(NEW_WORLD)
assert_equal(NEW_WORLD['enemies'], [{'alive?': True, 'current': {'x': 316, 'y': 409}, 'goal': {'x': 386, 'y': 48}}])
assert_equal(NEW_WORLD['enemy timer'], 100)

# Testing astronaut spawn timer (world['astronaut timer'])
NEW_WORLD['astronaut']['saved?'] = False
NEW_WORLD['astronaut']['location'] = {'x':0, 'y':0}
NEW_WORLD['astronaut timer'] = 0
update_world(NEW_WORLD)
assert_equal(NEW_WORLD['astronaut timer'], 300)
assert_equal(NEW_WORLD['astronaut']['location'], {'x': 128, 'y': 465})

## Testing handle_key
NEW_WORLD['player']['moving?'] = False
NEW_WORLD['player']['direction'] = ''
handle_key(NEW_WORLD, ord('w'))
assert_equal(NEW_WORLD['player']['direction'], 'up')
assert_equal(NEW_WORLD['player']['moving?'], True)

NEW_WORLD['player']['direction'] = ''
handle_key(NEW_WORLD, ord('a'))
assert_equal(NEW_WORLD['player']['direction'], 'left')

NEW_WORLD['player']['direction'] = ''
handle_key(NEW_WORLD, ord('s'))
assert_equal(NEW_WORLD['player']['direction'], 'down')

NEW_WORLD['player']['direction'] = ''
handle_key(NEW_WORLD, ord('d'))
assert_equal(NEW_WORLD['player']['direction'], 'right')

## Testing handle_mouse
NEW_WORLD['bullets'] = []
handle_mouse(NEW_WORLD, 1, 1, 'left')
assert_equal(NEW_WORLD['bullets'], [{'current': {'x': 386, 'y': 48}, 'goal': {'x': 101, 'y': 420}}])

## Testing handle_motion
NEW_WORLD['mouse']['x'] = 100
NEW_WORLD['mouse']['y'] = 100
handle_motion(NEW_WORLD, 200, 200)
assert_equal(NEW_WORLD['mouse']['x'], 200)
assert_equal(NEW_WORLD['mouse']['y'], 200)

## Testing handle_release
NEW_WORLD['player']['moving?'] = True
handle_release(NEW_WORLD, ord('f'))
assert_equal(NEW_WORLD['player']['moving?'], False)

# Describe this test here, then run whatever code is necessary to
#   perform the tests
assert_equal(1+1, 2)
assert_type(1+1, int)
