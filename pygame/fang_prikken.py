import pygame
import random
import sys
import os

pygame.init() # Start pygame (må alltid gjøres)
W, H = 1200, 720 # Størrelse på skjerm
bilde = pygame.image.load("tull.jpg")
riktige_bilde = pygame.transform.scale(bilde, (W, H))
poeng_fil = os.path.join(os.path.dirname(__file__), "poengsum_logg.txt")

skjerm = pygame.display.set_mode((W, H))
pygame.display.set_caption("Fang de Fallende blokkene!")

#Hva skjer hvis man erndrer tallene?
HVIT, BLAA, ROD, SVART = (255, 255, 255), (0, 0, 255), (255, 0, 0), (45, 207, 102) # Farger vi bruker

# klokke og font
klokke = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)
stor_font = pygame.font.SysFont(None, 64)


def sjekk_highscore():
    if not os.path.exists(poeng_fil):
        return 0  # Ingen tidligere poengsum, så dette er en highscore
    with open(poeng_fil, "r", encoding="utf-8") as fil:
        poengsummer = [int(line.strip()) for line in fil if line.strip().isdigit()]
    return max(poengsummer) if poengsummer else 0

def lagre_poengsum(poeng):
    with open(poeng_fil, "a", encoding="utf-8") as fil:
        fil.write(f"{poeng}\n")

def reset_spill():
    # plate og blokk oppsett
    plate = pygame.Rect(W // 2 - 60, H - 20, 120, 10)
    blokk = pygame.Rect(random.randint(0, W - 20), 0, 20, 20)
    blokk_fart = 5
    poengsum = 0
    fart_plate = 16
    return plate, blokk, blokk_fart, fart_plate, poengsum

plate, blokk, blokk_fart, fart_plate, poengsum = reset_spill()
high_score = sjekk_highscore()

pause_valg = ["Fortsett", "Start pa nytt", "Avslutt"]
game_over_valg = ["Start pa nytt", "Avslutt"]
valgt_index = 0
paused = False
game_over_aktiv = False

key_up = (pygame.K_w, pygame.K_UP)
key_down = (pygame.K_s, pygame.K_DOWN)
key_select = (pygame.K_RETURN, pygame.K_KP_ENTER)
key_escape = (pygame.K_p, pygame.K_ESCAPE)

# Game loop
run = True
while run:
    skjerm.fill(SVART)
    #skjerm.blit(bilde, (0, 0))
    skjerm.blit(riktige_bilde, (0, 0))

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if e.type == pygame.KEYDOWN:
            if e.key in (pygame.K_p, pygame.K_ESCAPE):
                if not game_over_aktiv:
                    paused = not paused
            elif paused:
                aktive_valg = game_over_valg if game_over_aktiv else pause_valg
                if e.key in (pygame.K_w, pygame.K_UP):
                    valgt_index = (valgt_index - 1) % len(aktive_valg)
                elif e.key in (pygame.K_s, pygame.K_DOWN):
                    valgt_index = (valgt_index + 1) % len(aktive_valg)
                elif e.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                    valgt = aktive_valg[valgt_index]
                    if valgt == "Fortsett":
                        paused = False
                    elif valgt == "Start pa nytt":
                        plate, blokk, blokk_fart, fart_plate, poengsum = reset_spill()
                        paused = False
                        game_over_aktiv = False
                        valgt_index = 0
                    elif valgt == "Avslutt":
                        pygame.quit()
                        sys.exit()

    if not paused:
        # plate bevegelse
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and plate.left > 0:
            plate.move_ip(-fart_plate, 0)
        if keys[pygame.K_d] and plate.right < W:
            plate.move_ip(fart_plate, 0)

        # flytt blokk
        blokk.y += blokk_fart

        # Hvis blokken blir fanget
        if blokk.colliderect(plate):
            blokk.y = 0
            blokk.x = random.randint(0, W - 20)
            poengsum += 1
            blokk_fart += 0.5  # ok fart

        # Game over logikk
        # Hvis blokken ikke blir fanget
        if blokk.y > H:
            paused = True
            game_over_aktiv = True
            valgt_index = 0
            lagre_poengsum(poengsum)
            high_score = sjekk_highscore()


    # Tegn alt
    pygame.draw.rect(skjerm, HVIT, plate)
    pygame.draw.rect(skjerm, BLAA, blokk)

    # Vis poengsum
    poengsum_text = font.render(f"Poengsum: {poengsum}", True, HVIT)
    skjerm.blit(poengsum_text, (10, 10))

    # Vis highscore
    high_score_text = font.render(f"Highscore: {high_score}", True, HVIT)
    skjerm.blit(high_score_text, (10, 40))

    if paused:
        # Mørkt lag over spillet når pausemenyen vises.
        overlay = pygame.Surface((W, H), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        skjerm.blit(overlay, (0, 0))

        if game_over_aktiv:
            aktive_valg = game_over_valg
            tittel_text = "GAME OVER"
        else:
            aktive_valg = pause_valg
            tittel_text = "PAUSE"

        # aktive_valg = game_over_valg if game_over_aktiv else pause_valg
        # tittel_text = "GAME OVER" if game_over_aktiv else "PAUSE"
        tittel = stor_font.render(tittel_text, True, HVIT)
        skjerm.blit(tittel, (W // 2 - tittel.get_width() // 2, H // 2 - 150))

        if game_over_aktiv:
            slutt_poeng = font.render(f"Poengsum: {poengsum}", True, ROD)
            skjerm.blit(slutt_poeng, (W // 2 - slutt_poeng.get_width() // 2, H // 2 - 90))
            hjelp_text = "W/S eller piler: velg - Enter: bekreft"
        else:
            hjelp_text = "P/ESC: lukk meny - W/S eller piler: velg - Enter: bekreft"

        hjelp = font.render(hjelp_text, True, HVIT)
        skjerm.blit(hjelp, (W // 2 - hjelp.get_width() // 2, H // 2 + 90))

        for i, tekst in enumerate(aktive_valg):
            farge = BLAA if i == valgt_index else HVIT
            valg_tekst = font.render(tekst, True, farge)
            skjerm.blit(valg_tekst, (W // 2 - valg_tekst.get_width() // 2, H // 2 - 40 + i * 40))

    pygame.display.flip()
    klokke.tick(60)
