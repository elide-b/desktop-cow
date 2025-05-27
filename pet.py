import random
import tkinter as tk
import time
from win32api import EnumDisplayMonitors, GetMonitorInfo, MonitorFromPoint

# gets monitor(s) information
monitors = EnumDisplayMonitors()
monitor_geometries = [GetMonitorInfo(m[0])['Work'] for m in monitors]
monitor_index = 1 if len(monitor_geometries) > 1 else 0
if len(monitor_geometries) > 1:
    monitor = monitor_geometries[1]
    screen_width = monitor[2]
    screen_height = monitor[3]
    print(screen_width, screen_height)
else:
    monitor = monitor_geometries[0]
    screen_width = monitor[2]
    screen_height = monitor[3]


class Pet:
    def __init__(self):
        self.window = tk.Tk()
        self.screen_bounds = monitor_geometries[monitor_index]

        # load pet gifs
        self.walking_left = [tk.PhotoImage(file='sprites/walking_left.gif', format='gif -index %i' % i) for i in range(4)]
        self.walking_right = [tk.PhotoImage(file='sprites/walking_right.gif', format='gif -index %i' % i) for i in range(4)]
        self.walking_up = [tk.PhotoImage(file='sprites/walking_up.gif', format='gif -index %i' % i) for i in range(4)]
        self.walking_down = [tk.PhotoImage(file='sprites/walking_down.gif', format='gif -index %i' % i) for i in range(4)]
        # self.idle = [tk.PhotoImage(file='C:\\your\\path\\to\\file', format='gif -index %i' % i) for i in range(4)]
        # self.sleep = [tk.PhotoImage(file='C:\\your\\path\\to\\file', format='gif -index %i' % i) for i in range(2)]

        # moving directions
        self.directions = {
            'left': self.walking_left,
            'right': self.walking_right,
            'up': self.walking_up,
            'down': self.walking_down,
        }

        self.direction = random.choice(list(self.directions.keys()))
        self.frames = self.directions[self.direction]

        self.x = int(screen_width * 0.9)
        self.y = int(screen_height * 0.5)

        self.frame_index = 0
        self.img = self.frames[self.frame_index]
        self.img = self.img.subsample(2, 2)
        self.timestamp = time.time()
        self.last_dir_change = time.time()

        # adjusting gifs and window
        self.window.config(highlightbackground='black')
        self.window.overrideredirect(True)
        self.window.attributes('-topmost', True)
        self.window.wm_attributes('-transparentcolor', 'black')
        self.label = tk.Label(self.window, bd=0, bg='black')
        self.label.configure(image=self.img)
        self.label.pack()

        w = self.img.width()
        h = self.img.height()
        self.window.geometry(f'{w}x{h}+{self.x}+{self.y}')
        self.window.after(0, self.update)

        # arrow keys movement
        self.window.bind('<Left>', lambda e: self.set_direction('left'))
        self.window.bind('<Right>', lambda e: self.set_direction('right'))
        self.window.bind('<Up>', lambda e: self.set_direction('up'))
        self.window.bind('<Down>', lambda e: self.set_direction('down'))
        self.window.focus_force()

        self.window.mainloop()

    def set_direction(self, dir):
        self.direction = dir
        self.frames = self.directions[dir]

    def move(self):
        pet_width = self.img.width()
        pet_height = self.img.height()

        hit_wall = False
        blocked_direction = None

        if self.direction == 'left':
            if self.x <= self.screen_bounds[0]:
                hit_wall = True
                blocked_direction = 'left'
            else:
                self.x -= 1

        elif self.direction == 'right':
            if self.x + pet_width >= self.screen_bounds[2]:
                hit_wall = True
                blocked_direction = 'right'
            else:
                self.x += 1

        elif self.direction == 'up':
            if self.y <= self.screen_bounds[1]:
                hit_wall = True
                blocked_direction = 'up'
            else:
                self.y -= 1

        elif self.direction == 'down':
            if self.y + pet_height >= self.screen_bounds[3]:
                hit_wall = True
                blocked_direction = 'down'
            else:
                self.y += 1

        if hit_wall:
            possible_directions = ['left', 'right', 'up', 'down']
            possible_directions.remove(blocked_direction)
            new_direction = random.choice(possible_directions)
            self.set_direction(new_direction)

    def update(self):
        now = time.time()

        # random direction every 5 seconds
        if now - self.last_dir_change > 5:
            self.direction = random.choice(list(self.directions.keys()))
            self.frames = self.directions[self.direction]
            self.last_dir_change = now

        # animate
        if now - self.timestamp > 0.3:
            self.timestamp = now
            self.frame_index = (self.frame_index + 1) % len(self.frames)
            self.img = self.frames[self.frame_index]
            self.img = self.img.subsample(2, 2)

        self.move()
        w = self.img.width()
        h = self.img.height()
        self.window.geometry(f'{w}x{h}+{self.x}+{self.y}')
        self.label.configure(image=self.img)

        self.window.after(30, self.update)


Pet()