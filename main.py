import pygame
import random
import asyncio

pygame.init()

WIDTH, HEIGHT = 800, 600
BACKGROUND = (135, 206, 235) 
PLATFORM_COLOR = (139, 69, 19)
TEXT_COLOR = (255, 255, 255)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tung the Cupcake Collector")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)

player_image = pygame.image.load("assets/tung.png").convert_alpha()
player_image = pygame.transform.scale(player_image, (50, 50))
cupcake_image = pygame.image.load("assets/cupcake.png").convert_alpha()
cupcake_image = pygame.transform.scale(cupcake_image, (30, 30))

platforms = [
    pygame.Rect(0, HEIGHT - 30, WIDTH, 30),
    pygame.Rect(150, HEIGHT - 150, 200, 20),
    pygame.Rect(460, HEIGHT - 250, 200, 20),
    pygame.Rect(100, HEIGHT - 450, 200, 20),
    pygame.Rect(200, HEIGHT - 300, 100, 20),
    pygame.Rect(600, HEIGHT - 400, 150, 20)
]

cupcakes = [
    pygame.Rect(random.randint(0, WIDTH - 30), random.randint(0, HEIGHT - 100), 30, 30) for _ in range(5)
]

async def main():
    player_rect = pygame.Rect(50, 300, 50, 50)
    player_dy = 0.0
    gravity = 0.5
    jump_strength = -10
    max_jumps = 2
    jumps_left = max_jumps
    score = 0

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and jumps_left > 0:
                    player_dy = jump_strength
                    jumps_left -= 1
            
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player_rect.x -= 5
        if keys[pygame.K_RIGHT]:
            player_rect.x += 5

        # Vertical velocity & gravity
        player_dy += gravity
        player_rect.y += int(player_dy)

        # Window collisions
        if player_rect.left < 0:
            player_rect.left = 0
        if player_rect.right > WIDTH:
            player_rect.right = WIDTH
        if player_rect.top < 0:
            player_rect.top = 0
            player_dy = 0
        
        # Platform collisions
        for platform in platforms:
            if player_rect.colliderect(platform) and player_dy >= 0:
                player_rect.bottom = platform.top
                player_dy = 0
                jumps_left = max_jumps
            elif player_dy < 0 and player_rect.colliderect(platform):
                player_rect.top = platform.bottom
                player_dy = 0

        # Cupcake collisions
        for cupcake in cupcakes[:]:
            if player_rect.colliderect(cupcake):
                cupcakes.remove(cupcake)
                cupcakes.append(pygame.Rect(random.randint(0, WIDTH - 30), random.randint(0, HEIGHT - 100), 30, 30))
                score += 1

        # Drawing
        screen.fill(BACKGROUND)

        for platform in platforms:
            pygame.draw.rect(screen, PLATFORM_COLOR, platform)

        for cupcake in cupcakes:
            screen.blit(cupcake_image, cupcake)

        screen.blit(player_image, player_rect)

        score_text = font.render(f"Score: {score}", True, TEXT_COLOR)
        screen.blit(score_text, (10, 10))

        pygame.display.flip()
        clock.tick(60)
        await asyncio.sleep(0)

    pygame.quit()

asyncio.run(main())