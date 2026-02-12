import pygame
import random
import sys

pygame.init() # Start pygame (må alltid gjøres)
W, H = 600, 600 # Størrelse på skjerm

skjerm = pygame.display.set_mode((W, H))
pygame.display.set_caption("Fang de Fallende blokkene!")

#Hva skjer hvis man erndrer tallene?
HVIT, BLAA, ROD, SVART = (255, 255, 255), (0, 200, 255), (255, 0, 0), (0, 0, 0) # Farger vi bruker

# klokke og font
klokke = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)

# plate og blokk oppsett
plate = pygame.Rect(W // 2 - 60, H - 20, 120, 10)
blokk = pygame.Rect(random.randint(0, W - 20), 0, 20, 20)
blokk_fart = 5
fart_plate = 16
poengsum = 0 # poengsum

# Game loop
run = True
while run:
    skjerm.fill(SVART)

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # plate bevegelse
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and plate.left > 0:
        plate.move_ip(-fart_plate, 0)
    if keys[pygame.K_RIGHT] and plate.right < W:
        plate.move_ip(fart_plate, 0)

    # flytt blokk
    blokk.y += blokk_fart

    # Hvis blokken blir fanget
    if blokk.colliderect(plate):
        blokk.y = 0
        blokk.x = random.randint(0, W - 20)
        poengsum += 1
        blokk_fart += 0.5  # øk fart

    # Hvis blokken ikke blir fanget
    if blokk.y > H:
        game_over = font.render(f"Game Over!  Poengsum: {poengsum}", True, ROD)
        skjerm.blit(game_over, (W // 2 - 150, H // 2))
        pygame.display.flip()
        pygame.time.wait(2000)
        run = False

    # Tegn alt
    pygame.draw.rect(skjerm, HVIT, plate)
    pygame.draw.rect(skjerm, BLAA, blokk)

    # Vis poengsum
    poengsum_text = font.render(f"Poengsum: {poengsum}", True, HVIT)
    skjerm.blit(poengsum_text, (10, 10))

    pygame.display.flip()
    klokke.tick(60)