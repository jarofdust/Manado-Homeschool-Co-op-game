import pygame

win = pygame.display.set_mode((1100, 800))
player_idle_image = pygame.transform.scale_by(
    pygame.image.load('assets/Characters/red_knight.png').convert_alpha(), 2
)
jumping_player_image = pygame.transform.scale_by(
    pygame.image.load('assets/Characters/jumping_red_knight.png').convert_alpha(), 2
)
punching_player_image = pygame.transform.scale_by(
    pygame.image.load('assets/Characters/punching_red_knight.png').convert_alpha(), 2
)

velocity_x = 0
velocity_y = 0
move_speed = 20
is_moving = False
is_jumping = False
facing = "right"
jump_hold_duration = 0
player_image = player_idle_image
gravity = 1.2
jump_initial_strength = 33
player_x = 600
player_y = 100
CLOCK = pygame.time.Clock()
    
player_image_rect = player_image.get_rect(center=(player_x, player_y)) # draws the player at the x and y positions defined
           

current_sprite = player_image

running = True
while running:


    # Event Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Jump start
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not is_jumping:
                velocity_y = -jump_initial_strength
                is_jumping = True
        

        # Jump release (cut jump short)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE and is_jumping and velocity_y < 0:
                velocity_y *= 0.5
    
    keys = pygame.key.get_pressed()  
    # sets velocity_x to zero every frame, unless a or d are pressed
    velocity_x = 0
    if keys[pygame.K_a]:
        facing = "left"
        velocity_x = - move_speed
    elif keys[pygame.K_d]:
        facing = "right"
        velocity_x = move_speed

                       # Variable jump height while holding space (holy crap this took too long if your ever trying to add vriable jump, make sure you dont accidentaly redifine your y_velocity as some random variable)
    if keys[pygame.K_SPACE] and is_jumping:  
        velocity_y -= 0.2  # Extra lift while holding
        current_sprite = jumping_player_image
        

    # moves the player left or right based on velocity_x
    player_image_rect.x += velocity_x
        # Apply gravity
    velocity_y += gravity
    player_image_rect.y += velocity_y


            
    if player_image_rect.bottom >= 700:
        player_image_rect.bottom = 700
        current_sprite = player_idle_image
        velocity_y = 0
        is_jumping = False

    if event.type == pygame.MOUSEBUTTONDOWN:
        if event.button == 1:  # left click
            # changes image
            current_sprite = punching_player_image


            # Flip the sprite image when facing left
    if facing == "left":
        player_image = pygame.transform.flip(current_sprite, True, False)
    if facing == "right":
        player_image = current_sprite
    

    pygame.display.update()
    win.fill((40, 20, 0)) 
    win.blit(player_image, player_image_rect)
    CLOCK.tick(60) # framerate
