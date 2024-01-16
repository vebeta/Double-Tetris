def make_radius(field):
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

