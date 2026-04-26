import os
import pygame
from PIL import Image

# -------------------------
# DISPLAY ENVIRONMENT
# -------------------------
os.environ["DISPLAY"] = ":0"

# -------------------------
# SETTINGS
# -------------------------
WIDTH    = 800
HEIGHT   = 480
FPS      = 8
ANIM_DIR = "/home/tina386/PiPet-Cyberdeck-Ecosystem/house/animations"

# -------------------------
# GIF LOADER
# -------------------------
def load_gif(filename):
    frames = []
    gif = Image.open(os.path.join(ANIM_DIR, filename))
    for frame in range(gif.n_frames):
        gif.seek(frame)
        frame_img = gif.convert("RGB")
        frame_img = frame_img.resize((WIDTH, HEIGHT), Image.NEAREST)
        frames.append(frame_img)
    return frames

def pil_to_pygame(pil_image):
    return pygame.image.fromstring(
        pil_image.tobytes(), pil_image.size, "RGB"
    )

# -------------------------
# INIT PYGAME
# -------------------------
pygame.init()
font_name_large = pygame.font.SysFont("monospace", 20, bold=True)
font_name_small = pygame.font.SysFont("monospace", 13, bold=True)
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("PiPet House")
clock = pygame.time.Clock()

# -------------------------
# LOAD ANIMATIONS
# -------------------------
print("Loading animations...")
animations = {
    "idle":      load_gif("Cat_idle_house.gif"),
    "listening": load_gif("Cat_listen_house.gif"),
    "thinking":  load_gif("Cat_think_house.gif"),
    "speaking":  load_gif("Cat_speak_house.gif"),
    "error":     load_gif("Cat_error_house.gif"),
}
print("Animations loaded!")

# -------------------------
# LOAD STAT WIDGET IMAGES
# -------------------------
widget_collapsed = pygame.image.load(
    os.path.join(ANIM_DIR, "Status-bar-collapsed.png")
).convert_alpha()
widget_expanded = pygame.image.load(
    os.path.join(ANIM_DIR, "Status-bar-expanded.png")
).convert_alpha()

# Scale 2x
widget_collapsed = pygame.transform.scale(widget_collapsed, (240, 160))
widget_expanded  = pygame.transform.scale(widget_expanded,  (240, 160))


# -------------------------
# LOAD CLOSE BUTTON
# -------------------------
close_btn_img = pygame.image.load(
    os.path.join(ANIM_DIR, "Exit Icon.png")
).convert_alpha()
close_btn_img = pygame.transform.scale(close_btn_img, (50, 50))
close_btn_rect = close_btn_img.get_rect()
close_btn_rect.topright = (WIDTH - 15, 15)  # Top-right corner
close_btn_hovered = False

# -------------------------
# BAR POSITIONS (2x scaled)
# -------------------------
BAR_X      = 82
BAR_WIDTH  = 136
BAR_HEIGHT = 14

BARS_COLLAPSED = [
    {"y": 24, "stat": None},
    {"y": 40, "stat": None},
]

BARS_EXPANDED = [
    {"y": 24, "stat": "hunger"},
    {"y": 40, "stat": "happiness"},
    {"y": 56, "stat": "health"},
    {"y": 72, "stat": "energy"},
    {"y": 88, "stat": "cleanliness"},
]

# Arrow touch areas
ARROW_COLLAPSED = pygame.Rect(182, 56,  56, 26)
ARROW_EXPANDED  = pygame.Rect(194, 108, 26, 18)

# -------------------------
# MOCK STATS
# Replace with pet.py later
# -------------------------
stats = {
    "hunger":      80,
    "happiness":   30,
    "health":      60,
    "energy":      20,
    "cleanliness": 90,
}

# -------------------------
# HELPERS
# -------------------------
def get_bar_color(value):
    if value >= 70:
        return (100, 200, 120)   # green
    elif value >= 40:
        return (255, 200, 50)    # yellow
    else:
        return (220, 80, 80)     # red

def get_lowest_stats(stats):
    sorted_stats = sorted(stats.items(), key=lambda x: x[1])
    return [sorted_stats[0][0], sorted_stats[1][0]]

# Add font after pygame.init()
pip_font = pygame.font.SysFont("monospace", 14, bold=True)

def draw_stat_widget(screen, stats, widget_open):
    img = widget_expanded if widget_open else widget_collapsed
    screen.blit(img, (0, 0))

    if widget_open:
        bars = BARS_EXPANDED

        # Name in cat head, centered, left of 5th bar
        name_surface = font_name_small.render("Pip", True, (80, 50, 50))
        name_x = (78 - name_surface.get_width()) // 2 + 10
        screen.blit(name_surface, (name_x, 85))

    else:
        lowest = get_lowest_stats(stats)
        bars = [
            {"y": BARS_COLLAPSED[0]["y"], "stat": lowest[0]},
            {"y": BARS_COLLAPSED[1]["y"], "stat": lowest[1]},
        ]

        # Name bigger, centered in pink space left of dropdown
        name_surface = font_name_large.render("Pip", True, (80, 50, 50))
        name_x = (160 - name_surface.get_width()) // 2 + 18
        screen.blit(name_surface, (name_x + 40,59))

    for bar in bars:
        stat_name = bar["stat"]
        if stat_name is None:
            continue
        value      = stats[stat_name]
        fill_width = int((value / 100) * BAR_WIDTH)
        color      = get_bar_color(value)
        pygame.draw.rect(
            screen, color,
            (BAR_X, bar["y"], fill_width, BAR_HEIGHT)
        )
def handle_tap(pos, widget_open):
    arrow = ARROW_EXPANDED if widget_open else ARROW_COLLAPSED
    if arrow.collidepoint(pos):
        print(f"Arrow tapped! {'Collapsing' if widget_open else 'Expanding'}")
        return not widget_open
    return widget_open

# -------------------------
# STATE
# -------------------------
current_state = "idle"
frame_index   = 0
widget_open   = False

# -------------------------
# MAIN LOOP
# -------------------------
print("Starting display loop...")
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Keyboard shortcuts
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_1:
                current_state = "idle"
                frame_index = 0
            elif event.key == pygame.K_2:
                current_state = "listening"
                frame_index = 0
            elif event.key == pygame.K_3:
                current_state = "thinking"
                frame_index = 0
            elif event.key == pygame.K_4:
                current_state = "speaking"
                frame_index = 0
            elif event.key == pygame.K_5:
                current_state = "error"
                frame_index = 0

         # Mouse click
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Check if close button was clicked
            if close_btn_rect.collidepoint(event.pos):
                running = False
            else:
                widget_open = handle_tap(event.pos, widget_open)

        # Check for hover
        if event.type == pygame.MOUSEMOTION:
            close_btn_hovered = close_btn_rect.collidepoint(event.pos)

        # Finger touch (Pi touchscreen)
        if event.type == pygame.FINGERDOWN:
            tap_x = int(event.x * WIDTH)
            tap_y = int(event.y * HEIGHT)
            widget_open = handle_tap((tap_x, tap_y), widget_open)

    # Draw animation
    frames  = animations[current_state]
    surface = pil_to_pygame(frames[frame_index])
    screen.blit(surface, (0, 0))

    # Draw stat widget on top
    draw_stat_widget(screen, stats, widget_open)

     # Draw close button (add this)
    if close_btn_hovered:
        scaled = pygame.transform.scale(close_btn_img, (55, 55))
        rect = scaled.get_rect(center=close_btn_rect.center)
        screen.blit(scaled, rect)
    else:
        screen.blit(close_btn_img, close_btn_rect)

    pygame.display.flip()
    frame_index = (frame_index + 1) % len(frames)
    clock.tick(FPS)

pygame.quit()
