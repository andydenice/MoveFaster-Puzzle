import pygame
import random
import sys

def main(rows, cols, duration):
    pygame.init()

    # Constants
    SCREEN_WIDTH, SCREEN_HEIGHT = 600, 600
    IMAGE_SIZE = SCREEN_WIDTH // cols
    FPS = 60

    # Colors
    WHITE = (255, 255, 255)

    # Set up the display
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("MoveFaster Puzzle")

    # Load and scale the image
    image_path = "img.png"  # Default image name
    image = pygame.image.load(image_path)
    image = pygame.transform.scale(image, (SCREEN_WIDTH, SCREEN_HEIGHT))

    # Slice the image into pieces
    pieces = [[image.subsurface((j * IMAGE_SIZE, i * IMAGE_SIZE, IMAGE_SIZE, IMAGE_SIZE))
               for j in range(cols)] for i in range(rows)]

    # Prepare slots with random positions
    slots = []
    correct_positions = [(j * IMAGE_SIZE, i * IMAGE_SIZE) for i in range(rows) for j in range(cols)]
    random_positions = random.sample(correct_positions, len(correct_positions))
    slots.extend(random_positions)

    # Maintain a list of pieces for drawing in order
    draw_order = list(range(len(slots)))

    # Track if a piece is correctly placed
    correctly_placed = [False] * (rows * cols)

    # Timer variables
    timer = duration * FPS
    timer_font = pygame.font.Font(None, 36)

    # Game variables
    selected_piece = None
    selected_offset_x = 0
    selected_offset_y = 0
    running = True
    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                for i in reversed(draw_order):
                    x, y = slots[i]
                    if x <= mouse_x <= x + IMAGE_SIZE and y <= mouse_y <= y + IMAGE_SIZE:
                        if not correctly_placed[i]:
                            selected_piece = i
                            selected_offset_x = x - mouse_x
                            selected_offset_y = y - mouse_y
                            draw_order.append(draw_order.pop(draw_order.index(i)))
                            break
            elif event.type == pygame.MOUSEBUTTONUP:
                if selected_piece is not None:
                    piece_x, piece_y = slots[selected_piece]
                    correct_x, correct_y = correct_positions[selected_piece]
                    if abs(piece_x - correct_x) <= 30 and abs(piece_y - correct_y) <= 30:
                        slots[selected_piece] = (correct_x, correct_y)
                        correctly_placed[selected_piece] = True
                        for j in draw_order:
                            if j != selected_piece and not correctly_placed[j]:
                                jx, jy = slots[j]
                                if (correct_x, correct_y) == (jx, jy):
                                    draw_order.append(draw_order.pop(draw_order.index(j)))
                        selected_piece = None
                        if all(correctly_placed):
                            show_congratulations(screen, clock, duration, timer)
                            return

            elif event.type == pygame.MOUSEMOTION and selected_piece is not None:
                mouse_x, mouse_y = event.pos
                slots[selected_piece] = (mouse_x + selected_offset_x, mouse_y + selected_offset_y)

        # Timer
        timer -= 1
        if timer <= 0:
            show_times_up(screen)
            return

        # Draw
        screen.fill(WHITE)
        for i in draw_order:
            x, y = slots[i]
            piece = pieces[i // rows][i % cols]
            screen.blit(piece, (x, y))

        # Display timer
        timer_text = timer_font.render(f"Time Left: {timer // FPS} seconds", True, (255, 0, 0))
        screen.blit(timer_text, (10, 10))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

def show_congratulations(screen, clock, duration, timer):

    background_image = pygame.image.load("EndBg.png")
    background_image = pygame.transform.scale(background_image, (600, 600))
    screen.blit(background_image, (0, 0))

    font = pygame.font.Font(None, 45)
    congrats_text = font.render("Congratulations!", True, (0, 255, 0))
    time_taken_text = font.render(f"Time: {duration - (timer // 60)} seconds", True, (75, 0, 130))
    restart_text = font.render("Restart", True, (75, 0, 130))
    menu_text = font.render("Menu", True, (75, 0, 130))

    congrats_rect = congrats_text.get_rect(center=(300, 300))
    time_taken_rect = time_taken_text.get_rect(center=(300, 370))
    restart_rect = restart_text.get_rect(center=(200, 440))
    menu_rect = menu_text.get_rect(center=(400, 440))

    screen.blit(congrats_text, congrats_rect)
    screen.blit(time_taken_text, time_taken_rect)
    screen.blit(restart_text, restart_rect)
    screen.blit(menu_text, menu_rect)

    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                waiting = False
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                if restart_rect.collidepoint(mouse_x, mouse_y):
                    waiting = False
                    main(3, 3, 30)  # Restart with the same difficulty
                elif menu_rect.collidepoint(mouse_x, mouse_y):
                    waiting = False
                    start_menu()

def show_times_up(screen):

    background_image = pygame.image.load("EndBg.png")
    background_image = pygame.transform.scale(background_image, (600, 600))
    screen.blit(background_image, (0, 0))

    font = pygame.font.Font(None, 45)
    time_up_text = font.render("Time's Up!", True, (255, 0, 0))
    restart_text = font.render("Restart", True, (75, 0, 130))
    menu_text = font.render("Menu", True, (75, 0, 130))

    time_up_rect = time_up_text.get_rect(center=(300, 300))
    restart_rect = restart_text.get_rect(center=(200, 370))
    menu_rect = menu_text.get_rect(center=(400, 370))

    screen.blit(time_up_text, time_up_rect)
    screen.blit(restart_text, restart_rect)
    screen.blit(menu_text, menu_rect)

    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                waiting = False
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                if restart_rect.collidepoint(mouse_x, mouse_y):
                    waiting = False
                    main(3, 3, 30)  # Restart with the same difficulty
                elif menu_rect.collidepoint(mouse_x, mouse_y):
                    waiting = False
                    start_menu()

def start_menu():
    pygame.init()
    screen = pygame.display.set_mode((300, 300))
    pygame.display.set_caption("Select Difficulty")

    background_image = pygame.image.load("StartBg.png")

    font = pygame.font.Font(None, 28)
    easy_text = font.render('Easy', True, (75, 0, 130))
    medium_text = font.render('Medium', True, (75, 0, 130))
    hard_text = font.render('Hard', True, (75, 0, 130))

    easy_rect = easy_text.get_rect(center=(150, 155))
    medium_rect = medium_text.get_rect(center=(150, 180))
    hard_rect = hard_text.get_rect(center=(150, 205))

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if easy_rect.collidepoint(event.pos):
                    main(3, 3, 30)  # Duration for Easy level
                elif medium_rect.collidepoint(event.pos):
                    main(4, 4, 40)  # Duration for Medium level
                elif hard_rect.collidepoint(event.pos):
                    main(5, 5, 60)  # Duration for Hard level

        # Draw background image
        screen.blit(background_image, (0, 0))
        
        # Draw text
        screen.blit(easy_text, easy_rect)
        screen.blit(medium_text, medium_rect)
        screen.blit(hard_text, hard_rect)

        pygame.display.flip()

def get_duration(rows, cols):
    if rows == 3 and cols == 3:
        return 30
    elif rows == 4 and cols == 4:
        return 40
    elif rows == 5 and cols == 5:
        return 60
    # Add more conditions for higher levels if needed
    else:
        return 30  # Default duration for unknown levels

start_menu()