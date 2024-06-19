import sys
import pygame
import random
import math
from GIFImage import GIFImage
from Zombie import Zombie
from ZombieType import ZombieType
from Player import Player
import Gun
from Gun import Level

# Game Control until we have the code to control bullet damage and reload/speed per gun and Gif.
screen_width = 1200
screen_height = 700
player_speed = 6
initial_bullet_speed = 5

z1 = ZombieType("zombie1", 3, 6, 1, 1)
z2 = ZombieType("zombie2", 9, 4, 3, 2)

class Bullet:
    def __init__(self, x, y, speed, damage):
        self.x = x
        self.y = y
        self.damage = damage
        self.speed = speed

class Particle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = pygame.image.load("particles.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (40, 40))  # Make the particle smaller
        self.timer = 5000  # Particle effect duration in milliseconds

    def update(self, dt):
        self.timer -= dt

    def render(self, screen):
        screen.blit(self.image, (self.x, self.y))

def moveZombieAuto(zombie: Zombie, player: Player):
    if zombie.x > screen_width - 100:
        zombie.isXForward = True

    if zombie.isXForward:
        zombie.x -= zombie.speed
        if zombie.x < 5:
            player.hp -= zombie.damage
            zombie.x = screen_width + random.randint(0, 100)
    else:
        zombie.x += zombie.speed

def printZombie(screen, gifImg, zombie):
    gifImg.render(screen, (zombie.x, zombie.y))

def checkCollision(bullet: Bullet, zombies: list[Zombie]):
    for zombie in zombies:
        distance = math.sqrt((bullet.x - zombie.x) ** 2 + (bullet.y - zombie.y) ** 2)
        if distance < 40:
            zombie.hp -= bullet.damage
            return True

    if bullet.x > screen_width or bullet.x < 0 or bullet.y > screen_height or bullet.y < 0:
        return True

    return False

def drawBackground(backgroundNo, screen):
    if backgroundNo == 0:
        bg = pygame.image.load("bg.jpeg").convert()
        bg = pygame.transform.scale(bg, (screen_width, screen_height))
    elif backgroundNo == 1:
        bg = pygame.image.load("bg2.png").convert()
        bg = pygame.transform.scale(bg, (screen_width, screen_height))
    else:
        bg = pygame.image.load("bg3.png").convert()
        bg = pygame.transform.scale(bg, (screen_width, screen_height))

    screen.blit(bg, (0, 0))

def endScene(screen, myfont, score, coins):
    screen.fill((0, 0, 0))  # Fill screen with black color

    endText1 = myfont.render("Game Over!", True, (255, 255, 255))
    endText2 = myfont.render(f"Final Score: {score}", True, (255, 255, 255))
    endText3 = myfont.render(f"Coins Collected: {coins}", True, (255, 255, 255))
    endText4 = myfont.render("Press any key to restart.", True, (255, 255, 255))

    screen.blit(endText1, (screen_width // 3, screen_height // 4))
    screen.blit(endText2, (screen_width // 3, screen_height // 4 + 50))
    screen.blit(endText3, (screen_width // 3, screen_height // 4 + 100))
    screen.blit(endText4, (screen_width // 3, screen_height // 4 + 150))

    pygame.display.update()

def startScene(screen, myfont):
    screen.fill((0, 0, 0))  # Fill screen with black color

    titleText = myfont.render("Zombie Shooter Game", True, (255, 255, 255))
    instructionText1 = myfont.render("Instructions:", True, (255, 255, 255))
    instructionText2 = myfont.render("Use arrow keys to move", True, (255, 255, 255))
    instructionText3 = myfont.render("Press space to shoot", True, (255, 255, 255))
    startText = myfont.render("Press any key to start", True, (255, 255, 255))

    screen.blit(titleText, (screen_width // 4, screen_height // 4))
    screen.blit(instructionText1, (screen_width // 4, screen_height // 4 + 50))
    screen.blit(instructionText2, (screen_width // 4, screen_height // 4 + 100))
    screen.blit(instructionText3, (screen_width // 4, screen_height // 4 + 150))
    screen.blit(startText, (screen_width // 4, screen_height // 4 + 250))

    pygame.display.update()

def mapSelectionScene(screen, myfont):
    screen.fill((0, 0, 0))  # Fill screen with black color

    titleText = myfont.render("Map Selection", True, (255, 255, 255))
    instructionText = myfont.render("Choose a map: 1, 2, or 3", True, (255, 255, 255))

    screen.blit(titleText, (screen_width // 4, screen_height // 4))
    screen.blit(instructionText, (screen_width // 4, screen_height // 4 + 50))

    pygame.display.update()

class Player:
    def __init__(self):
        self.x = 100
        self.y = 100
        self.hp = 25
        self.score = 0
        self.coin = 0
        self.level = 1
        self.attack = 3
        self.gold_for_next_level = 10
        self.last_shot_time = 0
        self.shot_delay = 450  # Shot delay in milliseconds
        self.speed = 15

    def level_up(self):
        self.level += 1
        self.hp += 5
        self.attack += 2
        self.gold_for_next_level *= 2  # Increase the required gold for next level
        self.shot_delay -= 5
        self.speed += 2
def main():
    player = Player()

    pygame.init()

    player1 = pygame.image.load("LVL1 Archer Shooting.gif")
    player1 = pygame.transform.scale(player1, (150, 80))
    bullet1 = pygame.image.load("ArrowLvl1.gif")
    bullet1 = pygame.transform.scale(bullet1, (40, 70))

    zombie1Gif = GIFImage("zombie1.gif")
    zombie1Gif.set_scale(0.05)
    zombie2Gif = GIFImage("zombie2.gif")
    zombie2Gif.set_scale(0.2)

    player1Gif = GIFImage("LVL1 Archer Shooting.gif")
    player1Gif.set_scale(0.15)

    pygame.font.init()
    myfont = pygame.font.SysFont('Phosphate', 30)

    pygame.display.set_caption("Zombie Shooter Game")
    screen = pygame.display.set_mode((screen_width, screen_height))

    running = True
    startGame = False  # Flag to track if the game has started
    gameOver = False   # Flag to track game over state
    mapSelected = False  # Flag to track if a map is selected

    zombies = []
    for i in range(0, 2):  # Start with 2 zombies
        zombie = Zombie(z1, screen_width + random.randint(0, 100), random.randint(50, screen_height - 100))
        zombies.append(zombie)

    bulletList = []
    keypressed = False
    bulletFired = False
    bulletAnimationCount = 0

    backgroundNo = 0  # Default background
    showGuideFlag = False

    particles = []

    clock = pygame.time.Clock()
    spawn_time = 0  # Timer to track when to spawn new zombies
    spawn_interval = 5000  # Spawn new zombies every 5 seconds

    while running:
        dt = clock.tick(60)  # Get the time elapsed since last frame in milliseconds
        spawn_time += dt  # Increment the spawn timer
        keypressed = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                keypressed = True

        if not startGame:
            startScene(screen, myfont)

            for event in pygame.event.get():  # Wait for key press to start the game
                if event.type == pygame.KEYDOWN:
                    startGame = True
                    break

        elif startGame and not mapSelected:
            mapSelectionScene(screen, myfont)

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        backgroundNo = 0
                        mapSelected = True
                    elif event.key == pygame.K_2:
                        backgroundNo = 1
                        mapSelected = True
                    elif event.key == pygame.K_3:
                        backgroundNo = 2
                        mapSelected = True

        if gameOver:
            endScene(screen, myfont, player.score, player.coin)
            pygame.time.wait(2000)  # Wait for 2 seconds

            for event in pygame.event.get():  # Clear the event queue
                if event.type == pygame.KEYDOWN:
                    gameOver = False  # Reset game state
                    player.score = 0  # Reset score
                    player.coin = 0   # Reset coins
                    player.hp = 25   # Reset health
                    player.level = 1  # Reset level
                    player.attack = 3  # Reset attack
                    player.gold_for_next_level = 10  # Reset gold for next level
                    zombies.clear()   # Clear zombies
                    bulletList.clear() # Clear bullets
                    backgroundNo = random.randint(0, 2)  # Change background
                    spawn_time = 0  # Reset spawn timer

        if startGame and mapSelected and not gameOver:
            drawBackground(backgroundNo, screen)

            if spawn_time > spawn_interval:  # Time to spawn new zombies
                for i in range(player.level):  # Increase the number of zombies spawned based on player level
                    zombie_type = random.choice([z1, z2])
                    zombie_type.hp += player.level * 2  # Increase zombie health per player level
                    zombie_type.damage += player.level  # Increase zombie damage per player level
                    zombie = Zombie(zombie_type, screen_width + random.randint(0, 100), random.randint(50, screen_height - 100))
                    zombies.append(zombie)
                spawn_time = 0  # Reset spawn timer

            dead_zombies = []
            for zombie in zombies:
                if zombie.hp <= 0:
                    dead_zombies.append(zombie)
                    player.score += 1
                    player.coin += zombie.coin
                    particles.append(Particle(zombie.x, zombie.y))  # Add particle effect on zombie death
                else:
                    moveZombieAuto(zombie, player)
                    if zombie.zombieImageName == "zombie1":
                        printZombie(screen, zombie1Gif, zombie)
                    elif zombie.zombieImageName == "zombie2":
                        printZombie(screen, zombie2Gif, zombie)

            for zombie in dead_zombies:
                zombies.remove(zombie)

            # Check for player leveling up
            if player.coin >= player.gold_for_next_level:
                player.level_up()

            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP]:
                player.y -= player_speed
            if keys[pygame.K_DOWN]:
                player.y += player_speed
            if keys[pygame.K_k]:
                showGuideFlag = not showGuideFlag

            player.x = max(0, min(player.x, screen_width - 80))
            player.y = max(0, min(player.y, screen_height - 80))

            current_time = pygame.time.get_ticks()
            if keys[pygame.K_SPACE] and current_time - player.last_shot_time > player.shot_delay:
                bulletList.append(Bullet(player.x, player.y, initial_bullet_speed, player.attack))  # Use player's attack for bullet damage
                bulletFired = True
                bulletAnimationCount = 0
                player1Gif.seek(0)
                player.last_shot_time = current_time

            if bulletFired:
                player1Gif.render(screen, (player.x, player.y))
                bulletAnimationCount += 1

                if bulletAnimationCount > 105:
                    bulletFired = False
            else:
                screen.blit(player1, (player.x, player.y))

            for bullet in bulletList:
                if checkCollision(bullet, zombies):
                    bulletList.remove(bullet)
                else:
                    screen.blit(bullet1, (bullet.x, bullet.y))
                    bullet.x += bullet.speed

                    if bullet.x > screen_width or bullet.x < 0 or bullet.y > screen_height or bullet.y < 0:
                        bulletList.remove(bullet)

            textsurface = myfont.render(f"score: {player.score} coin: {player.coin} hp: {player.hp} level: {player.level}", False, (0, 0, 0))

            for particle in particles:
                particle.update(dt)
                particle.render(screen)

            particles = [p for p in particles if p.timer > 0]  # Remove particles whose timer is up

            if showGuideFlag:
                label = myfont.render("".join(README), False, (0, 0, 0))
                screen.blit(label, (100, 100))

            screen.blit(textsurface, (0, 0))

            if player.hp < 0:
                gameOver = True  # Set game over flag

            pygame.display.update()

if __name__ == "__main__":
    main()
