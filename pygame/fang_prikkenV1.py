import pygame
import random
import sys
import os

pygame.init() # Start pygame (må alltid gjøres)
W, H = 1200, 720 # Størrelse på skjerm
poeng_fil = os.path.join(os.path.dirname(__file__), "poengsum_logg.txt")
# Legge inn bilde
bilde = pygame.image.load("bakgrunn.jpg")
riktige_bilde = pygame.transform.scale(bilde, (W, H))

skjerm = pygame.display.set_mode((W, H))
pygame.display.set_caption("Fang de Fallende blokkene!")

#Hva skjer hvis man erndrer tallene?
HVIT, FARGE, ROD, SVART = (255, 255, 255), (34, 200, 96), (255, 0, 0), (0, 0, 0) # Farger vi bruker

# klokke og font
klokke = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)

# plate og blokk oppsett
plate = pygame.Rect(W // 2 - 60, H - 20, 120, 10)
blokk = pygame.Rect(random.randint(0, W - 20), 0, 20, 20)
blokk_fart = 5
fart_plate = 16
poengsum = 0 # poengsum

def lagre_poengsum(poeng):
    with open(poeng_fil, "a", encoding="utf-8") as fil:
        fil.write(f"{poeng}\n")

def sjekk_highscore():
    if not os.path.exists(poeng_fil):
        return 0  # Ingen tidligere poengsum, så dette er en highscore
    with open(poeng_fil, "r", encoding="utf-8") as fil:
        poengsummer = [int(line.strip()) for line in fil if line.strip().isdigit()]
    return max(poengsummer) if poengsummer else 0

high_score = sjekk_highscore()

# Game loop
run = True
while run:
    skjerm.fill(SVART)
    skjerm.blit(riktige_bilde, (0, 0))

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
        lagre_poengsum(poengsum)
        high_score = sjekk_highscore()

    # Tegn alt
    pygame.draw.rect(skjerm, HVIT, plate)
    pygame.draw.rect(skjerm, FARGE, blokk)

    # Vis poengsum
    poengsum_text = font.render(f"Poengsum: {poengsum}", True, HVIT)
    skjerm.blit(poengsum_text, (10, 10))

    # Vis highscore
    high_score_text = font.render(f"Highscore: {high_score}", True, HVIT)
    skjerm.blit(high_score_text, (10, 40))

    pygame.display.flip()
    klokke.tick(60)