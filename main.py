import pygame
import random



pygame.init()

pygame.mixer.init()

# Load and play background music
pygame.mixer.music.load('C:/Users/Windows 10/Downloads/Main Title - The Terminator - Trim.mp3')  # Replace with your music file path
pygame.mixer.music.play(-1)

meteor_sound = pygame.mixer.Sound('C:/Users/Windows 10/Downloads/shooting-star-136692-[AudioTrimmer.com].mp3')  # Replace with your sound file path
meteor_sound.set_volume(0.2)

ray_sound = pygame.mixer.Sound('C:/Users/Windows 10/Downloads/laser-gun-81720-[AudioTrimmer.com].mp3')
ray_sound.set_volume(0.5)

random_image_sound = pygame.mixer.Sound('C:/Users/Windows 10/Downloads/robot-walk-82499-[AudioTrimmer.com].mp3')  # Replace with your random image sound file path
random_image_sound.set_volume(0.5)

width = 1300
height = 800

screen = pygame.display.set_mode((width, height))

main = pygame.image.load('C:/Users/Windows 10/Downloads/apocalyptic-destruction-war-zone-landscape.jpg')
main = pygame.transform.scale(main,(width,height))

background = pygame.image.load('C:/Users/Windows 10/Downloads/7402581.jpg')
background = pygame.transform.scale(background, (width, height))

game_over_background = pygame.image.load('C:/Users/Windows 10/Downloads/apocalyptic-destruction-war-zone-landscape (1).jpg')  # Replace with your image path
game_over_background = pygame.transform.scale(game_over_background, (width, height))

image = pygame.image.load('C:/Users/Windows 10/Downloads/soldier-uniform-cartoon-character (2).png')
image = pygame.transform.scale(image, (250, 250))

random_image = pygame.image.load('C:/Users/Windows 10/Downloads/robot1.png')  # Replace with your obstacle image path
random_image = pygame.transform.scale(random_image, (250, 250))

random_image2 = pygame.image.load('C:/Users/Windows 10/Downloads/robot_2-removebg-preview.png')
random_image2 = pygame.transform.scale(random_image2, (250, 250))  # Second random image


meteor_image = pygame.image.load('C:/Users/Windows 10/Downloads/astrroid.png')  # Replace with actual meteor image path
meteor_image = pygame.transform.scale(meteor_image, (100, 100))


# Player attributes
player_x = width // 2
player_y = height - 220
player_speed = 7
player_jump_speed = -15
gravity = 0.5
is_jumping = False
velocity_y = 0

facing_right = True

# Random image attributes
random_image_x = random.choice([0, width - random_image.get_width()])  # Start from left or right
random_image_y = height - random_image.get_height()
random_image_speed_x = 1
random_spawn_timer = random.randint(1000, 3000)  # Timer for random image spawn (in milliseconds)
random_image_visible = False
moving_left = False

random_image2_x = random.choice([0, width - random_image2.get_width()])  # Spawn from left or right edge
random_image2_y = height - random_image2.get_height()  # Keep random object near the bottom of the screen
random_image2_speed_x = 1
random_image2_spawn_timer = random.randint(1000, 3000)  # Timer for random image spawn (in milliseconds)
random_image2_visible = False
random_image2_moving_left = False


meteor_x = random.randint(0, width - meteor_image.get_width())
meteor_y = -meteor_image.get_height()  # Start above the screen
meteor_speed_y = 2
meteor_speed_x = 2
meteor_visible = False
meteor_spawn_timer = random.randint(1000, 3000)  # Timer for meteor spawn (in milliseconds)



# Ray attributes (for the player)
rays=[]
ray_width = 5
ray_length = 10
ray_color = (255, 0, 0)
ray_active = False
ray_x = 0
ray_y = 0
ray_speed = 10
ray_direction = -1



font = pygame.font.SysFont(None, 150)
text = font.render('The project DARK', True, (255, 255, 255))

font2 = pygame.font.SysFont(None, 50)
text2 = font2.render('Play', True, (255, 255, 255))
text3 = font2.render('Exit', True, (255, 255, 255))

text_rect = text.get_rect(center=(width // 2, height // 3 + 36))
text2_rect = text2.get_rect(center=(width // 2 +30, height // 2 + 60))
text3_rect = text3.get_rect(center=(width // 2+30, height // 2 + 120))

game_over_font = pygame.font.SysFont(None, 100)
game_over_text = game_over_font.render('Game Over', True, (255, 0, 0))
game_over_rect = game_over_text.get_rect(center=(width // 2, height // 3))

game_over_menu_font = pygame.font.SysFont(None, 50)
replay_text = game_over_menu_font.render('Replay', True, (255, 255, 255))
exit_text = game_over_menu_font.render('Exit', True, (255, 255, 255))

replay_rect = replay_text.get_rect(center=(width // 2, height // 2 + 60))
exit_rect = exit_text.get_rect(center=(width // 2, height // 2 + 120))

in_menu = True
game_over = False  # New variable to track Game Over state

fps = 60
run = True
clock = pygame.time.Clock()

while run:
    delta_time = clock.tick(fps)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()

            if in_menu and text2_rect.collidepoint(mouse_pos):
                in_menu = False


            if in_menu and text3_rect.collidepoint(mouse_pos):
                run = False

            if game_over:
                if replay_rect.collidepoint(mouse_pos):
                    # Reset game variables to restart the game
                    player_x = width // 2
                    player_y = height - 220
                    is_jumping = False
                    velocity_y = 0
                    rays.clear()
                    ray_active = False
                    random_image_visible = False
                    random_image_x = random.choice([0, width - random_image.get_width()])
                    random_image2_visible = False
                    meteor_visible = False
                    game_over = False




                if exit_rect.collidepoint(mouse_pos):
                    run = False

    keys = pygame.key.get_pressed()

    if not in_menu and not game_over:

        # Player movement
        if keys[pygame.K_LEFT]:
            player_x -= player_speed
            facing_right = False
            ray_direction = 1
        if keys[pygame.K_RIGHT]:
            player_x += player_speed
            facing_right = True
            ray_direction = -1

        player_x = max(0, min(player_x, width - image.get_width()))

        # Jumping logic
        if not is_jumping:
            if keys[pygame.K_SPACE]:
                is_jumping = True
                velocity_y = player_jump_speed
        if is_jumping:
            player_y += velocity_y
            velocity_y += gravity

            if player_y >= height - 220:
                player_y = height - 220
                is_jumping = False

        # Ray shooting logic
        if keys[pygame.K_RETURN]:
            if len(rays) < 100:  # Limit the number of rays
                new_ray = {
                    'x': player_x + image.get_width() // 4,
                    'y': player_y + image.get_height() // 4 - 21,
                    'direction': ray_direction
                }
                rays.append(new_ray)
                ray_sound.play()  # Play sound when ray is fired

            # Move and update rays
        for ray in rays:
            ray['x'] += ray['direction'] * ray_speed
            if ray['x'] < 0 or ray['x'] > width:
                rays.remove(ray)  # Remove ray if it goes off the screen

            ray_rect = pygame.Rect(ray['x'], ray['y'], ray_length, ray_width)

            # Check collisions with random images
            if ray_rect.colliderect(random_image_rect):
                random_image_visible = False
                random_image_sound.stop()
                rays.remove(ray)  # Remove ray on collision with random image
            if ray_rect.colliderect(random_image2_rect):
                random_image2_visible = False
                random_image_sound.stop()
                rays.remove(ray)  # Remove ray on collision with random image 2

        # Spawn random image at random intervals
        random_spawn_timer -= delta_time
        if random_spawn_timer <= 0 and not random_image_visible:
            random_spawn_timer = random.randint(1000, 3000)
            random_image_x = random.choice([0, width - random_image.get_width()])
            random_image_y = height - random_image.get_height()
            moving_left = (random_image_x == width - random_image.get_width())
            random_image_visible = True
            random_image_instance = random_image_sound.play() # Play sound when random_image appears

            if random_image_x == 0:
                random_image_flipped = pygame.transform.flip(random_image, True, False)  # Flip horizontally
            else:
                random_image_flipped = random_image  # Use the original image

        # Move the random image horizontally
        if random_image_visible:
            if moving_left:
                random_image_x -= random_image_speed_x  # Move left
            else:
                random_image_x += random_image_speed_x  # Move right

            if random_image_x < 0 or random_image_x > width - random_image.get_width():
                random_image_visible = False
                random_image_sound.stop()

        random_image2_spawn_timer -= delta_time
        if random_image2_spawn_timer <= 0 and not random_image2_visible:
            random_image2_spawn_timer = random.randint(1000, 3000)
            random_image2_x = random.choice([0, width - random_image2.get_width()])  # Appear from the left or right
            random_image2_y = height - random_image2.get_height()  # Stay near the bottom
            random_image2_moving_left = (
                        random_image2_x == width - random_image2.get_width())  # Move left if spawned on the right
            random_image2_visible = True
            random_image2_instance = random_image_sound.play()

            if random_image2_x == 0:
                random_image2_flipped = pygame.transform.flip(random_image2, True, False)  # Flip horizontally
            else:
                random_image2_flipped = random_image2  # Use the original image

        # Move the random image 2 horizontally
        if random_image2_visible:
            if random_image2_moving_left:
                random_image2_x -= random_image2_speed_x  # Move left
            else:
                random_image2_x += random_image2_speed_x  # Move right

            if random_image2_x < 0 or random_image2_x > width - random_image2.get_width():
                random_image2_visible = False
                random_image_sound.stop()

        meteor_spawn_timer -= delta_time
        if meteor_spawn_timer <= 0 and not meteor_visible:
            meteor_spawn_timer = random.randint(1000, 3000)
            meteor_x = random.randint(0, width - meteor_image.get_width())
            meteor_y = -meteor_image.get_height()
            meteor_visible = True
            meteor_sound.play()

        if meteor_visible:
            meteor_y += meteor_speed_y
            meteor_x -= meteor_speed_x

            if meteor_y > height or meteor_x < -meteor_image.get_width():  # If meteor goes off screen
                meteor_visible = False
                meteor_sound.stop()

        ray_rect = pygame.Rect(ray_x, ray_y, ray_length, ray_width)
        random_image_rect = pygame.Rect(random_image_x, random_image_y, random_image.get_width(),
                                        random_image.get_height())
        random_image2_rect = pygame.Rect(random_image2_x, random_image2_y, random_image2.get_width(),
                                         random_image2.get_height())
        player_rect = pygame.Rect(player_x, player_y, image.get_width(), image.get_height())
        meteor_rect = pygame.Rect(meteor_x, meteor_y, meteor_image.get_width(), meteor_image.get_height())

        if ray_active:
            for ray in rays:
                ray_rect = pygame.Rect(ray['x'], ray['y'], ray_length, ray_width)
                if ray_rect.colliderect(random_image_rect):
                    random_image_visible = False
                    rays.remove(ray)  # Remove ray on collision with random image
                if ray_rect.colliderect(random_image2_rect):
                    random_image2_visible = False
                    rays.remove(ray)  # Remove ray on collision with random image 2

        # Collision detection between player and random images
        if player_rect.colliderect(random_image_rect) or player_rect.colliderect(random_image2_rect):
            game_over = True

            # Collision detection between player and meteor

    # Display Game Over screen
    if game_over:
        screen.blit(game_over_background, (0, 0))
        screen.blit(game_over_text, game_over_rect)
        screen.blit(replay_text, replay_rect)
        screen.blit(exit_text, exit_rect)
        pygame.display.flip()

        continue
    # Drawing the menu or game screen
    if in_menu:
        screen.blit(main, (0, 0))
        screen.blit(text, text_rect)
        screen.blit(text2, text2_rect)
        screen.blit(text3, text3_rect)
    else:
        screen.blit(background, (0, 0))

        if facing_right:
            screen.blit(image, (player_x, player_y))
        else:
            flipped_image = pygame.transform.flip(image, True, False)
            screen.blit(flipped_image, (player_x, player_y))

        for ray in rays:
            if ray['direction'] == 1:
                pygame.draw.line(screen, ray_color, (ray['x'], ray['y']),
                                 (ray['x'] + ray_length, ray['y']), ray_width)
            else:
                pygame.draw.line(screen, ray_color, (ray['x'], ray['y']),
                                 (ray['x'] - ray_length, ray['y']), ray_width)

        if random_image_visible:
            screen.blit(random_image_flipped, (random_image_x, random_image_y))

        if random_image2_visible:
            screen.blit(random_image2_flipped, (random_image2_x, random_image2_y))

        if meteor_visible:
            screen.blit(meteor_image, (meteor_x, meteor_y))


    pygame.display.update()

pygame.quit()

