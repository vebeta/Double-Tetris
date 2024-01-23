import pygame


def rotate_matrix(matrix):
    rotated_matrix = [[0 for i in range(len(matrix))] for i in range(len(matrix[0]))]
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            rotated_matrix[j][i] = matrix[len(matrix) - i - 1][j]
    return rotated_matrix


class Board(pygame.sprite.Group):
    # создание поля
    def __init__(self, width: int, height: int, screen: pygame.Surface, field: str):
        super().__init__()
        self.screen = screen
        self.width = width
        self.height = height
        field = [list(map(int, row.split())) for row in field.split('\n')]
        self.field = []
        for i in range(len(field)):
            self.field.append([])
            for j in range(len(field[i])):
                self.field[i].append((StopCell((i, j), (100, 100, 100), self) if field[i][j] == 1 else None))
        assert len(field) == self.height and len(field[0]) == self.width, "Размеры поля и карты отличаются"
        self.radius, self.colors = self.make_radius(field)
        self.left = 10
        self.top = 10
        self.cell_size = 30

    def make_radius(self, field):
        radius = field.copy()
        cl = 1
        cnt = 0
        colors = {}
        while 0 in [radius[i][j] for i in range(len(field)) for j in range(len(field[i]))]:
            for i in range(len(field)):
                for j in range(len(field[0])):
                    if radius[i][j] != 0:
                        continue
                    if i > 0 and radius[i - 1][j] == cl:
                        radius[i][j] = cl + 1
                        cnt += 1
                    elif i > 0 and j > 0 and radius[i - 1][j - 1] == cl:
                        radius[i][j] = cl + 1
                        cnt += 1
                    elif j > 0 and radius[i][j - 1] == cl:
                        radius[i][j] = cl + 1
                        cnt += 1
                    elif j > 0 and i < len(field) - 1 and radius[i + 1][j - 1] == cl:
                        radius[i][j] = cl + 1
                        cnt += 1
                    elif i < len(field) - 1 and radius[i + 1][j] == cl:
                        radius[i][j] = cl + 1
                        cnt += 1
                    elif i < len(field) - 1 and j < len(field[0]) - 1 and radius[i + 1][j + 1] == cl:
                        radius[i][j] = cl + 1
                        cnt += 1
                    elif j < len(field[0]) - 1 and radius[i][j + 1] == cl:
                        radius[i][j] = cl + 1
                        cnt += 1
                    elif i > 0 and j < len(field[0]) - 1 and radius[i - 1][j + 1] == cl:
                        radius[i][j] = cl + 1
                        cnt += 1
            colors[cl + 1] = cnt
            cl += 1
            cnt = 0
        return radius, colors

    # настройка внешнего вида
    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def update_field(self):
        self.field = [[None] * self.width for _ in range(self.height)]
        for sprite in self.sprites():
            if type(sprite) is MovingCell and sprite.shape:
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
                self.move_shapes()
                return True
        return False

    def delete(self, color):
        for i in range(len(self.field)):
            for j in range(len(self.field[i])):
                if self.radius[i][j] == color:
                    self.field[i][j].kill()
                    self.field[i][j] = None

    def move_shapes(self):
        flag = True
        while flag:
            flag = False
            for i in range(len(self.field)):
                for j in range(len(self.field[i])):
                    if type(self.field[i][j]) is MovingCell and self.field[i][j].can_move():
                        flag = True
                        self.field[i][j].move()

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
        self.struct = struct
        self.cells = []
        self.moving = True
        for i in range(len(self.struct)):
            self.cells.append([])
            for j in range(len(self.struct[i])):
                assert self.struct[i][j] in range(2), "Некорректный формат структуры фигуры"
                if self.struct[i][j] == 0:
                    self.cells[i].append(None)
                elif self.struct[i][j] == 1:
                    self.cells[i].append(MovingCell((i, j), self.color, self, self.board))
                    self.add(self.cells[i][j])
        self.width = len(self.struct[0])
        self.height = len(self.struct)

    def move(self, direction=None):
        # функция обновляющая координаты фигуры
        if not direction:
            direction = self.direction
        for sprite in self.sprites():
            if sprite.can_move(direction) is False:
                return False
        if direction == 0:
            self.row -= 1
        elif direction == 1:
            self.col += 1
        elif direction == 2:
            self.row += 1
        elif direction == 3:
            self.col -= 1

    def make_cells(self):
        self.cells = []
        for i in range(len(self.struct)):
            self.cells.append([])
            for j in range(len(self.struct[i])):
                assert self.struct[i][j] in range(2), "Некорректный формат структуры фигуры"
                if self.struct[i][j] == 0:
                    self.cells[i].append(None)
                elif self.struct[i][j] == 1:
                    self.cells[i].append(MovingCell((i, j), self.color, self, self.board))
                    self.add(self.cells[i][j])
        self.width = len(self.struct[0])
        self.height = len(self.struct)

    def stop_shape(self):
        if not self.moving:
            return
        self.moving = False
        for i in range(len(self.cells)):
            for j in range(len(self.cells[i])):
                if self.cells[i][j]:
                    self.cells[i][j].stop()

    def rotate(self):
        for i in range(len(self.cells)):
            for j in range(len(self.cells[0])):
                if self.cells[i][j]:
                    self.cells[i][j].kill()
        self.struct = rotate_matrix(self.struct)
        self.make_cells()
        self.width = len(self.struct[0])
        self.height = len(self.struct)


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
        self.direction = None
        shape.add(self)

    def can_move(self, direction=None):
        if not direction:
            direction = self.direction
        assert direction in range(4), "Направление движения должно быть в [0; 3]"
        try:
            if self.shape:
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
            else:
                if direction == 0:
                    if self.row == 0:
                        return False
                    if self.board.field[self.row - 1][self.col]:
                        return False
                elif direction == 1:
                    if self.board.field[self.row][self.col + 1]:
                        return False
                elif direction == 2:
                    if self.board.field[self.row + 1][self.col]:
                        return False
                elif direction == 3:
                    if self.col == 0:
                        return False
                    if self.board.field[self.row][self.col - 1]:
                        return False
        except IndexError:
            return False
        return True

    def stop(self):
        self.direction = self.shape.direction
        self.row += self.shape.row
        self.col += self.shape.col
        self.shape = None

    def move(self, direction=None):
        if not direction:
            direction = self.direction
        if self.can_move(direction):
            if direction == 0:
                self.board.field[self.row][self.col] = None
                self.row -= 1
                self.board.field[self.row][self.col] = self
            elif direction == 1:
                self.board.field[self.row][self.col] = None
                self.col += 1
                self.board.field[self.row][self.col] = self
            elif direction == 2:
                self.board.field[self.row][self.col] = None
                self.row += 1
                self.board.field[self.row][self.col] = self
            elif direction == 3:
                self.board.field[self.row][self.col] = None
                self.col -= 1
                self.board.field[self.row][self.col] = self

    def render(self):
        if self.shape:
            pygame.draw.rect(self.board.screen, self.color, (
                self.board.left + (self.col + self.shape.col) * self.board.cell_size,
                self.board.top + (self.row + self.shape.row) * self.board.cell_size,
                self.board.cell_size, self.board.cell_size))
        else:
            super().render()
