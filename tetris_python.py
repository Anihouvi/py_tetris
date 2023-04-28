import pygame
import random

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Grid size
GRID_SIZE = 25

# Tetris shapes
SHAPES = [
    # Line
    [
        ["0", "0", "0", "0"],
        ["1", "1", "1", "1"],
        ["0", "0", "0", "0"],
        ["0", "0", "0", "0"]
    ],
    # T
    [
        ["0", "1", "0"],
        ["1", "1", "1"],
        ["0", "0", "0"]
    ],
    # L
    [
        ["1", "0", "0"],
        ["1", "1", "1"],
        ["0", "0", "0"]
    ],
    # J
    [
        ["0", "0", "1"],
        ["1", "1", "1"],
        ["0", "0", "0"]
    ],
    # Z
    [
        ["1", "1", "0"],
        ["0", "1", "1"],
        ["0", "0", "0"]
    ],
    # S
    [
        ["0", "1", "1"],
        ["1", "1", "0"],
        ["0", "0", "0"]
    ],
    # O
    [
        ["1", "1"],
        ["1", "1"]
    ]
]


def main():
    pygame.init()

    size = [SCREEN_WIDTH, SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size)

    pygame.display.set_caption("Tetris By Anihouvi")

    done = False
    clock = pygame.time.Clock()

    while not done:
        # --- Event processing
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            # Add code to handle user input here

        # --- Game logic should go here

        # --- Drawing code
        screen.fill(BLACK)

        # Add code to draw grid, shapes, and score here

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


# Tetris game dimensions
GRID_WIDTH = 10
GRID_HEIGHT = 20


# Tetris game class
class Tetris:
    def __init__(self):
        self.grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        self.current_piece = self.new_piece()
        self.piece_x = GRID_WIDTH // 2
        self.piece_y = 0
        self.score = 0

    def new_piece(self):
        return random.choice(SHAPES)

    def rotate_piece(self):
        return list(zip(*reversed(self.current_piece)))

    def valid_move(self, x, y, piece):
        for row in range(len(piece)):
            for col in range(len(piece[row])):
                try:
                    if piece[row][col] == "1" and (self.grid[y + row][x + col] != 0 or x + col < 0 or x + col >= GRID_WIDTH):
                        return False
                except IndexError:
                    if piece[row][col] == "1":
                        return False
        return True

    def move_piece(self, dx, dy):
        new_x = self.piece_x + dx
        new_y = self.piece_y + dy
        if self.valid_move(new_x, new_y, self.current_piece):
            self.piece_x = new_x
            self.piece_y = new_y
            return True
        return False

    def rotate(self):
        rotated_piece = self.rotate_piece()
        if self.valid_move(self.piece_x, self.piece_y, rotated_piece):
            self.current_piece = rotated_piece

    def lock_piece(self):
        for row in range(len(self.current_piece)):
            for col in range(len(self.current_piece[row])):
                if self.current_piece[row][col] == "1":
                    self.grid[self.piece_y + row][self.piece_x + col] = 1
        self.current_piece = self.new_piece()
        self.piece_x = GRID_WIDTH // 2
        self.piece_y = 0
        if not self.valid_move(self.piece_x, self.piece_y, self.current_piece):
            return False
        return True

    def clear_lines(self):
        lines_to_clear = []
        for row in range(GRID_HEIGHT):
            if all(cell == 1 for cell in self.grid[row]):
                lines_to_clear.append(row)
        for row in lines_to_clear:
            self.grid.pop(row)
            self.grid.insert(0, [0 for _ in range(GRID_WIDTH)])

        lines_cleared = len(lines_to_clear)
        if lines_cleared == 1:
            self.score += 100
        elif lines_cleared == 2:
            self.score += 300
        elif lines_cleared == 3:
            self.score += 500
        elif lines_cleared == 4:
            self.score += 800

        return lines_cleared


def draw_grid(screen, game):
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            pygame.draw.rect(screen, WHITE if game.grid[y][x] else BLACK,
                             pygame.Rect(x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE - 1, GRID_SIZE - 1))


def draw_piece(screen, game, piece, x, y):
    for row in range(len(piece)):
        for col in range(len(piece[row])):
            if piece[row][col] == "1":
                pygame.draw.rect(screen, WHITE, pygame.Rect((x + col) * GRID_SIZE,
                                                            (y + row) * GRID_SIZE, GRID_SIZE - 1, GRID_SIZE - 1))


def draw_score(screen, game):
    font = pygame.font.Font(None, 36)
    text = font.render(f"Score: {game.score}", True, WHITE)
    screen.blit(text, (10, 10))


# Will finish implementing in v1
def draw_game_over(screen):
    font = pygame.font.Font(None, 48)
    text = font.render("Game Over", True, WHITE)
    screen.blit(text, (screen.get_width() // 2 - text.get_width() // 2,
                       screen.get_height() // 2 - text.get_height() // 2))


def main():
    pygame.init()

    size = [GRID_WIDTH * GRID_SIZE, GRID_HEIGHT * GRID_SIZE]
    screen = pygame.display.set_mode(size)

    pygame.display.set_caption("Tetris By Anihouvi")

    game = Tetris()
    done = False
    clock = pygame.time.Clock()
    gravity_timer = pygame.time.get_ticks()

    while not done:
        # --- Event processing
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    game.move_piece(-1, 0)
                elif event.key == pygame.K_RIGHT:
                    game.move_piece(1, 0)
                elif event.key == pygame.K_DOWN:
                    game.move_piece(0, 1)
                elif event.key == pygame.K_UP:
                    game.rotate()

        # --- Game logic
        if pygame.time.get_ticks() - gravity_timer > 500:
            if not game.move_piece(0, 1):
                if not game.lock_piece():
                    break
                game.clear_lines()
            gravity_timer = pygame.time.get_ticks()

        # --- Drawing code
        screen.fill(BLACK)
        draw_grid(screen, game)
        draw_score(screen, game)
        draw_piece(screen, game, game.current_piece, game.piece_x, game.piece_y)

        # If the game is over draw the "Game Over" message
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()

