import pygame
from constants import screen_width, screen_height

def start_scene(screen, myfont):
    screen.fill((0, 0, 0))  # Fill screen with black color

    title_text = myfont.render("Zombie Shooter Game", True, (255, 255, 255))
    instruction_text1 = myfont.render("Instructions:", True, (255, 255, 255))
    instruction_text2 = myfont.render("Use arrow keys to move", True, (255, 255, 255))
    instruction_text3 = myfont.render("Press space to shoot", True, (255, 255, 255))
    start_text = myfont.render("Press any key to start", True, (255, 255, 255))

    screen.blit(title_text, (screen_width // 4, screen_height // 4))
    screen.blit(instruction_text1, (screen_width // 4, screen_height // 4 + 50))
    screen.blit(instruction_text2, (screen_width // 4, screen_height // 4 + 100))
    screen.blit(instruction_text3, (screen_width // 4, screen_height // 4 + 150))
    screen.blit(start_text, (screen_width // 4, screen_height // 4 + 250))

    pygame.display.update()
