import pygame, random, time
pygame.init()
pygame.mixer.init()

# ====================== MUSIC & SFX ======================
pygame.mixer.music.load("backsound.mp3.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)  # Loop selamanya

sound_true = pygame.mixer.Sound("truee.mp3.mp3")
sound_false = pygame.mixer.Sound("false.mp3.mp3")

# SETUP WINDOW 
WIDTH, HEIGHT = 1200, 700
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("EcoSort – Game")

# FONT 
title_font = pygame.font.Font(None, 140)
subtitle_font = pygame.font.Font(None, 60)
button_font = pygame.font.Font(None, 70)

font_med = pygame.font.Font(None, 40)
font_big = pygame.font.Font(None, 120)
font_small = pygame.font.Font(None, 40)

# COLORS 
BG = (5, 7, 10)
WHITE = (240, 240, 240)
BLACK = (0, 0, 0)
PINK = (230, 60, 130)

GREEN = (80, 200, 80)
BLUE = (80, 160, 255)
YELLOW = (240, 190, 20)
RED = (240, 80, 80)

# BACKGROUND
def draw_cartoon_background(surface):
    sky = (135, 206, 235)
    grass = (100, 200, 70)
    mountain1 = (120, 160, 220)
    mountain2 = (90, 130, 200)
    tree_brown = (139, 69, 19)
    tree_green = (34, 139, 34)

    W, H = surface.get_width(), surface.get_height()

    surface.fill(sky)

    pygame.draw.polygon(surface, mountain1,
        [(0, H*0.6), (W*0.3, H*0.3), (W*0.6, H*0.6)]
    )
    pygame.draw.polygon(surface, mountain2,
        [(W*0.3, H*0.6), (W*0.65, H*0.35), (W, H*0.6)]
    )

    pygame.draw.rect(surface, grass, (0, H*0.6, W, H))

    pygame.draw.rect(surface, tree_brown, (100, H*0.45, 40, 150))
    pygame.draw.ellipse(surface, tree_green, (50, H*0.32, 140, 120))


# SAMPAH
TRASH_TYPES = {
    "Daun Kering": "Organik",
    "Sisa Makanan": "Organik",
    "Kulit Pisang": "Organik",
    "Kulit Telur": "Organik",
    "Ampas Kopi": "Organik",
    "Sayur Busuk": "Organik",
    "Buah Busuk": "Organik",
    "Ranting Pohon": "Organik",
    "Botol Plastik": "Plastik",
    "Kantong Plastik": "Plastik",
    "Sedotan Plastik": "Plastik",
    "Gelas Plastik": "Plastik",
    "Pembungkus Snack": "Plastik",
    "Tutup Botol": "Plastik",
    "Wadah Makanan Plastik": "Plastik",
    "Bubble Wrap": "Plastik",
    "Koran": "Kertas",
    "Kardus": "Kertas",
    "Tisu Kering": "Kertas",
    "Kertas HVS": "Kertas",
    "Buku Bekas": "Kertas",
    "Majalah": "Kertas",
    "Kotak Makanan Kertas": "Kertas",
    "Kaleng": "Logam",
    "Sendok Besi": "Logam",
    "Kaleng Minuman": "Logam",
    "Paku": "Logam",
    "Tutupan Kaleng": "Logam",
    "Aluminium Foil": "Logam",
    "Kunci Lapis Besi": "Logam"
}

BIN_COLORS = {
    "Organik": GREEN,
    "Plastik": YELLOW,
    "Kertas": BLUE,
    "Logam": RED
}

STATE = "menu"
score = 0
lives = 3
attempt = 0
max_attempt = 20

def spawn_trash():
    return random.choice(list(TRASH_TYPES.keys()))

current_trash = spawn_trash()

# Position & movement
trash_y = -50
trash_speed = 4

# POPUP
popup_active = False
popup_start_time = 0
POPUP_DURATION = 0.8

popup_wrong = False
popup_wrong_start = 0
WRONG_DURATION = 0.8


def draw_button(x, y, text):
    rect = pygame.Rect(x, y, 300, 90)
    pygame.draw.rect(window, PINK, rect, border_radius=40)
    pygame.draw.rect(window, BLACK, rect, 6, border_radius=40)
    label = button_font.render(text, True, BLACK)
    window.blit(label, (x + (300 - label.get_width())//2, y + 18))
    return rect


def draw_bins():
    x = 120
    bins = {}

    for category, color in BIN_COLORS.items():
        pygame.draw.rect(window, BLACK, (x + 8, 505 + 8, 220, 180), border_radius=30)
        body_rect = pygame.Rect(x, 505, 220, 180)

        pygame.draw.rect(window, color, body_rect, border_radius=30)
        pygame.draw.rect(window, BLACK, body_rect, 5, border_radius=30)

        txt = font_small.render(category, True, BLACK)
        window.blit(txt, (x + 55, 575))

        bins[category] = body_rect
        x += 260

    return bins


def draw_popup_correct():
    popup_rect = pygame.Rect(WIDTH//2 - 160, HEIGHT//2 - 150, 320, 300)
    pygame.draw.rect(window, WHITE, popup_rect, border_radius=40)
    msg = font_med.render("Benar!", True, BLACK)
    pts = font_small.render("+1 poin", True, BLACK)
    window.blit(msg, (WIDTH//2 - msg.get_width()//2, HEIGHT//2 + 40))
    window.blit(pts, (WIDTH//2 - pts.get_width()//2, HEIGHT//2 + 90))


def draw_popup_wrong():
    popup_rect = pygame.Rect(WIDTH//2 - 160, HEIGHT//2 - 150, 320, 300)
    pygame.draw.rect(window, (255, 120, 120), popup_rect, border_radius=40)
    msg = font_med.render("Salah!", True, BLACK)
    window.blit(msg, (WIDTH//2 - msg.get_width()//2, HEIGHT//2 + 40))



# MAIN LOOP 
running = True
clock = pygame.time.Clock()
bin_rects = {}

while running:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False

        if e.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()

            if STATE == "menu":
                if start_btn.collidepoint((mx, my)):
                    STATE = "game"

            elif STATE == "game" and not popup_active and not popup_wrong:
                for cat, rect in bin_rects.items():
                    if rect.collidepoint((mx, my)):

                        attempt += 1

                        if TRASH_TYPES[current_trash] == cat:
                            score += 1
                            sound_true.play()       # <<<<<< SUARA BENAR
                            popup_active = True
                            popup_start_time = time.time()
                        else:
                            lives -= 1
                            sound_false.play()      # <<<<<< SUARA SALAH
                            popup_wrong = True
                            popup_wrong_start = time.time()

                        if lives <= 0:
                            STATE = "gameover"
                        elif attempt >= max_attempt:
                            STATE = "winner"
                        else:
                            current_trash = spawn_trash()
                            trash_y = -50

            elif STATE in ["gameover", "winner"]:
                if restart_btn.collidepoint((mx, my)):
                    score = 0
                    lives = 3
                    attempt = 0
                    current_trash = spawn_trash()
                    trash_y = -50
                    STATE = "game"

    # Popup timer
    if popup_active and time.time() - popup_start_time > POPUP_DURATION:
        popup_active = False
    if popup_wrong and time.time() - popup_wrong_start > WRONG_DURATION:
        popup_wrong = False

    # MENU
    if STATE == "menu":
        draw_cartoon_background(window)

        eco = title_font.render("Eco", True, WHITE)
        sort = title_font.render("Sort", True, WHITE)

        total_width = eco.get_width() + sort.get_width() + 20
        eco_x = WIDTH//2 - total_width//2
        sort_x = eco_x + eco.get_width() + 20

        window.blit(eco, (eco_x, 330))
        window.blit(sort, (sort_x, 330))

        subtitle = subtitle_font.render("Petualangan Pemilah Sampah", True, WHITE)
        window.blit(subtitle, (WIDTH//2 - subtitle.get_width()//2, 430))

        start_btn = draw_button(WIDTH//2 - 150, 520, "START")

    # GAME
    elif STATE == "game":
        draw_cartoon_background(window)

        # --- Sampah jatuh ---
        trash_text = title_font.render(current_trash, True, BLACK)
        trash_y += trash_speed
        window.blit(trash_text, (WIDTH//2 - trash_text.get_width()//2, trash_y))

        # Jika sampah jatuh sampai tanah → dianggap salah
        if trash_y > 480 and not (popup_active or popup_wrong):
            lives -= 1
            attempt += 1

            sound_false.play()   # <<<<<< SUARA SALAH JIKA JATUH

            if lives <= 0:
                STATE = "gameover"
            elif attempt >= max_attempt:
                STATE = "winner"
            else:
                current_trash = spawn_trash()
                trash_y = -50

        # Tempat sampah
        bin_rects = draw_bins()

        # UI
        s = font_med.render(f"Skor: {score}", True, BLACK)
        l = font_med.render(f"Nyawa: {lives}", True, BLACK)
        a = font_med.render(f"Percobaan: {attempt}/{max_attempt}", True, BLACK)

        window.blit(s, (40, 25))
        window.blit(l, (40, 70))
        window.blit(a, (40, 115))

        # Popup
        if popup_active:
            draw_popup_correct()
        if popup_wrong:
            draw_popup_wrong()

    # GAME OVER
    elif STATE == "gameover":
        draw_cartoon_background(window)
        over = font_big.render("GAME OVER!", True, WHITE)
        final = font_med.render(f"Skor Akhir: {score}", True, WHITE)
        window.blit(over, (WIDTH//2 - over.get_width()//2, 200))
        window.blit(final, (WIDTH//2 - final.get_width()//2, 330))
        restart_btn = draw_button(WIDTH//2 - 150, 480, "RESTART")

    # WINNER
    elif STATE == "winner":
        draw_cartoon_background(window)
        win = font_big.render("YOU WIN!", True, GREEN)
        final = font_med.render(f"Skor Akhir: {score}", True, WHITE)
        window.blit(win, (WIDTH//2 - win.get_width()//2, 200))
        window.blit(final, (WIDTH//2 - final.get_width()//2, 330))
        restart_btn = draw_button(WIDTH//2 - 150, 480, "RESTART")

    pygame.display.update()
    clock.tick(60)

pygame.quit()
