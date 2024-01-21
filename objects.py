import pygame
from methods import make_radius


class Board(pygame.sprite.Group):
    # создание поля
    def __init__(self, width: int, height: int, screen: pygame.Surface, field: str):
        super().__init__()
        self.screen = screen
        self.width = width
        self.height = height
        field = [list(map(int, row.split())) for row in field.split('\n')]
        self.radius, self.colors = make_radius(field)
        assert len(field) == self.height and len(field[0]) == self.width, "Размеры поля и карты отличаются"
        self.field = []
        for i in range(len(field)):
            self.field.append([])
            for j in range(len(field[i])):
                self.field[i].append((StopCell((i, j), (100, 100, 100), self) if field[i][j] == 1 else None))
        self.left = 10
        self.top = 10
        self.cell_size = 30

    # настройка внешнего вида
    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def update_field(self):
        self.field = [[None] * self.width for _ in range(self.height)]
        for sprite in self.sprites():
            if type(sprite) is MovingCell:
                self.field[sprite.row + sprite.shape.row][sprite.col + sprite.shape.col] = sprite
            else:
                self.field[sprite.row][sprite.col] = sprite

    def check(self):
        colors_filled = {}
        for i in range(len(self.field)):
            for j in range(len(self.field[i])):
                if type(self.field[i][j]) is MovingCell:
                    colors_filled[self.radius[i][j]] = colors_filled.get(self.radius[i][j], 0) + 1
        for i in range(2, len(self.colors) + 2):
            if colors_filled.get(i, 0) == self.colors[i]:
                self.delete(i)
                return

    def delete(self, color):
        for i in range(len(self.field)):
            for j in range(len(self.field[i])):
                if self.radius[i][j] == color:
                    self.field[i][j].kill()

    def render(self):
        for row in range(self.height):
            for col in range(self.width):
                pygame.draw.rect(self.screen, 'white',
                                 (self.top + col * self.cell_size, self.left + row * self.cell_size, self.cell_size,
                                  self.cell_size), 1)
                if self.field[row][col]:
                    self.field[row][col].render()


class Shape(pygame.sprite.Group):
    def __init__(self, struct: list, color: tuple, coords: tuple, direction: int, board: Board):
        super().__init__()
        self.color = color
        self.board = board
        self.direction = direction
        self.row, self.col = coords
        self.struct = []
        for i in range(len(struct)):
            self.struct.append([])
            for j in range(len(struct[i])):
                assert struct[i][j] in range(2), "Некорректный формат структуры фигуры"
                if struct[i][j] == 0:
                    self.struct[i].append(None)
                elif struct[i][j] == 1:
                    self.struct[i].append(MovingCell((i, j), self.color, self, self.board))
                    self.add(self.struct[i][j])
        self.width = len(self.struct[0])
        self.height = len(self.struct)

    def update(self, *args):
        if args[0] == 'm':
            self.move(args[1])

    def move(self, direction=None):
        # функция обновляющая координаты фигуры
        if not direction:
            direction = self.direction
        for sprite in self.sprites():
            if sprite.move(direction) is False:
                return False
        if direction == 0:
            self.row -= 1
        elif direction == 1:
            self.col += 1
        elif direction == 2:
            self.row += 1
        elif direction == 3:
            self.col -= 1


class Cell(pygame.sprite.Sprite):
    def __init__(self, coords: tuple, color: tuple, board: Board):
        super().__init__(board)
        self.row, self.col = coords
        self.color = color
        self.board = board
        self.board.add(self)

    def render(self):
        pygame.draw.rect(self.board.screen, self.color, (
            self.board.left + self.col * self.board.cell_size,
            self.board.top + self.row * self.board.cell_size,
            self.board.cell_size, self.board.cell_size))


class StopCell(Cell):
    pass


class MovingCell(Cell):
    def __init__(self, coords: tuple, color: tuple, shape: Shape, board: Board):
        super().__init__(coords, color, board)
        self.shape = shape
        self.board.field[self.row + self.shape.row][self.col + self.shape.col] = self
        shape.add(self)

    def move(self, direction):
        assert direction in range(4), "Направление движения должно быть в [0; 3]"
        try:
            if direction == 0:
                if self.shape.row + self.row == 0:
                    return False
                if self.board.field[self.shape.row + self.row - 1][self.shape.col + self.col] and \
                        self.board.field[self.shape.row + self.row - 1][
                            self.shape.col + self.col] not in self.shape.sprites():
                    return False
            elif direction == 1:
                if self.board.field[self.shape.row + self.row][self.shape.col + self.col + 1] and \
                        self.board.field[self.shape.row + self.row][
                            self.shape.col + self.col + 1] not in self.shape.sprites():
                    return False
            elif direction == 2:
                if self.board.field[self.shape.row + self.row + 1][self.shape.col + self.col] and \
                        self.board.field[self.shape.row + self.row + 1][
                            self.shape.col + self.col] not in self.shape.sprites():
                    return False
            elif direction == 3:
                if self.shape.col + self.col == 0:
                    return False
                if self.board.field[self.shape.row + self.row][self.shape.col + self.col - 1] and \
                        self.board.field[self.shape.row + self.row][
                            self.shape.col + self.col - 1] not in self.shape.sprites():
                    return False
        except IndexError:
            return False

    def render(self):
        pygame.draw.rect(self.board.screen, self.color, (
            self.board.left + (self.col + self.shape.col) * self.board.cell_size,
            self.board.top + (self.row + self.shape.row) * self.board.cell_size,
            self.board.cell_size, self.board.cell_size))
