import pygame
import sys
import time

pygame.init()

# Ekran i font
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("Nothing Game")
font = pygame.font.SysFont("Arial", 30)

# Stanja igre
NOT_STARTED = 0
IN_PROGRESS = 1
GAME_OVER = 2

current_state = NOT_STARTED
inactivity_time = 0
startup_period = 1
state_change_time = time.time()

nothing_label = "nothing"
something_label = "something"

clock = pygame.time.Clock()


def time_text_formatted(seconds):
    num = int(seconds)
    days = num // 86400
    num %= 86400
    hours = num // 3600
    num %= 3600
    minutes = num // 60
    num %= 60

    parts = []
    if days > 0:
        parts.append(f"{days} day{'s' if days != 1 else ''}")
    if hours > 0:
        parts.append(f"{hours} hour{'s' if hours != 1 else ''}")
    if minutes > 0:
        parts.append(f"{minutes} minute{'s' if minutes != 1 else ''}")
    parts.append(f"{num} second{'s' if num != 1 else ''}")

    return ", ".join(parts)


def did_start_game(events):
    for event in events:
        if event.type in [pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN]:
            return True
    return False


def did_something(events):
    for event in events:
        if event.type in [pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN, pygame.MOUSEMOTION]:
            return True
    return False


def draw_text(text):
    screen.fill((0, 0, 0))
    lines = text.split('\n')
    y = screen.get_height() // 2 - (len(lines) * 20)

    for line in lines:
        rendered = font.render(line, True, (255, 255, 255))
        text_rect = rendered.get_rect(center=(screen.get_width() // 2, y))
        screen.blit(rendered, text_rect)
        y += 40
    pygame.display.flip()


def reset_game():
    global current_state, inactivity_time, state_change_time
    current_state = NOT_STARTED
    inactivity_time = 0
    state_change_time = time.time()
    draw_text(f"Press any key or mouse button to start doing {nothing_label}\n")


reset_game()

while True:
    dt = clock.tick(60) / 1000.0
    events = pygame.event.get()

    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        pygame.quit()
        sys.exit()

    now = time.time()

    if current_state == NOT_STARTED:
        if did_start_game(events):
            current_state = IN_PROGRESS
            state_change_time = now
        elif now - state_change_time >= startup_period:
            draw_text(f"Press any key or mouse button to start doing {nothing_label}\n")

    elif current_state == IN_PROGRESS:
        inactivity_time += dt
        draw_text(f"You have been doing {nothing_label} for\n{time_text_formatted(inactivity_time)}\n")
        if now - state_change_time >= 1.0 and did_something(events):
            current_state = GAME_OVER
            state_change_time = now

    elif current_state == GAME_OVER:
        draw_text(f"You did {something_label}, you lost\nYou did {nothing_label} for {time_text_formatted(inactivity_time)}")
        if now - state_change_time >= 1.0 and did_start_game(events):
            reset_game()
