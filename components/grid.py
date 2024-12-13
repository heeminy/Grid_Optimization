from practice_code.body import Body

class Grid:
    def __init__(self, screen_width, screen_height, x_num, y_num):
        self.x_max = x_num - 1
        self.y_max = y_num - 1
        self.width = screen_width / x_num
        self.height = screen_height / y_num
        self.grids = []

        for _ in range (x_num + 1):
            x_index_list = []
            for _ in range (y_num + 1):
                x_index_list.append([])
            self.grids.append(x_index_list)

    def object_allocation(self, obj:Body):

        min_x = obj.box[0] / self.width
        min_y = obj.box[1] / self.height
        max_x = int(obj.box[2] // self.width)
        max_y = int(obj.box[3] // self.height)

        if max_x < 0 or max_y < 0 or min_x > self.x_max or min_y > self.y_max:
            #Objects outside the grid are not handled for now.
            return

        if min_x > 0 and int(min_x) == min_x:
            min_x -= 1
        if min_y > 0 and int(min_y) == min_y:
            min_y -= 1
        min_x = int(min_x)
        min_y = int(min_y)


        for x in range(min_x, max_x + 1):
            for y in range(min_y, max_y + 1):
                self.grids[x][y].append(obj)







    