import pgzero.builtins
import time
import random

WIDTH = 800
HEIGHT = 600

player_images = ['player_frame_0', 'player_frame_1']
enemy_images = ['enemy_frame_0', 'enemy_frame_1']
life_images = ['life_frame_0', 'life_frame_1']

player = Actor(player_images[0], center=(WIDTH / 2, HEIGHT / 2))
enemy = Actor(enemy_images[0])
life_item = Actor(life_images[0])

# --- Variáveis do Jogo ---
PLAYER_SPEED = 5
player_lives = 3
invulnerable_timer = 0
is_flashing = False

enemy_speed = 3
enemy_dx = 0
enemy_dy = 0
enemy_exists = False
TRACKING_STRENGTH = 0.02

LIFE_ITEM_SPEED = 1.5
life_item_dx = 0
life_item_dy = 0
life_item_exists = False
LIFE_ITEM_SPAWN_CHANCE = 100
FLEE_DISTANCE = 150
MAX_FLEE_STRENGTH = 0.1

score = 0
start_time = 0
game_duration = 0
game_state = "menu"

DIFFICULTY_SCORE_INTERVAL = 5
last_difficulty_score = 0
INITIAL_ENEMY_SPEED = 3
INITIAL_TRACKING_STRENGTH = 0.02

# --- Configuração do Menu ---
BUTTON_WIDTH = 150
BUTTON_HEIGHT = 50
START_BUTTON_X = WIDTH // 2 - BUTTON_WIDTH // 2
START_BUTTON_Y = 150
EXIT_BUTTON_X = WIDTH // 2 - BUTTON_WIDTH // 2
EXIT_BUTTON_Y = HEIGHT - 100
SLIDER_WIDTH = 250
SLIDER_HEIGHT = 10
SLIDER_X = WIDTH // 2 - SLIDER_WIDTH // 2
SLIDER_Y = 325 - SLIDER_HEIGHT // 2
music_volume = 0.5
dragging_slider = False

music.set_volume(music_volume)
music.play("music")

# --- Fundo e Bolhas ---
bubbles = []
BUBBLE_COUNT = 50
WATER_COLOR_DEEP = (0, 0, 75)
WATER_COLOR_LIGHT = (30, 144, 255)
OCEAN_FLOOR_COLOR = '#8B4513'

def create_bubbles():
    for _ in range(BUBBLE_COUNT):
        bubbles.append({
            'x': random.randint(0, WIDTH),
            'y': random.randint(0, HEIGHT),
            'size': random.randint(1, 4),
            'speed': random.uniform(0.1, 0.5),
        })

def draw_background():
    for y_line in range(HEIGHT):
        r = int(WATER_COLOR_DEEP[0] + (WATER_COLOR_LIGHT[0] - WATER_COLOR_DEEP[0]) * (y_line / HEIGHT))
        g = int(WATER_COLOR_DEEP[1] + (WATER_COLOR_LIGHT[1] - WATER_COLOR_DEEP[1]) * (y_line / HEIGHT))
        b = int(WATER_COLOR_DEEP[2] + (WATER_COLOR_LIGHT[2] - WATER_COLOR_DEEP[2]) * (y_line / HEIGHT))
        screen.draw.line((0, y_line), (WIDTH, y_line), (r, g, b))
    screen.draw.filled_rect(Rect(0, HEIGHT - 30, WIDTH, 30), OCEAN_FLOOR_COLOR)
    for bubble in bubbles:
        bubble_color = (190, 220, 255)
        screen.draw.filled_rect(Rect(bubble['x'], bubble['y'], bubble['size'], bubble['size']), bubble_color)
        bubble['y'] -= bubble['speed']
        if bubble['y'] < 0:
            bubble['y'] = HEIGHT
            bubble['x'] = random.randint(0, WIDTH)

def generate_random_enemy():
    global enemy_dx, enemy_dy, enemy_exists
    side = random.randint(0, 3)
    if side == 0: enemy.x, enemy.bottom = random.randint(0, WIDTH), 0
    elif side == 1: enemy.y, enemy.left = random.randint(0, HEIGHT), WIDTH
    elif side == 2: enemy.x, enemy.top = random.randint(0, WIDTH), HEIGHT
    else: enemy.y, enemy.right = random.randint(0, HEIGHT), 0
    target_dx, target_dy = player.x - enemy.x, player.y - enemy.y
    magnitude = (target_dx**2 + target_dy**2)**0.5
    enemy_dx = target_dx / magnitude if magnitude else 0
    enemy_dy = target_dy / magnitude if magnitude else 0
    enemy_exists = True

def generate_random_life_item():
    global life_item_dx, life_item_dy, life_item_exists
    side = random.randint(0, 3)
    if side == 0: life_item.x, life_item.bottom = random.randint(0, WIDTH), 0
    elif side == 1: life_item.y, life_item.left = random.randint(0, HEIGHT), WIDTH
    elif side == 2: life_item.x, life_item.top = random.randint(0, WIDTH), HEIGHT
    else: life_item.y, life_item.right = random.randint(0, HEIGHT), 0
    life_item_dx, life_item_dy = random.uniform(-1, 1), random.uniform(-1, 1)
    magnitude = (life_item_dx**2 + life_item_dy**2)**0.5
    if magnitude:
        life_item_dx /= magnitude
        life_item_dy /= magnitude
    life_item_exists = True

def reset_game():
    global player_lives, invulnerable_timer, is_flashing, score, start_time
    global enemy_exists, life_item_exists, enemy_speed, TRACKING_STRENGTH, last_difficulty_score
    player.pos = (WIDTH / 2, HEIGHT / 2)
    player_lives = 3
    invulnerable_timer = 0
    is_flashing = False
    score = 0
    start_time = time.time()
    enemy_exists = False
    life_item_exists = False
    enemy_speed = INITIAL_ENEMY_SPEED
    TRACKING_STRENGTH = INITIAL_TRACKING_STRENGTH
    last_difficulty_score = 0

def update(dt):
    global game_state, player_lives, invulnerable_timer, is_flashing, score, game_duration
    global enemy_exists, enemy_dx, enemy_dy, enemy_speed, TRACKING_STRENGTH, last_difficulty_score
    global life_item_exists, life_item_dx, life_item_dy
    
    if game_state != "game":
        return

    anim_speed = 5
    player.image = player_images[int(time.time() * anim_speed) % len(player_images)]
    enemy.image = enemy_images[int(time.time() * anim_speed) % len(enemy_images)]
    life_item.image = life_images[int(time.time() * anim_speed) % len(life_images)]
    
    game_duration = time.time() - start_time
    
    if score >= last_difficulty_score + DIFFICULTY_SCORE_INTERVAL:
        last_difficulty_score = score
        enemy_speed += 0.5
        TRACKING_STRENGTH = min(0.1, TRACKING_STRENGTH + 0.005)

    if invulnerable_timer > 0:
        invulnerable_timer -= dt
        is_flashing = invulnerable_timer > 0

    player_is_moving = (keyboard.a or keyboard.left or
                        keyboard.d or keyboard.right or
                        keyboard.w or keyboard.up or
                        keyboard.s or keyboard.down)

    if player_is_moving:
        if keyboard.a or keyboard.left: player.x -= PLAYER_SPEED
        if keyboard.d or keyboard.right: player.x += PLAYER_SPEED
        if keyboard.w or keyboard.up: player.y -= PLAYER_SPEED
        if keyboard.s or keyboard.down: player.y += PLAYER_SPEED
        player.x = max(player.width / 2, min(WIDTH - player.width / 2, player.x))
        player.y = max(player.height / 2, min(HEIGHT - player.height / 2, player.y))

    if not enemy_exists:
        generate_random_enemy()
    else:
        # Lógica de perseguição do inimigo
        target_dx, target_dy = player.x - enemy.x, player.y - enemy.y
        magnitude = (target_dx**2 + target_dy**2)**0.5

        if magnitude > 0:
            target_dx_norm = target_dx / magnitude
            target_dy_norm = target_dy / magnitude

            # Se o jogador estiver parado, o inimigo mira diretamente
            if not player_is_moving:
                enemy_dx = target_dx_norm
                enemy_dy = target_dy_norm
            # Se o jogador estiver em movimento, a mira é mais suave
            else:
                enemy_dx = (1 - TRACKING_STRENGTH) * enemy_dx + TRACKING_STRENGTH * target_dx_norm
                enemy_dy = (1 - TRACKING_STRENGTH) * enemy_dy + TRACKING_STRENGTH * target_dy_norm
                # Normaliza o vetor de direção para manter a velocidade constante
                dir_mag = (enemy_dx**2 + enemy_dy**2)**0.5
                if dir_mag > 0:
                    enemy_dx /= dir_mag
                    enemy_dy /= dir_mag

        enemy.x += enemy_dx * enemy_speed
        enemy.y += enemy_dy * enemy_speed

        if enemy.left > WIDTH or enemy.right < 0 or enemy.top > HEIGHT or enemy.bottom < 0:
            score += 1
            enemy_exists = False

    if not life_item_exists and player_lives < 3 and random.randint(1, LIFE_ITEM_SPAWN_CHANCE) == 1:
        generate_random_life_item()
    if life_item_exists:
        flee_dx, flee_dy = life_item.x - player.x, life_item.y - player.y
        flee_mag = (flee_dx**2 + flee_dy**2)**0.5
        if 0 < flee_mag < FLEE_DISTANCE:
            strength = MAX_FLEE_STRENGTH * (1 - flee_mag / FLEE_DISTANCE)
            life_item_dx = (1-strength) * life_item_dx + strength * (flee_dx/flee_mag)
            life_item_dy = (1-strength) * life_item_dy + strength * (flee_dy/flee_mag)
        life_item.x += life_item_dx * LIFE_ITEM_SPEED
        life_item.y += life_item_dy * LIFE_ITEM_SPEED
        if life_item.left > WIDTH or life_item.right < 0 or life_item.top > HEIGHT or life_item.bottom < 0:
            life_item_exists = False

    if enemy_exists and player.colliderect(enemy) and invulnerable_timer <= 0:
        player_lives -= 1
        invulnerable_timer = 2
        enemy_exists = False
        if player_lives < 0:
            game_state = "game_over"
    if life_item_exists and player.colliderect(life_item):
        if player_lives < 3: player_lives += 1
        life_item_exists = False

def draw():
    screen.clear()
    draw_background()

    if game_state == "menu":
        screen.draw.text("BitGame - Diogo Silva", center=(WIDTH / 2, 50), fontsize=60, color="white")
        screen.draw.filled_rect(Rect((START_BUTTON_X, START_BUTTON_Y), (BUTTON_WIDTH, BUTTON_HEIGHT)), "orange")
        screen.draw.text("Start Game", center=(START_BUTTON_X + BUTTON_WIDTH / 2, START_BUTTON_Y + BUTTON_HEIGHT / 2), fontsize=30, color="white")
        screen.draw.filled_rect(Rect((EXIT_BUTTON_X, EXIT_BUTTON_Y), (BUTTON_WIDTH, BUTTON_HEIGHT)), "orange")
        screen.draw.text("Exit", center=(EXIT_BUTTON_X + BUTTON_WIDTH / 2, EXIT_BUTTON_Y + BUTTON_HEIGHT / 2), fontsize=30, color="white")
        screen.draw.filled_rect(Rect((SLIDER_X, SLIDER_Y), (SLIDER_WIDTH, SLIDER_HEIGHT)), "gray")
        screen.draw.text("Volume", center=(WIDTH / 2, SLIDER_Y - 30), fontsize=30, color="white")
        screen.draw.text(f"{int(100 * music_volume)}%", center=(WIDTH / 2, SLIDER_Y + 40), fontsize=30, color="white")
        pin_x = SLIDER_X + int(SLIDER_WIDTH * music_volume)
        screen.draw.filled_circle((pin_x, SLIDER_Y + SLIDER_HEIGHT / 2), 15, "orange")
    
    elif game_state == "game_over":
        screen.draw.text("Game Over", center=(WIDTH/2, 100), fontsize=100, color="red")
        screen.draw.text(f"Score: {score}", center=(WIDTH/2, 200), fontsize=60, color="white")
        minutes, seconds = divmod(int(game_duration), 60)
        screen.draw.text(f"Time: {minutes:02d}:{seconds:02d}", center=(WIDTH/2, 260), fontsize=60, color="white")
        screen.draw.filled_rect(Rect((EXIT_BUTTON_X, EXIT_BUTTON_Y - 100), (BUTTON_WIDTH, BUTTON_HEIGHT)), "orange")
        screen.draw.text("Start Menu", center=(EXIT_BUTTON_X + BUTTON_WIDTH/2, EXIT_BUTTON_Y - 100 + BUTTON_HEIGHT/2), fontsize=30, color="white")
        screen.draw.filled_rect(Rect((EXIT_BUTTON_X, EXIT_BUTTON_Y), (BUTTON_WIDTH, BUTTON_HEIGHT)), "orange")
        screen.draw.text("Exit", center=(EXIT_BUTTON_X + BUTTON_WIDTH / 2, EXIT_BUTTON_Y + BUTTON_HEIGHT / 2), fontsize=30, color="white")

    elif game_state == "game":
        if not is_flashing or (int(time.time() * 10) % 2 == 0):
            player.draw()
        if enemy_exists: enemy.draw()
        if life_item_exists: life_item.draw()
        screen.draw.text(f"Lives: {player_lives}", topleft=(10, 10), fontsize=40, color="white")
        screen.draw.text(f"Score: {score}", topleft=(10, 50), fontsize=40, color="white")

def on_mouse_down(pos):
    global game_state, dragging_slider
    start_button = Rect((START_BUTTON_X, START_BUTTON_Y), (BUTTON_WIDTH, BUTTON_HEIGHT))
    exit_button = Rect((EXIT_BUTTON_X, EXIT_BUTTON_Y), (BUTTON_WIDTH, BUTTON_HEIGHT))
    menu_button = Rect((EXIT_BUTTON_X, EXIT_BUTTON_Y - 100), (BUTTON_WIDTH, BUTTON_HEIGHT))
    pin_x = SLIDER_X + int(SLIDER_WIDTH * music_volume)
    pin = Rect((pin_x - 15, SLIDER_Y - 10), (30, 30))
    if game_state == "menu":
        if start_button.collidepoint(pos):
            game_state = "game"
            reset_game()
        elif exit_button.collidepoint(pos): exit()
        elif pin.collidepoint(pos): dragging_slider = True
    elif game_state == "game_over":
        if menu_button.collidepoint(pos): game_state = "menu"
        elif exit_button.collidepoint(pos): exit()

def on_mouse_up(pos):
    global dragging_slider
    dragging_slider = False

def on_mouse_move(pos):
    global music_volume
    if dragging_slider:
        x = max(SLIDER_X, min(pos[0], SLIDER_X + SLIDER_WIDTH))
        music_volume = (x - SLIDER_X) / SLIDER_WIDTH
        music.set_volume(music_volume)

create_bubbles()
