import asyncio
import random
import pygame


# ------------------------------------------------------------
# Basic Pygame setup
# ------------------------------------------------------------
pygame.init()

WIDTH = 1300
HEIGHT = 800
FPS = 60

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("The Project DARK")
clock = pygame.time.Clock()


# ------------------------------------------------------------
# Load images
# ------------------------------------------------------------
menu_background = pygame.image.load(
    "images/menu.png"
).convert()

menu_background = pygame.transform.scale(
    menu_background,
    (WIDTH, HEIGHT)
)

game_background = pygame.image.load(
    "images/background.png"
).convert()

game_background = pygame.transform.scale(
    game_background,
    (WIDTH, HEIGHT)
)

game_over_background = pygame.image.load(
    "images/gameover.png"
).convert()

game_over_background = pygame.transform.scale(
    game_over_background,
    (WIDTH, HEIGHT)
)

player_image = pygame.image.load(
    "images/player_transparent.png"
).convert_alpha()

player_image = pygame.transform.scale(
    player_image,
    (350, 350)
)

robot1_image = pygame.image.load(
    "images/terminator_transparent.png"
).convert_alpha()

robot1_image = pygame.transform.scale(
    robot1_image,
    (300, 300)
)

robot2_image = pygame.image.load(
    "images/terminator2_transparent.png"
).convert_alpha()

robot2_image = pygame.transform.scale(
    robot2_image,
    (300, 300)
)

meteor_image = pygame.image.load(
    "images/astriod_transparent.png"
).convert_alpha()

meteor_image = pygame.transform.scale(
    meteor_image,
    (350, 350)
)


# ------------------------------------------------------------
# Audio
#
# Audio is initialized only after the player clicks Play.
# This is important because browsers block automatic audio.
# ------------------------------------------------------------
audio_ready = False
meteor_sound = None
ray_sound = None
robot_walk_sound = None


def initialize_audio():
    """Initialize and load sounds after a user interaction."""
    global audio_ready
    global meteor_sound, ray_sound, robot_walk_sound

    if audio_ready:
        return

    try:
        if not pygame.mixer.get_init():
            pygame.mixer.init()

        pygame.mixer.music.load(
            "sounds/robot_wars_main_theme.ogg"
        )
        pygame.mixer.music.set_volume(0.35)

        meteor_sound = pygame.mixer.Sound(
            "sounds/meteor_sound.ogg"
        )
        meteor_sound.set_volume(0.20)

        ray_sound = pygame.mixer.Sound(
            "sounds/laser_gun.ogg"
        )
        ray_sound.set_volume(0.50)

        robot_walk_sound = pygame.mixer.Sound(
            "sounds/robot_walk.ogg"
        )
        robot_walk_sound.set_volume(0.50)

        audio_ready = True
        print("Audio initialized successfully.")

    except pygame.error as error:
        # The game will continue even if the browser cannot start audio.
        audio_ready = False
        print(f"Audio could not be initialized: {error}")


def start_background_music():
    """Start the background music after the Play click."""
    if not audio_ready:
        return

    try:
        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.play(-1)
    except pygame.error as error:
        print(f"Background music could not start: {error}")


def play_sound(sound):
    """Safely play a sound when audio is available."""
    if not audio_ready or sound is None:
        return

    try:
        sound.play()
    except pygame.error as error:
        print(f"Sound could not play: {error}")


def stop_sound(sound):
    """Safely stop a sound when audio is available."""
    if not audio_ready or sound is None:
        return

    try:
        sound.stop()
    except pygame.error:
        pass


# ------------------------------------------------------------
# Player values
# ------------------------------------------------------------
ground_y = HEIGHT - player_image.get_height() + 10

player_x = WIDTH // 2
player_y = ground_y

player_speed = 7
player_jump_speed = -15
gravity = 0.5

is_jumping = False
velocity_y = 0

facing_right = True


# ------------------------------------------------------------
# Robot 1 values
# ------------------------------------------------------------
robot1_x = random.choice([
    0,
    WIDTH - robot1_image.get_width()
])

robot1_y = HEIGHT - robot1_image.get_height()
robot1_speed_x = 1
robot1_spawn_timer = random.randint(1000, 3000)
robot1_visible = False
robot1_moving_left = False
robot1_draw_image = robot1_image


# ------------------------------------------------------------
# Robot 2 values
# ------------------------------------------------------------
robot2_x = random.choice([
    0,
    WIDTH - robot2_image.get_width()
])

robot2_y = HEIGHT - robot2_image.get_height()
robot2_speed_x = 1
robot2_spawn_timer = random.randint(1000, 3000)
robot2_visible = False
robot2_moving_left = False
robot2_draw_image = robot2_image


# ------------------------------------------------------------
# Meteor values
# ------------------------------------------------------------
meteor_x = random.randint(
    0,
    WIDTH - meteor_image.get_width()
)

meteor_y = -meteor_image.get_height()
meteor_speed_y = 2
meteor_speed_x = 2
meteor_visible = False
meteor_spawn_timer = random.randint(1000, 3000)


# ------------------------------------------------------------
# Laser values
# ------------------------------------------------------------
rays = []

ray_width = 5
ray_length = 10
ray_color = (255, 0, 0)
ray_speed = 10
ray_direction = 1


# ------------------------------------------------------------
# Text and buttons
# ------------------------------------------------------------
title_font = pygame.font.SysFont(None, 150)
title_text = title_font.render(
    "The project DARK",
    True,
    (255, 255, 255)
)

menu_font = pygame.font.SysFont(None, 50)

play_text = menu_font.render(
    "Play",
    True,
    (255, 255, 255)
)

menu_exit_text = menu_font.render(
    "Exit",
    True,
    (255, 255, 255)
)

title_rect = title_text.get_rect(
    center=(WIDTH // 2, HEIGHT // 3 + 36)
)

play_rect = play_text.get_rect(
    center=(WIDTH // 2 + 30, HEIGHT // 2 + 60)
)

menu_exit_rect = menu_exit_text.get_rect(
    center=(WIDTH // 2 + 30, HEIGHT // 2 + 120)
)

game_over_font = pygame.font.SysFont(None, 100)

game_over_text = game_over_font.render(
    "Game Over",
    True,
    (255, 0, 0)
)

game_over_rect = game_over_text.get_rect(
    center=(WIDTH // 2, HEIGHT // 3)
)

game_over_menu_font = pygame.font.SysFont(None, 50)

replay_text = game_over_menu_font.render(
    "Replay",
    True,
    (255, 255, 255)
)

game_exit_text = game_over_menu_font.render(
    "Exit",
    True,
    (255, 255, 255)
)

replay_rect = replay_text.get_rect(
    center=(WIDTH // 2, HEIGHT // 2 + 60)
)

game_exit_rect = game_exit_text.get_rect(
    center=(WIDTH // 2, HEIGHT // 2 + 120)
)


# ------------------------------------------------------------
# Game state
# ------------------------------------------------------------
in_menu = True
game_over = False
run = True


def reset_game():
    """Reset every gameplay value for a clean replay."""
    global player_x, player_y
    global is_jumping, velocity_y
    global facing_right, ray_direction

    global robot1_x, robot1_y
    global robot1_spawn_timer
    global robot1_visible
    global robot1_moving_left
    global robot1_draw_image

    global robot2_x, robot2_y
    global robot2_spawn_timer
    global robot2_visible
    global robot2_moving_left
    global robot2_draw_image

    global meteor_x, meteor_y
    global meteor_visible
    global meteor_spawn_timer

    # Reset the player.
    player_x = WIDTH // 2
    player_y = ground_y
    is_jumping = False
    velocity_y = 0
    facing_right = True
    ray_direction = 1

    # Remove all old lasers.
    rays.clear()

    # Reset robot 1.
    robot1_x = random.choice([
        0,
        WIDTH - robot1_image.get_width()
    ])
    robot1_y = HEIGHT - robot1_image.get_height()
    robot1_moving_left = (
        robot1_x == WIDTH - robot1_image.get_width()
    )
    robot1_visible = False
    robot1_spawn_timer = random.randint(1000, 3000)
    robot1_draw_image = robot1_image

    # Reset robot 2.
    robot2_x = random.choice([
        0,
        WIDTH - robot2_image.get_width()
    ])
    robot2_y = HEIGHT - robot2_image.get_height()
    robot2_moving_left = (
        robot2_x == WIDTH - robot2_image.get_width()
    )
    robot2_visible = False
    robot2_spawn_timer = random.randint(1000, 3000)
    robot2_draw_image = robot2_image

    # Reset the meteor.
    meteor_x = random.randint(
        0,
        WIDTH - meteor_image.get_width()
    )
    meteor_y = -meteor_image.get_height()
    meteor_visible = False
    meteor_spawn_timer = random.randint(1000, 3000)

    # Stop old sounds from the previous round.
    stop_sound(robot_walk_sound)
    stop_sound(meteor_sound)


async def main():
    global run, in_menu, game_over

    global player_x, player_y
    global is_jumping, velocity_y
    global facing_right, ray_direction

    global robot1_x, robot1_y
    global robot1_spawn_timer
    global robot1_visible
    global robot1_moving_left
    global robot1_draw_image

    global robot2_x, robot2_y
    global robot2_spawn_timer
    global robot2_visible
    global robot2_moving_left
    global robot2_draw_image

    global meteor_x, meteor_y
    global meteor_spawn_timer
    global meteor_visible

    while run:
        delta_time = clock.tick(FPS)

        # ----------------------------------------------------
        # Events
        # ----------------------------------------------------
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_position = pygame.mouse.get_pos()

                # Main menu Play button.
                if in_menu and play_rect.collidepoint(
                    mouse_position
                ):
                    initialize_audio()
                    start_background_music()

                    reset_game()
                    in_menu = False
                    game_over = False

                # Main menu Exit button.
                elif in_menu and menu_exit_rect.collidepoint(
                    mouse_position
                ):
                    run = False

                # Game-over menu.
                elif game_over:
                    if replay_rect.collidepoint(mouse_position):
                        initialize_audio()
                        start_background_music()

                        reset_game()
                        game_over = False
                        in_menu = False

                    elif game_exit_rect.collidepoint(
                        mouse_position
                    ):
                        run = False

        keys = pygame.key.get_pressed()

        # ----------------------------------------------------
        # Gameplay updates
        # ----------------------------------------------------
        if not in_menu and not game_over:

            # Player movement.
            if keys[pygame.K_LEFT]:
                player_x -= player_speed
                facing_right = False
                ray_direction = -1

            if keys[pygame.K_RIGHT]:
                player_x += player_speed
                facing_right = True
                ray_direction = 1

            player_x = max(
                0,
                min(
                    player_x,
                    WIDTH - player_image.get_width()
                )
            )

            # Jumping.
            if not is_jumping and keys[pygame.K_SPACE]:
                is_jumping = True
                velocity_y = player_jump_speed

            if is_jumping:
                player_y += velocity_y
                velocity_y += gravity

                if player_y >= ground_y:
                    player_y = ground_y
                    is_jumping = False
                    velocity_y = 0

            # Shoot a laser.
            if keys[pygame.K_RETURN]:
                if len(rays) < 100:
                    if facing_right:
                        ray_start_x = (
                            player_x
                            + player_image.get_width()
                            - 70
                        )
                    else:
                        ray_start_x = player_x + 70

                    new_ray = {
                        "x": ray_start_x,
                        "y": (
                            player_y
                            + player_image.get_height() // 2
                            - 38
                        ),
                        "direction": ray_direction
                    }

                    rays.append(new_ray)
                    play_sound(ray_sound)

            # Collision rectangles before laser movement.
            robot1_rect = pygame.Rect(
                robot1_x,
                robot1_y,
                robot1_image.get_width(),
                robot1_image.get_height()
            )

            robot2_rect = pygame.Rect(
                robot2_x,
                robot2_y,
                robot2_image.get_width(),
                robot2_image.get_height()
            )

            # Safely update and remove lasers.
            for ray in rays[:]:
                ray["x"] += (
                    ray["direction"] * ray_speed
                )

                remove_ray = False

                if (
                    ray["x"] < -ray_length
                    or ray["x"] > WIDTH + ray_length
                ):
                    remove_ray = True

                else:
                    ray_rect = pygame.Rect(
                        ray["x"],
                        ray["y"],
                        ray_length,
                        ray_width
                    )

                    if (
                        robot1_visible
                        and ray_rect.colliderect(robot1_rect)
                    ):
                        robot1_visible = False
                        stop_sound(robot_walk_sound)
                        remove_ray = True

                    elif (
                        robot2_visible
                        and ray_rect.colliderect(robot2_rect)
                    ):
                        robot2_visible = False
                        stop_sound(robot_walk_sound)
                        remove_ray = True

                if remove_ray and ray in rays:
                    rays.remove(ray)

            # Spawn robot 1.
            robot1_spawn_timer -= delta_time

            if (
                robot1_spawn_timer <= 0
                and not robot1_visible
            ):
                robot1_spawn_timer = random.randint(
                    1000,
                    3000
                )

                robot1_x = random.choice([
                    0,
                    WIDTH - robot1_image.get_width()
                ])

                robot1_y = (
                    HEIGHT - robot1_image.get_height()
                )

                robot1_moving_left = (
                    robot1_x
                    == WIDTH - robot1_image.get_width()
                )

                robot1_visible = True
                play_sound(robot_walk_sound)

                if robot1_x == 0:
                    robot1_draw_image = pygame.transform.flip(
                        robot1_image,
                        True,
                        False
                    )
                else:
                    robot1_draw_image = robot1_image

            # Move robot 1.
            if robot1_visible:
                if robot1_moving_left:
                    robot1_x -= robot1_speed_x
                else:
                    robot1_x += robot1_speed_x

                if (
                    robot1_x < 0
                    or robot1_x
                    > WIDTH - robot1_image.get_width()
                ):
                    robot1_visible = False
                    stop_sound(robot_walk_sound)

            # Spawn robot 2.
            robot2_spawn_timer -= delta_time

            if (
                robot2_spawn_timer <= 0
                and not robot2_visible
            ):
                robot2_spawn_timer = random.randint(
                    1000,
                    3000
                )

                robot2_x = random.choice([
                    0,
                    WIDTH - robot2_image.get_width()
                ])

                robot2_y = (
                    HEIGHT - robot2_image.get_height()
                )

                robot2_moving_left = (
                    robot2_x
                    == WIDTH - robot2_image.get_width()
                )

                robot2_visible = True
                play_sound(robot_walk_sound)

                if robot2_x == 0:
                    robot2_draw_image = pygame.transform.flip(
                        robot2_image,
                        True,
                        False
                    )
                else:
                    robot2_draw_image = robot2_image

            # Move robot 2.
            if robot2_visible:
                if robot2_moving_left:
                    robot2_x -= robot2_speed_x
                else:
                    robot2_x += robot2_speed_x

                if (
                    robot2_x < 0
                    or robot2_x
                    > WIDTH - robot2_image.get_width()
                ):
                    robot2_visible = False
                    stop_sound(robot_walk_sound)

            # Spawn the meteor.
            meteor_spawn_timer -= delta_time

            if (
                meteor_spawn_timer <= 0
                and not meteor_visible
            ):
                meteor_spawn_timer = random.randint(
                    1000,
                    3000
                )

                meteor_x = random.randint(
                    0,
                    WIDTH - meteor_image.get_width()
                )

                meteor_y = -meteor_image.get_height()
                meteor_visible = True
                play_sound(meteor_sound)

            # Move the meteor.
            if meteor_visible:
                meteor_y += meteor_speed_y
                meteor_x -= meteor_speed_x

                if (
                    meteor_y > HEIGHT
                    or meteor_x < -meteor_image.get_width()
                ):
                    meteor_visible = False
                    stop_sound(meteor_sound)

            # Rebuild collision rectangles after movement.
            player_rect = pygame.Rect(
                player_x,
                player_y,
                player_image.get_width(),
                player_image.get_height()
            )

            robot1_rect = pygame.Rect(
                robot1_x,
                robot1_y,
                robot1_image.get_width(),
                robot1_image.get_height()
            )

            robot2_rect = pygame.Rect(
                robot2_x,
                robot2_y,
                robot2_image.get_width(),
                robot2_image.get_height()
            )

            meteor_rect = pygame.Rect(
                meteor_x,
                meteor_y,
                meteor_image.get_width(),
                meteor_image.get_height()
            )

            hit_robot1 = (
                robot1_visible
                and player_rect.colliderect(robot1_rect)
            )

            hit_robot2 = (
                robot2_visible
                and player_rect.colliderect(robot2_rect)
            )

            hit_meteor = (
                meteor_visible
                and player_rect.colliderect(meteor_rect)
            )

            if hit_robot1 or hit_robot2 or hit_meteor:
                game_over = True
                stop_sound(robot_walk_sound)
                stop_sound(meteor_sound)

        # ----------------------------------------------------
        # Drawing
        # ----------------------------------------------------
        if game_over:
            screen.blit(
                game_over_background,
                (0, 0)
            )
            screen.blit(
                game_over_text,
                game_over_rect
            )
            screen.blit(
                replay_text,
                replay_rect
            )
            screen.blit(
                game_exit_text,
                game_exit_rect
            )

        elif in_menu:
            screen.blit(
                menu_background,
                (0, 0)
            )
            screen.blit(
                title_text,
                title_rect
            )
            screen.blit(
                play_text,
                play_rect
            )
            screen.blit(
                menu_exit_text,
                menu_exit_rect
            )

        else:
            screen.blit(
                game_background,
                (0, 0)
            )

            if facing_right:
                screen.blit(
                    player_image,
                    (player_x, player_y)
                )
            else:
                flipped_player = pygame.transform.flip(
                    player_image,
                    True,
                    False
                )

                screen.blit(
                    flipped_player,
                    (player_x, player_y)
                )

            for ray in rays:
                if ray["direction"] == 1:
                    pygame.draw.line(
                        screen,
                        ray_color,
                        (ray["x"], ray["y"]),
                        (
                            ray["x"] + ray_length,
                            ray["y"]
                        ),
                        ray_width
                    )
                else:
                    pygame.draw.line(
                        screen,
                        ray_color,
                        (ray["x"], ray["y"]),
                        (
                            ray["x"] - ray_length,
                            ray["y"]
                        ),
                        ray_width
                    )

            if robot1_visible:
                screen.blit(
                    robot1_draw_image,
                    (robot1_x, robot1_y)
                )

            if robot2_visible:
                screen.blit(
                    robot2_draw_image,
                    (robot2_x, robot2_y)
                )

            if meteor_visible:
                screen.blit(
                    meteor_image,
                    (meteor_x, meteor_y)
                )

        pygame.display.update()

        # Required by Pygbag so the browser remains responsive.
        await asyncio.sleep(0)


# Browser/Pygbag entry point.
asyncio.run(main())
