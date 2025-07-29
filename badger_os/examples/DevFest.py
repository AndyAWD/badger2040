import badger2040
import qrcode

# Global Constants
WIDTH = badger2040.WIDTH
HEIGHT = badger2040.HEIGHT

# --- Text content from a01.jpg ---
TITLE_TOP = "DevFest Kaohsiung 2025"
TITLE_TOP_SIZE = 2
NAME = "Andy Dai"
NAME_SIZE = 5
TITLE_BOTTOM = "Southern Communities Summit"
TITLE_BOTTOM_SIZE = 2
QR_CONTENT = "https://www.andyawd.com.tw"


# ------------------------------
#      Drawing functions
# ------------------------------

def draw_badge():
    """
    Draws the badge with only the NAME, vertically centered.
    """
    display.set_pen(15)
    display.clear()
    display.set_font("bitmap8")

    # --- Header ---
    display.set_pen(0)
    display.rectangle(0, 0, WIDTH, 30)
    display.set_pen(15)
    company_scale = TITLE_TOP_SIZE
    company_width = display.measure_text(TITLE_TOP, company_scale)
    company_y = int((30 - (8 * company_scale)) / 2)
    display.text(TITLE_TOP, int((WIDTH - company_width) / 2), company_y, WIDTH, company_scale)

    # --- Footer ---
    display.set_pen(0)
    display.rectangle(0, HEIGHT - 30, WIDTH, 30)
    display.set_pen(15)
    details_scale = TITLE_BOTTOM_SIZE
    details_width = display.measure_text(TITLE_BOTTOM, details_scale)
    details_y = (HEIGHT - 30) + int((30 - (8 * details_scale)) / 2)
    display.text(TITLE_BOTTOM, int((WIDTH - details_width) / 2), details_y, WIDTH, details_scale)

    # --- QR Code (Right side) ---
    code = qrcode.QRCode()
    code.set_text(QR_CONTENT)

    white_space_height = HEIGHT - 60  # 68px

    size, module_size = measure_qr_code(white_space_height, code)

    qr_y = 30 + int((white_space_height - size) / 2)
    qr_x = WIDTH - size - 10

    draw_qr_code(qr_x, qr_y, code, module_size)

    # --- Main Info (Left side) ---
    display.set_pen(0)
    text_area_width = qr_x - 10

    # Name (centered vertically in the white space)
    name_scale = NAME_SIZE
    name_height = 8 * name_scale
    name_width = display.measure_text(NAME, name_scale)
    name_x = int((text_area_width - name_width) / 2)
    name_y = 30 + int((white_space_height - name_height) / 2)

    display.text(NAME, name_x, name_y, text_area_width, name_scale)

    display.update()


def measure_qr_code(max_size, code):
    w, h = code.get_size()
    if w == 0: return 0, 0
    module_size = int(max_size / w)
    if module_size < 1: module_size = 1
    return module_size * w, module_size


def draw_qr_code(ox, oy, code, module_size):
    w, h = code.get_size()
    if w == 0: return
    display.set_pen(0)
    for x in range(w):
        for y in range(h):
            if code.get_module(x, y):
                display.rectangle(ox + x * module_size, oy + y * module_size, module_size, module_size)


# ------------------------------
#        Program setup
# ------------------------------
display = badger2040.Badger2040()
display.led(128)
display.set_update_speed(badger2040.UPDATE_NORMAL)
display.set_thickness(2)

# ------------------------------
#       Main program
# ------------------------------
draw_badge()

while True:
    display.keepalive()
    display.halt()
