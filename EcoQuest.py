import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
ITEM_SIZE = 20
WHITE = (255, 255, 255)
BROWN = (165, 42, 42)
GREEN = (0, 128, 0)
SAND = (244, 164, 96)
GRAY = (128, 128, 128)

# Classes
class Player:
    def __init__(self):
        self.x = SCREEN_WIDTH // 2
        self.y = SCREEN_HEIGHT // 2

    def move(self, dx, dy):
        self.x += dx
        self.y += dy
        # Ensure player stays within bounds
        self.x = max(0, min(SCREEN_WIDTH, self.x))
        self.y = max(0, min(SCREEN_HEIGHT, self.y))

    def draw(self, screen):
        pygame.draw.circle(screen, WHITE, (self.x, self.y), 20)

class Item:
    def __init__(self):
        self.x = random.randint(ITEM_SIZE, SCREEN_WIDTH - ITEM_SIZE)  # Avoid edges
        self.y = random.randint(ITEM_SIZE, SCREEN_HEIGHT - ITEM_SIZE)  # Avoid edges

    def draw(self, screen):
        pygame.draw.rect(screen, BROWN, (self.x, self.y, ITEM_SIZE, ITEM_SIZE))

# Main function
def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Item Collector")

    player = Player()
    items = []
    item_collected = False
    item_timer = 0
    time_left = 10
    level = 1

    clock = pygame.time.Clock()

    levels = [
        {"background_color": GREEN, "items_to_collect": 1},
        {"background_color": SAND, "items_to_collect": 1},
        {"background_color": GRAY, "items_to_collect": 1}
    ]

    # Game loop
    running = True
    while running:
        screen.fill(levels[level-1]["background_color"])

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Show start menu or countdown
        if not item_collected:
            if level < len(levels):
                font = pygame.font.Font(None, 36)
                if level == 1:
                    text = font.render("Press SPACE to start the game!", True, WHITE)
                else:
                    text = font.render("Get ready for Level " + str(level), True, WHITE)
                text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
                screen.blit(text, text_rect)
                pygame.display.flip()
                pygame.time.delay(1000)
                for i in range(3, 0, -1):
                    screen.fill(levels[level-1]["background_color"])
                    text = font.render(str(i), True, WHITE)
                    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
                    screen.blit(text, text_rect)
                    pygame.display.flip()
                    pygame.time.delay(1000)
            else:
                font = pygame.font.Font(None, 36)
                text = font.render("Get ready for the next level! " + str(level), True, WHITE)
                text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
                screen.blit(text, text_rect)
                pygame.display.flip()
                pygame.time.delay(1000)
                for i in range(3, 0, -1):
                    screen.fill(levels[level-1]["background_color"])
                    text = font.render(str(i), True, WHITE)
                    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
                    screen.blit(text, text_rect)
                    pygame.display.flip()
                    pygame.time.delay(1000)

            item_collected = True

        # Game logic
        if item_collected:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_a]:
                player.move(-8, 0)
            if keys[pygame.K_d]:
                player.move(8, 0)
            if keys[pygame.K_w]:
                player.move(0, -8)
            if keys[pygame.K_s]:
                player.move(0, 8)

            player.draw(screen)

            if len(items) == 0:
                if item_timer == 0:
                    items.append(Item())
                    item_timer = pygame.time.get_ticks()
                elif pygame.time.get_ticks() - item_timer >= 2500:  # Timer for item spawn (2.5 seconds)
                    items.append(Item())
                    item_timer = pygame.time.get_ticks()

            for item in items:
                item.draw(screen)
                if pygame.Rect(item.x, item.y, ITEM_SIZE, ITEM_SIZE).colliderect(
                        pygame.Rect(player.x, player.y, 20, 20)):
                    items.remove(item)
                    if len(items) == 0:
                        levels[level - 1]["items_to_collect"] -= 1
                        time_left = 10  # Reset time left
                        if levels[level - 1]["items_to_collect"] == 0:
                            if level < len(levels):
                                level += 1
                                item_collected = False
                            else:
                                font = pygame.font.Font(None, 36)
                                text = font.render("You Win! Press Q to quit or R to restart", True, WHITE)
                                text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
                                screen.blit(text, text_rect)
                                pygame.display.flip()
                                while True:  # Wait for user to press Q or R
                                    for event in pygame.event.get():
                                        if event.type == pygame.KEYDOWN:
                                            if event.key == pygame.K_q:
                                                running = False
                                                break
                                            elif event.key == pygame.K_r:
                                                level = 1
                                                item_collected = False
                                                break

        # Display GUI
        font = pygame.font.Font(None, 24)
        text = font.render(f"Amount of Trash to collect: {max(levels[level-1]['items_to_collect'], 0)}", True, WHITE)
        screen.blit(text, (10, 10))

        text = font.render(f"Time Left: {int(max(time_left, 0))}", True, WHITE)  # Cast time_left to int
        screen.blit(text, (10, 40))

        # Timer countdown
        if item_collected:
            time_left -= clock.get_time() / 1000  # Convert milliseconds to seconds

            if time_left <= 0:
                font = pygame.font.Font(None, 36)
                text = font.render("You lost! The environment got polluted.", True, WHITE)
                text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
                screen.blit(text, text_rect)
                pygame.display.flip()
                pygame.time.delay(2000)
                running = False

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()
