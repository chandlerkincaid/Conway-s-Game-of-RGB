import random as rand
import time
from openrazer.client import DeviceManager
from openrazer.client import constants as razer_constants

# preset colors
colors = [
    (255, 0, 0),
    (0, 255, 0),
    (0, 0, 255),
    (255, 255, 0),
    (255, 0, 255),
    (0, 255, 255)
]

# Create a DeviceManager. This is used to get specific devices
device_manager = DeviceManager()

print("Found {} Razer devices".format(len(device_manager.devices)))

devices = device_manager.devices
for device in devices:
    if not device.fx.advanced:
        print("Skipping device " + device.name + " (" + device.serial + ")")
        devices.remove(device)
print()

# Disable daemon effect syncing.
# Without this, the daemon will try to set the lighting effect to every device.
device_manager.sync_effects = False

# Helper function to generate interesting colors
kb = devices[0]


def wrap_handle(k, idx_max):
    if k < 0:
        return idx_max
    elif k > idx_max:
        return 0
    else:
        return k


def count_neighbors(matrix, x, y):
    x_bound = len(matrix) - 1
    y_bound = len(matrix[0]) - 1
    l = wrap_handle(x-1, x_bound)
    r = wrap_handle(x+1, x_bound)
    t = wrap_handle(y-1, y_bound)
    b = wrap_handle(y+1, y_bound)
    lt = matrix[l][t]
    mt = matrix[x][t]
    rt = matrix[r][t]
    lm = matrix[l][y]
    rm = matrix[r][y]
    lb = matrix[l][b]
    mb = matrix[x][b]
    rb = matrix[r][b]
    return lt + mt + rt + lm + rm + lb + mb + rb


def get_spawn_color(matrix, x, y):
    x_bound = matrix.fx.advanced.cols - 1
    y_bound = matrix.fx.advanced.rows - 1
    l = wrap_handle(x-1, x_bound)
    r = wrap_handle(x+1, x_bound)
    t = wrap_handle(y-1, y_bound)
    b = wrap_handle(y+1, y_bound)
    lt = matrix.fx.advanced.matrix[t, l]
    mt = matrix.fx.advanced.matrix[t, x]
    rt = matrix.fx.advanced.matrix[t, r]
    lm = matrix.fx.advanced.matrix[y, l]
    rm = matrix.fx.advanced.matrix[y, r]
    lb = matrix.fx.advanced.matrix[b, l]
    mb = matrix.fx.advanced.matrix[b, x]
    rb = matrix.fx.advanced.matrix[b, r]
    current_colors = [lt, mt, rt, lm, rm, lb, mb, rb]
    non_black = [x for x in current_colors if x != (0, 0, 0)]
    return rand.choice(non_black)


def initialize_matrix(data_matrix, display_matrix):
    for x in range(len(data_matrix)):
        for y in range(len(data_matrix[0])):
            if data_matrix[x][y] == 1:
                display_matrix.fx.advanced.matrix[y, x] = rand.choice(colors)
            else:
                display_matrix.fx.advanced.matrix[y, x] = (0, 0, 0)


def update_matrix(data_matrix, display_matrix):
    for x in range(len(data_matrix)):
        for y in range(len(data_matrix[0])):
            count = count_neighbors(data_matrix, x, y)
            if data_matrix[x][y] == 1:
                if count < 2 or count > 3:
                    data_matrix[x][y] = 0
                    display_matrix.fx.advanced.matrix[y, x] = (0, 0, 0)
            else:
                if count == 3:
                    data_matrix[x][y] = 1
                    display_matrix.fx.advanced.matrix[y, x] = get_spawn_color(display_matrix, x, y)
                    # display_matrix.fx.advanced.matrix[y, x] = rand.choice(colors)


    display_matrix.fx.advanced.draw()


con_matrix = [[rand.randint(0, 1) for y in range(kb.fx.advanced.rows)] for x in range(kb.fx.advanced.cols)]
initialize_matrix(con_matrix, kb)

while True:
    update_matrix(con_matrix, kb)
    time.sleep(0.5)
