from tkinter import messagebox, Tk, Canvas, StringVar, Button, Label, Entry
import time
import queue
from node import Node
import threading
# TODO bug if you create a wall over start or finish and you dont set another start


class App:

    def __init__(self, height, width, canvas_size):
        self.window = Tk()
        self.height = height
        self.width = width
        self.speed = 0
        self.squares = 10
        self.canvas_size = canvas_size
        self.square_ratio = canvas_size // self.squares
        self.canvas = Canvas(self.window, width=self.canvas_size, height=self.canvas_size)
        self.start_x = 0
        self.start_y = 0
        self.input_squares = StringVar(value=str(self.squares))
        self.input_speed = StringVar(value=str(self.speed))
        self.grid = [[0 for _ in range(self.squares)] for _ in range(self.squares)]
        self.finish_x = len(self.grid[0]) - 1
        self.finish_y = len(self.grid[1]) - 1
        self.choose_start_permission = False
        self.choose_finish_permission = False
        self.edit_walls_permission = False
        self.should_stop = False
        self.directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, -1), (-1, 1), (-1, -1), (1, 1)]
        self.is_running = False

    def draw_yellow(self, x, y, canvas=None, speed=None):
        if speed is None:
            speed = self.speed
        if canvas is None:
            canvas = self.canvas
        x *= self.square_ratio
        y *= self.square_ratio
        canvas.create_rectangle(x, y, x + self.square_ratio, y + self.square_ratio, fill='yellow')
        canvas.update()
        time.sleep(speed)

    def draw_green(self, x, y, canvas=None, speed=None):
        if speed is None:
            speed = self.speed
        if canvas is None:
            canvas = self.canvas
        x *= self.square_ratio
        y *= self.square_ratio
        canvas.create_rectangle(x, y, x + self.square_ratio, y + self.square_ratio, fill='green')
        canvas.update()
        time.sleep(speed)

    def draw_black(self, x, y, canvas=None, speed=None):
        if speed is None:
            speed = self.speed
        if canvas is None:
            canvas = self.canvas
        x *= self.square_ratio
        y *= self.square_ratio
        canvas.create_rectangle(x, y, x + self.square_ratio, y + self.square_ratio, fill='black')
        canvas.update()
        time.sleep(speed)

    def draw_blue(self, x, y, canvas=None, speed=None):
        if speed is None:
            speed = self.speed
        if canvas is None:
            canvas = self.canvas
        x *= self.square_ratio
        y *= self.square_ratio
        canvas.create_rectangle(x, y, x + self.square_ratio, y + self.square_ratio, fill='blue')
        canvas.update()
        time.sleep(speed)

    def draw_red(self, x, y, canvas=None, speed=None):
        if speed is None:
            speed = self.speed
        if canvas is None:
            canvas = self.canvas
        x *= self.square_ratio
        y *= self.square_ratio
        canvas.create_rectangle(x, y, x + self.square_ratio, y + self.square_ratio, fill='red')
        canvas.update()
        time.sleep(speed)

    def simple_draw(self, x, y, canvas=None, speed=None):
        if not speed:
            speed = self.speed
        if canvas is None:
            canvas = self.canvas
        x *= self.square_ratio
        y *= self.square_ratio
        canvas.create_rectangle(x, y, x + self.square_ratio, y + self.square_ratio, fill='white')
        canvas.update()
        time.sleep(speed)

    def __choose_start(self):
        self.choose_start_permission = True
        self.edit_walls_permission = False
        self.choose_finish_permission = False

    def __edit_walls(self):
        self.edit_walls_permission = True
        self.choose_start_permission = False
        self.choose_finish_permission = False

    def __choose_finish(self):
        self.choose_finish_permission = True
        self.choose_start_permission = False
        self.edit_walls_permission = False

    def quit_app(self):
        self.window.quit()

    def __create_wall(self, event):
        if event.x <= self.canvas_size and event.y <= self.canvas_size and self.edit_walls_permission:
            x = event.x
            y = event.y
            x -= x % self.square_ratio
            y -= y % self.square_ratio
            self.canvas.create_rectangle(x, y, x + self.square_ratio, y + self.square_ratio, fill='black')
            self.grid[x // self.square_ratio][y // self.square_ratio] = -1

    def reset_grid(self, grid=None, canvas=None):
        if canvas is None:
            canvas = self.canvas
        if grid is None:
            grid = self.grid = [[0 for _ in range(self.squares)] for _ in range(self.squares)]
            self.start_x = 0
            self.start_y = 0

        canvas.delete('all')
        canvas.update()
        self.finish_x = len(self.grid[0]) - 1
        self.finish_y = len(self.grid[0]) - 1
        for i in range(0, self.canvas_size, self.square_ratio):
            for j in range(0, self.canvas_size, self.square_ratio):
                if grid[i // self.square_ratio][j // self.square_ratio] == -1:
                    canvas.create_rectangle(i, j, i + self.square_ratio, j + self.square_ratio, fill='black')
                    continue
                canvas.create_rectangle(i, j, i + self.square_ratio, j + self.square_ratio)
        canvas.place(relx=0, rely=0, anchor='nw')
        self.draw_blue(self.start_x, self.start_y, speed=0, canvas=canvas)
        self.draw_red(self.finish_x, self.finish_y, speed=0, canvas=canvas)
        canvas.update()

    def __choose_start_finish(self, event):
        x = event.x
        y = event.y
        if x <= self.canvas_size and y <= self.canvas_size:
            x -= x % self.square_ratio
            y -= y % self.square_ratio
            if self.choose_start_permission:
                self.simple_draw(self.start_x, self.start_y)
                self.start_x = x // self.square_ratio
                self.start_y = y // self.square_ratio
                self.draw_blue(self.start_x, self.start_y, speed=0)
            if self.choose_finish_permission:
                self.simple_draw(self.finish_x, self.finish_y)
                self.finish_x = x // self.square_ratio
                self.finish_y = y // self.square_ratio
                self.draw_red(self.finish_x, self.finish_y, speed=0)

    def update_var(self):
        try:
            self.squares = int(self.input_squares.get())
            self.speed = float(self.input_speed.get())
            self.square_ratio = self.canvas_size // self.squares
            self.reset_grid()
        except ValueError:
            self.__show_error()

    @staticmethod
    def __show_error():
        error_message = messagebox.showerror('Error', 'Please eneter a valid input')

    def run(self):
        self.window.geometry('{0}x{1}'.format(self.width, self.height))
        self.window.title('Algorithm Visualization')
        self.window.bind('<B1-Motion>', self.__create_wall)
        self.window.bind('<Double-Button-1>', self.__choose_start_finish)
        self.window.resizable(False, False)
        y = 50
        start_button = Button(self.window, text='Start Lee', command=self.lee)
        start_button.place(x=850, y=y, width=100)
        y += 50
        start_a_star = Button(self.window, text='Start A*', command=self.a_star)
        start_a_star.place(x=850, y=y, width=100)
        y += 50
        start_a_star = Button(self.window, text='Start both', command=self.start_both)
        start_a_star.place(x=850, y=y, width=100)
        y += 50
        choose_start_b = Button(self.window, text='Choose Start', command=self.__choose_start)
        choose_start_b.place(x=850, y=y, width=100)
        y += 50
        choose_finish_b = Button(self.window, text='Choose Finish', command=self.__choose_finish)
        choose_finish_b.place(x=850, y=y, width=100)
        y += 50
        create_walls_b = Button(self.window, text='Edit Walls', command=self.__edit_walls)
        create_walls_b.place(x=850, y=y, width=100)
        y += 50
        speed_l = Label(text='Speed:', anchor="w")
        speed_l.place(x=850, y=y, width=100)
        y += 20
        speed_e = Entry(self.window, textvariable=self.input_speed)
        speed_e.place(x=850, y=y, width=100)
        y += 50
        rows_l = Label(text='Number of rows:', anchor="w")
        rows_l.place(x=850, y=y, width=100)
        y += 20
        row_e = Entry(self.window, textvariable=self.input_squares)
        row_e.place(x=850, y=y, width=100)
        y += 50
        submit_b = Button(self.window, text='submit', command=self.update_var)
        submit_b.place(x=850, y=y, width=100)


        quit_b = Button(self.window, text='Quit', command=self.quit_app)
        quit_b.place(x=850, y=750, width=100)

        self.reset_grid()
        self.window.mainloop()

    @staticmethod
    def __is_valid_path(x, y, local_grid):
        if x < 0:
            return False
        if y < 0:
            return False
        if x >= len(local_grid[0]):
            return False
        if y >= len(local_grid[0]):
            return False
        if local_grid[x][y] == -1:
            return False
        if local_grid[x][y] == 0:
            return False
        return True

    def __draw_path_lee(self, local_grid):
        x = self.finish_x
        y = self.finish_y
        self.draw_red(x, y)
        ct = 0

        while (x, y) != (self.start_x, self.start_y):
            ct += 1
            for d in self.directions:
                i = d[0]
                j = d[1]
                if self.__is_valid_path(x + i, y + j, local_grid):
                    if local_grid[x + i][y + j] == local_grid[x][y] - 1:
                        x, y = x + i, y + j
                        self.draw_red(x, y)
                        break

        print('Length :', ct)

    @staticmethod
    def __is_valid(x, y, local_grid):
        if x < 0:
            return False
        if y < 0:
            return False
        if x >= len(local_grid[0]):
            return False
        if y >= len(local_grid[0]):
            return False
        if local_grid[x][y] != 0:
            return False
        return True

    def clear(self):
        if not self.is_running:
            self.reset_grid()
        else:
            self.should_stop = True

    def __create_label(self, x, y, *cost):
        text = ''
        for c in cost:
            text = text + ' ' + str(c)
        speed_l = Label(text='{} \n {}'.format(text, sum(cost)))
        speed_l.place(x=x * self.square_ratio, y=y * self.square_ratio, width=self.square_ratio)

    def lee(self):
        q = queue.Queue()
        q.put((self.start_x, self.start_y))
        print(self.grid)
        self.draw_green(self.start_x, self.start_y)
        local_grid = [row[:] for row in self.grid]
        local_grid[self.start_x][self.start_y] = 1
        while not q.empty():
            coord = q.get()
            x = coord[0]
            y = coord[1]
            self.draw_yellow(x, y)

            for d in self.directions:
                i = d[0]
                j = d[1]

                if (x + i, y + j) == (self.finish_x, self.finish_y):
                    print('Finished')
                    local_grid[x + i][y + j] = local_grid[x][y] + 1
                    self.__draw_path_lee(local_grid)
                    break

                if self.__is_valid(x + i, y + j, local_grid):

                    local_grid[x + i][y + j] = local_grid[x][y] + 1
                    self.draw_green(x + i, y + j)
                    q.put((x + i, y + j))
            else:
                continue
            break

    def __calc_g(self, x, y):
        return round(((x - self.start_x) ** 2 + (y - self.start_y) ** 2) ** (1 / 2) * 1000)

    def __calc_h(self, x, y):
        return round(((x - self.finish_x) ** 2 + (y - self.finish_y) ** 2) ** (1 / 2) * 1000)

    def __calc_f(self, x, y):
        return self.__calc_g(x, y) + self.__calc_h(x, y)

    def a_star(self, canvas=None):
        if canvas is None:
            canvas = self.canvas

        maze = [row[:] for row in self.grid]
        start = (self.start_x, self.start_y)
        end = (self.finish_x, self.finish_y)

        start_node = Node(None, start)
        start_node.g = start_node.h = start_node.f = 0
        end_node = Node(None, end)
        end_node.g = end_node.h = end_node.f = 0

        open_list = queue.PriorityQueue()
        closed_list = set()

        # Add the start node
        open_list.put(start_node)
        self.draw_green(start_node.position[0], start_node.position[1], canvas=canvas)

        # Loop until you find the end
        while not open_list.empty():

            # Get the current node
            current_node = open_list.get()

            # Pop lowest f cost off open list, add to closed list
            closed_list.add(current_node)
            self.draw_yellow(current_node.position[0], current_node.position[1], canvas=canvas)

            # Found the goal
            if current_node == end_node:
                path = []
                current = current_node
                while current is not None:
                    path.append(current.position)
                    current = current.parent
                self.__draw_a_star_path(path, canvas=canvas)
                break

            # Generate children
            children = []
            for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1),
                                 (1, 1)]:  # Adjacent squares

                # Get node position
                node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

                # Make sure within range
                if node_position[0] > (len(maze) - 1) or node_position[0] < 0 or node_position[1] > (
                        len(maze[len(maze) - 1]) - 1) or node_position[1] < 0:
                    continue

                # Make sure walkable terrain
                if maze[node_position[0]][node_position[1]] != 0:
                    continue
                maze[node_position[0]][node_position[1]] = 1
                new_node = Node(current_node, node_position)

                children.append(new_node)

            # Loop through children
            for child in children:
                # Child is on the closed list
                for closed_child in closed_list:
                    if child == closed_child:
                        break
                else:
                    # Create the f, g, and h values
                    if current_node - child in ((1, 1), (-1, -1), (1, -1), (-1, 1)):
                        child.g = current_node.g + 1.414213562
                    else:
                        child.g = current_node.g + 1
                    child.h = (((child.position[0] - end_node.position[0]) ** 2) + ((child.position[1] - end_node.position[1]) ** 2)) ** (1/2)
                    child.f = child.g + child.h

                    # Child is already in the open list
                    for open_node in list(open_list.queue):
                        # check if the new path to children is worst or equal
                        # than one already in the open_list (by measuring g)
                        if child == open_node and child.g >= open_node.g:
                            break
                    else:
                        # Add the child to the open list
                        open_list.put(child)
                        self.draw_green(child.position[0], child.position[1], canvas=canvas)

    def __draw_a_star_path(self, path, canvas):
        for p in path:
            self.draw_red(p[0], p[1], canvas=canvas)

    def start_both(self):
        window1 = Tk()
        window1.title('A Star')
        canvas1 = Canvas(window1, height=self.canvas_size, width=self.canvas_size)
        self.reset_grid(grid=self.grid.copy(), canvas=canvas1)
        window1.geometry('{0}x{1}'.format(self.canvas_size, self.canvas_size))
        window1.resizable(False, False)

        t1 = threading.Thread(target=self.a_star, args=[canvas1])
        t2 = threading.Thread(target=self.lee)
        t1.run()
        t2.run()

