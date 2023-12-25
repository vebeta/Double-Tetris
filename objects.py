import pygame


class Board(pygame.sprite.Group):
    # создание поля
    def __init__(self, width, height, screen):
        super().__init__()
        self.screen = screen
        self.width = width
        self.height = height
        self.field = [[None] * width for _ in range(height)]
        self.left = 10
        self.top = 10
        self.cell_size = 30

    # настройка внешнего вида
    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self):
        for row in range(self.height):
            for col in range(self.width):
                pygame.draw.rect(self.screen, 'white',
                                 (self.top + row * self.cell_size, self.left + col * self.cell_size, self.cell_size,
                                  self.cell_size), 1)
                if self.field[row][col]:
                    self.field[row][col].render()


class Shape(pygame.sprite.Group):
    def __init__(self, struct: list, color: tuple, direction: int, coords: tuple, board: Board):
        super().__init__()
        self.color = color
        self.direction = direction
        self.board = board
        self.row, self.col = coords
        self.struct = []
        for i in range(len(struct)):
            self.struct.append([])
            for j in range(len(struct[i])):
                assert struct[i][j] in range(2), "Некорректный формат структуры фигуры"
                if struct[i][j] == 0:
                    self.struct[i].append(None)
                elif struct[i][j] == 1:
                    self.struct[i].append(Cell((i, j), self.color, self, self.board))
                    self.add(self.struct[i][j])

    def render(self, board):
        # функция передающая фигуру
        pass

    def update(self):
        # функция обновляющая координаты фигуры
        for sprite in self.sprites():
            sprite.move()
        pass


class Cell(pygame.sprite.Sprite):
    def __init__(self, coords: tuple, color: tuple, shape: Shape, board: Board):
        super().__init__(shape, board)
        self.row, self.col = coords
        self.color = color
        self.shape = shape
        self.board = board
        self.board.field[self.row + self.shape.row][self.col + self.shape.col] = self

    def update(self, *args):
        self.move(args[0])

    def move(self):
        direction = self.shape.direction
        assert direction in range(4), "Направление движения должно быть в [0; 3]"
        if direction == 0:
            if self.board.field[self.row][self.col - 1]:
                return False
            self.col -= 1
            self.board.field[self.row][self.col + 1] = None
            self.board.field[self.row][self.col] = self
        elif direction == 1:
            if self.board.field[self.row + 1][self.col]:
                return False
            self.row += 1
            self.board.field[self.row - 1][self.col] = None
            self.board.field[self.row][self.col] = self
        elif direction == 2:
            if self.board.field[self.row][self.col + 1]:
                return False
            self.col += 1
            self.board.field[self.row][self.col + 1] = None
            self.board.field[self.row][self.col] = self
        elif direction == 3:
            if self.board.field[self.row - 1][self.y]:
                return False
            self.row -= 1
            self.board.field[self.row][self.col + 1] = None
            self.board.field[self.row][self.col] = self

    def render(self):
        pygame.draw.rect(self.board.screen, self.color, (
            self.board.left + (self.col + self.shape.col) * self.board.cell_size, self.board.top + (self.row + self.shape.row) * self.board.cell_size,
            self.board.cell_size, self.board.cell_size))
