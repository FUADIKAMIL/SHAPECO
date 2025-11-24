# src/app_full_ui_png.py
import os, io, math
import pygame
import cairo
import sys

# ---------------- Paths ----------------
IMG_DIR = "assets/images"
SOUNDS_DIR = "assets/sounds"
os.makedirs(IMG_DIR, exist_ok=True)
os.makedirs(SOUNDS_DIR, exist_ok=True)

BG_PATH = os.path.join(IMG_DIR, "background.png")
CHAR_PATH = os.path.join(IMG_DIR, "char.png")
PLAY_PNG = os.path.join(IMG_DIR, "play.png")
BACK_PNG = os.path.join(IMG_DIR, "back.png")
BOX_PNG = os.path.join(IMG_DIR, "box_template.png")
CARD_PNG = os.path.join(IMG_DIR, "card_template.png")
ICON_COLOR_PNG = os.path.join(IMG_DIR, "icon_color_template.png")
ICON_SHAPE_PNG = os.path.join(IMG_DIR, "icon_shape_template.png")

# fallback uploaded images available in environment
FALLBACK_BG = "/mnt/data/772bea74-9758-4f21-8423-36d1cff64b0e.jpg"
FALLBACK_CHAR = "/mnt/data/14578f74-d9f1-446a-90c2-9629d68fa418.jpg"

# ---------------- Window ----------------
WINDOW_W, WINDOW_H = 900, 600
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WINDOW_W, WINDOW_H))
pygame.display.set_caption("SHAPECO")
clock = pygame.time.Clock()

# Fonts
def try_font(name, size, bold=False):
    try:
        return pygame.font.SysFont(name, size, bold=bold)
    except Exception:
        return pygame.font.SysFont(None, size, bold=bold)

FONT_BIG = try_font("Comic Sans MS", 64, bold=True)
FONT = try_font("Comic Sans MS", 28, bold=True)
SMALL = try_font("Comic Sans MS", 16)

# ---------------- Cairo helpers ----------------
def cairo_surface_to_png_bytes(surf):
    buf = io.BytesIO()
    surf.write_to_png(buf)
    return buf.getvalue()

def cairo_to_pygame(surf):
    b = cairo_surface_to_png_bytes(surf)
    return pygame.image.load(io.BytesIO(b)).convert_alpha()

# ---------------- Default PNG creators (only if missing) ----------------
def create_play_png(path, size=180):
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, size, size)
    ctx = cairo.Context(surf)
    ctx.set_source_rgb(0.27,0.65,0.95)
    ctx.arc(size/2, size/2, size*0.44, 0, 2*math.pi)
    ctx.fill()
    ctx.set_source_rgb(1,1,1)
    ctx.move_to(size*0.44, size*0.32)
    ctx.line_to(size*0.72, size*0.50)
    ctx.line_to(size*0.44, size*0.68)
    ctx.close_path()
    ctx.fill()
    surf.write_to_png(path)

def create_back_png(path, size=96):
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, size, size)
    ctx = cairo.Context(surf)
    ctx.set_source_rgb(0.95,0.4,0.45)
    ctx.arc(size/2, size/2, size*0.42, 0, 2*math.pi)
    ctx.fill()
    ctx.set_source_rgb(1,1,1)
    s = size*0.28
    x = size/2; y = size/2
    ctx.move_to(x + s*0.45, y - s)
    ctx.line_to(x - s*0.15, y)
    ctx.line_to(x + s*0.45, y + s)
    ctx.set_line_width(size*0.08)
    ctx.set_line_cap(cairo.LineCap.ROUND)
    ctx.stroke()
    surf.write_to_png(path)

def create_box_png(path, w=640, h=160):
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, w, h)
    ctx = cairo.Context(surf)
    r = 20
    ctx.new_sub_path()
    ctx.arc(w-r, r, r, -math.pi/2, 0)
    ctx.arc(w-r, h-r, r, 0, math.pi/2)
    ctx.arc(r, h-r, r, math.pi/2, math.pi)
    ctx.arc(r, r, r, math.pi, 3*math.pi/2)
    ctx.close_path()
    ctx.set_source_rgb(1,1,1)
    ctx.fill_preserve()
    ctx.set_line_width(4)
    ctx.set_source_rgba(0,0,0,0.12)
    ctx.stroke()
    surf.write_to_png(path)

def create_card_template_png(path, w=360, h=200):
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, w, h)
    ctx = cairo.Context(surf)
    r = 18
    ctx.new_sub_path()
    ctx.arc(w-r, r, r, -math.pi/2, 0)
    ctx.arc(w-r, h-r, r, 0, math.pi/2)
    ctx.arc(r, h-r, r, math.pi/2, math.pi)
    ctx.arc(r, r, r, math.pi, 3*math.pi/2)
    ctx.close_path()
    ctx.set_source_rgb(0.98,0.98,1)
    ctx.fill_preserve()
    ctx.set_line_width(3)
    ctx.set_source_rgba(0,0,0,0.08)
    ctx.stroke()
    surf.write_to_png(path)

def create_icon_templates(color_path, shape_path, size=72):
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, size, size)
    ctx = cairo.Context(surf)
    cx = cy = size/2; r = size*0.34
    ctx.arc(cx, cy, r, 0, 2*math.pi)
    ctx.set_source_rgb(0.8,0.8,0.8)
    ctx.fill_preserve()
    ctx.set_line_width(2)
    ctx.set_source_rgba(0,0,0,0.12)
    ctx.stroke()
    surf.write_to_png(color_path)

    surf2 = cairo.ImageSurface(cairo.FORMAT_ARGB32, size, size)
    ctx2 = cairo.Context(surf2)
    s = size*0.32
    ctx2.rectangle((size/2 - s), (size/2 - s), s*2, s*2)
    ctx2.set_source_rgb(0.8,0.8,0.8)
    ctx2.fill_preserve()
    ctx2.set_line_width(2)
    ctx2.set_source_rgba(0,0,0,0.12)
    ctx2.stroke()
    surf2.write_to_png(shape_path)

# Auto create PNG defaults if missing
if not os.path.exists(PLAY_PNG): create_play_png(PLAY_PNG)
if not os.path.exists(BACK_PNG): create_back_png(BACK_PNG)
if not os.path.exists(BOX_PNG): create_box_png(BOX_PNG)
if not os.path.exists(CARD_PNG): create_card_template_png(CARD_PNG)
if not os.path.exists(ICON_COLOR_PNG) or not os.path.exists(ICON_SHAPE_PNG):
    create_icon_templates(ICON_COLOR_PNG, ICON_SHAPE_PNG)

# ---------------- Load PNG assets ----------------
def load_img(path, fallback=None, size=None):
    if os.path.exists(path):
        im = pygame.image.load(path).convert_alpha()
        if size: im = pygame.transform.smoothscale(im, size)
        return im
    if fallback and os.path.exists(fallback):
        im = pygame.image.load(fallback).convert_alpha()
        if size: im = pygame.transform.smoothscale(im, size)
        return im
    return None

BACKGROUND = load_img(BG_PATH, fallback=FALLBACK_BG, size=(WINDOW_W, WINDOW_H))
CHARACTER = load_img(CHAR_PATH, fallback=FALLBACK_CHAR, size=(260,260))
BTN_PLAY = load_img(PLAY_PNG, size=(140,140))
BTN_BACK = load_img(BACK_PNG, size=(64,64))
BOX_PNG_SURF = load_img(BOX_PNG, size=(640,160))
CARD_TEMPLATE = load_img(CARD_PNG, size=(360,200))

# ---------------- Data ----------------
COLORS = [("Merah",(220,20,60)),("Hijau",(34,139,34)),("Biru",(30,144,255)),("Kuning",(255,215,0))]
SHAPES = [("Persegi","square"),("Lingkaran","circle"),("Segitiga","triangle")]

# Load sounds
def load_sound(name):
    base = os.path.join(SOUNDS_DIR, name)
    for ext in ("wav","ogg","mp3"):
        p = f"{base}.{ext}"
        if os.path.exists(p):
            try: return pygame.mixer.Sound(p)
            except: pass
    return None

sound_colors = {n: load_sound(n.lower()) for n,_ in COLORS}
sound_shapes = {n: load_sound(n.lower()) for n,_ in SHAPES}

# ---------------- SOUND FIX: add missing play_sound() ----------------
def play_sound(s):
    if s:
        try: s.play()
        except: pass

# ---------------- Cairo icon renderers ----------------
def render_color_icon_cairo(rgb, size=64):
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, size, size)
    ctx = cairo.Context(surf)
    cx = cy = size/2; r = size*0.34
    ctx.arc(cx,cy,r,0,2*math.pi)
    ctx.set_source_rgb(*(c/255 for c in rgb))
    ctx.fill_preserve()
    ctx.set_line_width(3)
    ctx.set_source_rgba(0,0,0,0.12)
    ctx.stroke()
    return cairo_to_pygame(surf)

def render_shape_icon_cairo(kind, size=64):
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, size, size)
    ctx = cairo.Context(surf)
    cx = cy = size/2; s = size*0.28
    ctx.set_source_rgb(0.25,0.55,0.95)
    if kind == "circle":
        ctx.arc(cx,cy,s,0,2*math.pi); ctx.fill()
    elif kind == "square":
        ctx.rectangle(cx-s, cy-s, s*2, s*2); ctx.fill()
    else:
        ctx.move_to(cx, cy-s); ctx.line_to(cx-s, cy+s); ctx.line_to(cx+s, cy+s); ctx.close_path(); ctx.fill()
    return cairo_to_pygame(surf)

# ---------------- Build final card surfaces ----------------
def make_color_card(name, rgb):
    card = CARD_TEMPLATE.copy()
    icon = render_color_icon_cairo(rgb, size=96)
    card.blit(icon, (16, (card.get_height()-96)//2))
    text = try_font("Comic Sans MS", 22, bold=True).render(name, True, (255,255,255))
    card.blit(text, (card.get_width()-text.get_width()-20, card.get_height()-text.get_height()-18))
    return card

def make_shape_card(name, kind):
    card = CARD_TEMPLATE.copy()
    icon = render_shape_icon_cairo(kind, size=96)
    card.blit(icon, (16, (card.get_height()-96)//2))
    text = try_font("Comic Sans MS", 22, bold=True).render(name, True, (40,40,40))
    card.blit(text, (card.get_width()-text.get_width()-20, card.get_height()-text.get_height()-18))
    return card

# ---------------- Create cards ----------------
color_cards = [(n, make_color_card(n, rgb), rgb) for n,rgb in COLORS]
shape_cards = [(n, make_shape_card(n, kind), kind) for n,kind in SHAPES]

# ---------------- Layout ----------------
def layout_cards_grid(count, top, cols=2, card_w=360, card_h=200, gap_x=24, gap_y=18):
    positions = []
    total_w = cols*card_w + (cols-1)*gap_x
    x0 = (WINDOW_W - total_w) // 2
    for i in range(count):
        c = i % cols; r = i // cols
        x = x0 + c*(card_w + gap_x)
        y = top + r*(card_h + gap_y)
        positions.append(pygame.Rect(x,y,card_w,card_h))
    return positions

color_pos = layout_cards_grid(len(color_cards), top=160)
shape_pos = layout_cards_grid(len(shape_cards), top=160)

# ---------------- UI Rects ----------------
scene = "splash"
PLAY_RECT = BTN_PLAY.get_rect(center=(WINDOW_W//2, WINDOW_H//2 + 60))
BOX1_RECT = BOX_PNG_SURF.get_rect(center=(WINDOW_W//2, 220))
BOX2_RECT = BOX_PNG_SURF.get_rect(center=(WINDOW_W//2, 400))
BACK_RECT = BTN_BACK.get_rect(topleft=(12,12))

# Hover scale
hover_play = hover_box1 = hover_box2 = hover_back = False
scale_play = scale_back = scale_box1 = scale_box2 = 1.0

# ---------------- Main loop ----------------
running = True
while running:
    dt = clock.tick(60) / 1000.0
    mx, my = pygame.mouse.get_pos()

    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            running = False

        elif ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:

            if scene == "splash":
                if PLAY_RECT.collidepoint(mx,my):
                    scene = "mainmenu"

            elif scene == "mainmenu":
                if BOX1_RECT.collidepoint(mx,my):
                    scene = "color"
                elif BOX2_RECT.collidepoint(mx,my):
                    scene = "shape"

            else:
                if BACK_RECT.collidepoint(mx,my):
                    scene = "mainmenu"

                if scene == "color":
                    for (name,img,rgb),rect in zip(color_cards, color_pos):
                        if rect.collidepoint(mx,my):
                            play_sound(sound_colors.get(name))

                if scene == "shape":
                    for (name,img,k),rect in zip(shape_cards, shape_pos):
                        if rect.collidepoint(mx,my):
                            play_sound(sound_shapes.get(name))

    # hover & scale animation
    hover_play = PLAY_RECT.collidepoint(mx,my) and scene=="splash"
    hover_box1 = BOX1_RECT.collidepoint(mx,my) and scene=="mainmenu"
    hover_box2 = BOX2_RECT.collidepoint(mx,my) and scene=="mainmenu"
    hover_back = BACK_RECT.collidepoint(mx,my) and scene not in ("splash","mainmenu")

    def lerp(a,b,t): return a + (b-a)*max(0, min(1,t))

    scale_play = lerp(scale_play, 1.06 if hover_play else 1.0, dt*8)
    scale_box1 = lerp(scale_box1, 1.03 if hover_box1 else 1.0, dt*8)
    scale_box2 = lerp(scale_box2, 1.03 if hover_box2 else 1.0, dt*8)
    scale_back = lerp(scale_back, 1.06 if hover_back else 1.0, dt*8)

    # draw bg
    if BACKGROUND:
        screen.blit(BACKGROUND, (0,0))
    else:
        screen.fill((245,245,255))

    # character
    if CHARACTER:
        cw,ch = CHARACTER.get_size()
        screen.blit(CHARACTER, (12, WINDOW_H - ch - 12))

    # scenes
    if scene == "splash":
        title = FONT_BIG.render("SHAPECO", True, (255,255,255))
        screen.blit(title, ((WINDOW_W-title.get_width())//2, 80))
        surf = pygame.transform.rotozoom(BTN_PLAY, 0, scale_play)
        screen.blit(surf, surf.get_rect(center=PLAY_RECT.center))

    elif scene == "mainmenu":
        header = FONT.render("Pilih Menu", True, (255,255,255))
        screen.blit(header, ((WINDOW_W-header.get_width())//2, 36))

        surf1 = pygame.transform.rotozoom(BOX_PNG_SURF, 0, scale_box1)
        screen.blit(surf1, surf1.get_rect(center=BOX1_RECT.center))

        surf2 = pygame.transform.rotozoom(BOX_PNG_SURF, 0, scale_box2)
        screen.blit(surf2, surf2.get_rect(center=BOX2_RECT.center))

    elif scene == "color":
        # BACK
        surf = pygame.transform.rotozoom(BTN_BACK, 0, scale_back)
        screen.blit(surf, BACK_RECT)
        screen.blit(FONT.render("Menu Warna", True, (40,40,40)), (82,18))

        for (name,img,rgb),rect in zip(color_cards, color_pos):
            screen.blit(img, rect)
            if rect.collidepoint(mx,my):
                pygame.draw.rect(screen, (255,255,255), rect.inflate(8,8), 3, border_radius=18)

    elif scene == "shape":
        surf = pygame.transform.rotozoom(BTN_BACK, 0, scale_back)
        screen.blit(surf, BACK_RECT)
        screen.blit(FONT.render("Menu Bentuk", True, (40,40,40)), (82,18))

        for (name,img,k),rect in zip(shape_cards, shape_pos):
            screen.blit(img, rect)
            if rect.collidepoint(mx,my):
                pygame.draw.rect(screen, (255,255,255), rect.inflate(8,8), 3, border_radius=18)

    # footer
    foot = SMALL.render("EduApp • SHAPECO • Pygame + Pycairo", True, (100,100,120))
    screen.blit(foot, (WINDOW_W-foot.get_width()-12, WINDOW_H-22))

    pygame.display.flip()

pygame.quit()
sys.exit()