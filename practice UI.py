import pygame
import pygame_gui

pygame.init()

WINDOW_SIZE = (800, 600)
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("PyGame GUI Menu")

clock = pygame.time.Clock()

# UI Manager
ui_manager = pygame_gui.UIManager(WINDOW_SIZE)

# start button
start_button = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect(300, 200, 200, 50),
    text="Start",
    manager=ui_manager
)

# exit button
exit_button = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect(300, 300, 200, 50),
    text="Exit",
    manager=ui_manager
)

# START text after click
game_started_text = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect(275, 400, 250, 50),
    text="",
    manager=ui_manager
)

running = True
while running:
    time_delta = clock.tick(60) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # UI button events
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == start_button:
                game_started_text.set_text("The game has started")

            elif event.ui_element == exit_button:
                running = False

        ui_manager.process_events(event)

    ui_manager.update(time_delta)

    screen.fill((30, 30, 30))
    ui_manager.draw_ui(screen)

    pygame.display.update()

pygame.quit()
