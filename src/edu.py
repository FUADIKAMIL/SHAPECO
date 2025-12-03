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
BG_Menu = os.path.join(IMG_DIR, "backgroundmenu.png")
BG_WarnaBentuk = os.path.join(IMG_DIR, "bgwarnabentuk.png")
CHAR_PATH = os.path.join(IMG_DIR, "char.png")
PLAY_PNG = os.path.join(IMG_DIR, "play.png")
BACK_PNG = os.path.join(IMG_DIR, "back.png")
MENU_COLOR_PNG = os.path.join(IMG_DIR, "4.png")
MENU_SHAPE_PNG = os.path.join(IMG_DIR, "3.png")
ICON_COLOR_PNG = os.path.join(IMG_DIR, "icon_color_template.png")
ICON_SHAPE_PNG = os.path.join(IMG_DIR, "icon_shape_template.png")

# fallback uploaded images available in environment
FALLBACK_BG = "/mnt/data/772bea74-9758-4f21-8423-36d1cff64b0e.jpg"
FALLBACK_CHAR = "/mnt/data/14578f74-d9f1-446a-90c2-9629d68fa418.jpg"

# ---------------- Window ----------------
WINDOW_W, WINDOW_H = 1280, 720
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

# ---------------- Default PNG creators ----------------
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

if not os.path.exists(PLAY_PNG): create_play_png(PLAY_PNG)
if not os.path.exists(BACK_PNG): create_back_png(BACK_PNG)
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
BACKGROUNDMENU = load_img(BG_Menu, fallback=FALLBACK_BG, size=(WINDOW_W, WINDOW_H))
BACKGROUNDWARNA_BENTUK = load_img(BG_WarnaBentuk, fallback=FALLBACK_BG, size=(WINDOW_W, WINDOW_H))
CHARACTER = load_img(CHAR_PATH, fallback=FALLBACK_CHAR, size=(260,260))
BTN_PLAY = load_img(PLAY_PNG, size=(140,140))
BTN_BACK = load_img(BACK_PNG, size=(64,64))
MENU_COLOR_SURF = load_img(MENU_COLOR_PNG, size=(450, 450))
MENU_SHAPE_SURF = load_img(MENU_SHAPE_PNG, size=(440, 380))

# ---------------- Data ----------------
COLORS = [
    ("Merah",(220,20,60)),
    ("Oranye",(255,140,0)),
    ("Kuning",(255,215,0)),
    ("Hijau",(34,139,34)),
    ("Tosca",(64,224,208)),
    ("Biru",(30,144,255)),
    ("Nila",(75,0,130)),
    ("Ungu",(138,43,226)),
    ("Pink",(255,105,180)),
    ("Cokelat",(160,82,45)),
    ("Abuabu",(169,169,169)),
    ("Hitam",(20,20,20)),
]

# 9 BENTUK
SHAPES = [
    ("Lingkaran", "circle"),
    ("Kotak", "square"),
    ("Segitiga", "triangle"),
    ("Oval", "oval"),
    ("Ketupat", "diamond"),
    ("Segilima", "pentagon"),
    ("Segienam", "hexagon"),
    ("Bintang", "star"),
    ("Tambah", "plus")
]

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

def play_sound(s):
    if s:
        try: s.play()
        except: pass

# ---------------- Layout Functions (GRID MODE) ----------------

# Fungsi Layout Grid yang Rapi dan Terpusat
def layout_grid_centered(count, cols, item_size, gap_x, gap_y, start_y):
    positions = []
    
    # Hitung lebar total grid agar bisa ditengahin
    total_grid_w = cols * item_size + (cols - 1) * gap_x
    start_x = (WINDOW_W - total_grid_w) // 2
    
    for i in range(count):
        row = i // cols
        col = i % cols
        
        x = start_x + col * (item_size + gap_x)
        y = start_y + row * (item_size + gap_y)
        
        positions.append(pygame.Rect(x, y, item_size, item_size))
        
    return positions

# --- GENERATE POSITIONS ---

# 1. WARNA: 12 Item. Format 4 Kolom x 3 Baris.
# Ukuran item 150px, Jarak 40px.
color_pos = layout_grid_centered(
    count=len(COLORS), 
    cols=4, 
    item_size=150, 
    gap_x=40, 
    gap_y=30, 
    start_y=130
)

# 2. BENTUK: 9 Item. Format 3 Kolom x 3 Baris.
# Ukuran item 160px (sedikit lebih besar karena jumlahnya sedikit), Jarak 50px.
shape_pos = layout_grid_centered(
    count=len(SHAPES), 
    cols=3, 
    item_size=160, 
    gap_x=60, 
    gap_y=30, 
    start_y=130
)


# ---------------- UI Rects ----------------
scene = "splash"
PLAY_RECT = BTN_PLAY.get_rect(center=(WINDOW_W//2, WINDOW_H//2 + 126))
BOX1_RECT = MENU_COLOR_SURF.get_rect(center=(WINDOW_W//2 - 340, 400))
BOX2_RECT = MENU_SHAPE_SURF.get_rect(center=(WINDOW_W//2 + 340, 435))
BACK_RECT = BTN_BACK.get_rect(topleft=(12,12))

# Hover scale
hover_play = hover_box1 = hover_box2 = hover_back = 1.0
scale_play = scale_back = scale_box1 = scale_box2 = 1.0

# ---------------- Helper Geometry Functions ----------------
def get_polygon_points(cx, cy, radius, sides, angle_offset=0):
    points = []
    for i in range(sides):
        angle = angle_offset + (2 * math.pi * i / sides)
        x = cx + radius * math.cos(angle)
        y = cy + radius * math.sin(angle)
        points.append((x, y))
    return points

def get_star_points(cx, cy, outer_radius, inner_radius, points=5):
    coords = []
    angle_step = math.pi / points
    current_angle = -math.pi / 2 # start pointing up
    for i in range(points * 2):
        r = outer_radius if i % 2 == 0 else inner_radius
        x = cx + r * math.cos(current_angle)
        y = cy + r * math.sin(current_angle)
        coords.append((x, y))
        current_angle += angle_step
    return coords

# ---------------- Helper draw functions ----------------
def draw_color_circle_at_rect(surface, rect, rgb, hover=False):
    cx, cy = rect.center
    radius = rect.width // 2 
    
    # Bayangan tipis biar rapi
    pygame.draw.circle(surface, (0,0,0,50), (cx+3, cy+3), radius)
    
    # Lingkaran Utama
    pygame.draw.circle(surface, rgb, (cx, cy), radius)
    
    # Outline putih halus
    pygame.draw.circle(surface, (255,255,255), (cx, cy), radius, 2)

    if hover:
        pygame.draw.circle(surface, (255,255,255), (cx,cy), radius+6, 4)

def draw_shape_in_rect(surface, rect, kind, hover=False):
    cx, cy = rect.center
    # Radius dasar (lingkaran putih)
    radius = rect.width // 2
    
    # Bayangan
    pygame.draw.circle(surface, (0,0,0,50), (cx+3, cy+3), radius)

    # Background lingkaran putih
    pygame.draw.circle(surface, (255,255,255), (cx, cy), radius)
    
    # Radius untuk menggambar bentuk di dalamnya
    draw_radius = radius - 25
    
    if kind == "circle":
        pygame.draw.circle(surface, (40,120,255), (cx,cy), draw_radius)

    elif kind == "square":
        s = draw_radius
        pygame.draw.rect(surface, (255,140,0), (cx-s, cy-s, s*2, s*2))

    elif kind == "triangle":
        pts = get_polygon_points(cx, cy, draw_radius, 3, angle_offset=-math.pi/2)
        pygame.draw.polygon(surface, (220,60,150), pts)
        
    elif kind == "oval":
        w = draw_radius * 1.8
        h = draw_radius * 1.2
        oval_rect = pygame.Rect(cx - w/2, cy - h/2, w, h)
        pygame.draw.ellipse(surface, (0,180,100), oval_rect)

    elif kind == "diamond":
        pts = [(cx, cy - draw_radius), (cx + draw_radius, cy), 
               (cx, cy + draw_radius), (cx - draw_radius, cy)]
        pygame.draw.polygon(surface, (128,0,128), pts)
        
    elif kind == "pentagon":
        pts = get_polygon_points(cx, cy, draw_radius, 5, angle_offset=-math.pi/2)
        pygame.draw.polygon(surface, (255,69,0), pts)
        
    elif kind == "hexagon":
        pts = get_polygon_points(cx, cy, draw_radius, 6, angle_offset=0)
        pygame.draw.polygon(surface, (70,130,180), pts)

    elif kind == "star":
        pts = get_star_points(cx, cy, draw_radius, draw_radius*0.4, 5)
        pygame.draw.polygon(surface, (255,215,0), pts)

    elif kind == "plus":
        th = draw_radius * 0.4; l = draw_radius * 1.6
        pygame.draw.rect(surface, (50,50,50), (cx - l/2, cy - th/2, l, th))
        pygame.draw.rect(surface, (50,50,50), (cx - th/2, cy - l/2, th, l))
    
    # Hover outline
    if hover:
        pygame.draw.circle(surface, (255,255,255), (cx,cy), radius+8, 4)

# ---------------- Main loop ----------------
running = True
while running:
    dt = clock.tick(60) / 1000.0
    mx, my = pygame.mouse.get_pos()
    mouse_down = False

    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            running = False

        elif ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
            mouse_down = True

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
                    for (name,rgb),rect in zip(COLORS, color_pos):
                        if rect.collidepoint(mx,my):
                            play_sound(sound_colors.get(name))

                if scene == "shape":
                    for (name,kind),rect in zip(SHAPES, shape_pos):
                        if rect.collidepoint(mx,my):
                            play_sound(sound_shapes.get(name))

    # hover state
    hover_play = PLAY_RECT.collidepoint(mx,my) and scene=="splash"
    hover_box1 = BOX1_RECT.collidepoint(mx,my) and scene=="mainmenu"
    hover_box2 = BOX2_RECT.collidepoint(mx,my) and scene=="mainmenu"
    hover_back = BACK_RECT.collidepoint(mx,my) and scene not in ("splash","mainmenu")

    def lerp(a,b,t): return a + (b-a)*max(0, min(1,t))

    scale_play = lerp(scale_play, 1.06 if hover_play else 1.0, dt*8)
    scale_box1 = lerp(scale_box1, 1.06 if hover_box1 else 1.0, dt*8)
    scale_box2 = lerp(scale_box2, 1.06 if hover_box2 else 1.0, dt*8)
    scale_back = lerp(scale_back, 1.06 if hover_back else 1.0, dt*8)

    # draw bg sesuai scene
    if scene == "splash":
        if BACKGROUND: screen.blit(BACKGROUND, (0,0))
        else: screen.fill((30,30,40))

    elif scene == "mainmenu":
        if BACKGROUNDMENU: screen.blit(BACKGROUNDMENU, (0,0))
        else: screen.fill((40,40,50))

    else:
        if BACKGROUNDWARNA_BENTUK: screen.blit(BACKGROUNDWARNA_BENTUK, (0,0))
        else: screen.fill((45,45,60))


    # character
    if CHARACTER:
        cw,ch = CHARACTER.get_size()
        screen.blit(CHARACTER, (12, WINDOW_H - ch - 12))

    # scenes
    if scene == "splash":
        surf = pygame.transform.rotozoom(BTN_PLAY, 0, scale_play) if BTN_PLAY else None
        if surf:
            screen.blit(surf, surf.get_rect(center=PLAY_RECT.center))
        else:
            txt = FONT_BIG.render("PLAY", True, (255,255,255))
            screen.blit(txt, txt.get_rect(center=PLAY_RECT.center))

    elif scene == "mainmenu":
        surf1 = pygame.transform.rotozoom(MENU_COLOR_SURF, 0, scale_box1) if MENU_COLOR_SURF else None
        if surf1: screen.blit(surf1, surf1.get_rect(center=BOX1_RECT.center))
        surf2 = pygame.transform.rotozoom(MENU_SHAPE_SURF, 0, scale_box2) if MENU_SHAPE_SURF else None
        if surf2: screen.blit(surf2, surf2.get_rect(center=BOX2_RECT.center))

    elif scene == "color":
        surf = pygame.transform.rotozoom(BTN_BACK, 0, scale_back) if BTN_BACK else None
        if surf: screen.blit(surf, BACK_RECT)
        screen.blit(FONT.render("Menu Warna", True, (40,40,40)), (82,18))

        # draw colors
        for (name,rgb),rect in zip(COLORS, color_pos):
            hover = rect.collidepoint(mx,my)
            draw_color_circle_at_rect(screen, rect, rgb, hover=hover)

    elif scene == "shape":
        surf = pygame.transform.rotozoom(BTN_BACK, 0, scale_back) if BTN_BACK else None
        if surf: screen.blit(surf, BACK_RECT)
        screen.blit(FONT.render("Menu Bentuk", True, (40,40,40)), (82,18))

        # draw shapes
        for (name,kind),rect in zip(SHAPES, shape_pos):
            hover = rect.collidepoint(mx,my)
            draw_shape_in_rect(screen, rect, kind, hover=hover)

    # footer
    foot = SMALL.render("EduApp • SHAPECO", True, (100,100,120))
    screen.blit(foot, (WINDOW_W-foot.get_width()-12, WINDOW_H-22))

    pygame.display.flip()

pygame.quit()
sys.exit()