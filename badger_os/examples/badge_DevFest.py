import badger2040
import qrcode

# Global Constants
WIDTH = badger2040.WIDTH
HEIGHT = badger2040.HEIGHT

# --- Text content from a01.jpg ---
COMPANY = "DevFest Kaohsiung 2025"
NAME = "Andy Dai"
TITLE = "GDG Kaohsiung | Android"
DETAILS = "Southern Taiwan Tech Summit" # Combined into one line
QR_CONTENT = "https://www.andyawd.com.tw"


# ------------------------------
#      Drawing functions
# ------------------------------

def draw_badge():
    """
    Draws the badge with the largest possible QR code, perfectly
    centered in the available white space.
    """
    display.set_pen(15)
    display.clear()
    display.set_font("bitmap8")

    # --- Header ---
    display.set_pen(0)
    display.rectangle(0, 0, WIDTH, 30)
    display.set_pen(15)
    company_scale = 2
    company_width = display.measure_text(COMPANY, company_scale)
    company_y = int((30 - (8 * company_scale)) / 2)
    display.text(COMPANY, int((WIDTH - company_width) / 2), company_y, WIDTH, company_scale)

    # --- Footer ---
    display.set_pen(0)
    display.rectangle(0, HEIGHT - 30, WIDTH, 30)
    display.set_pen(15)
    details_scale = 2
    details_width = display.measure_text(DETAILS, details_scale)
    details_y = (HEIGHT - 30) + int((30 - (8 * details_scale)) / 2)
    display.text(DETAILS, int((WIDTH - details_width) / 2), details_y, WIDTH, details_scale)

    # --- QR Code (Right side) ---
    code = qrcode.QRCode()
    code.set_text(QR_CONTENT)
    
    white_space_height = HEIGHT - 60 # 68px
    
    # This calculates the largest possible QR code size (50px)
    size, module_size = measure_qr_code(white_space_height, code)
    
    # This calculation perfectly centers the 50px QR code in the 68px space
    qr_y = 30 + int((white_space_height - size) / 2)
    qr_x = WIDTH - size - 10
    
    draw_qr_code(qr_x, qr_y, code, module_size)

    # --- Main Info (Left side) ---
    display.set_pen(0)
    text_area_width = qr_x - 10

    name_scale = 4
    name_height = 8 * name_scale
    name_width = display.measure_text(NAME, name_scale)
    name_x = int((text_area_width - name_width) / 2)
    
    title_scale = 2
    title_height = 8 * title_scale
    title_width = display.measure_text(TITLE, title_scale)
    title_x = int((text_area_width - title_width) / 2)
    
    total_text_height = name_height + title_height
    gap = int((white_space_height - total_text_height) / 3)
    
    name_y = 30 + gap
    title_y = name_y + name_height + gap

    display.text(NAME, name_x, name_y, text_area_width, name_scale)
    display.text(TITLE, title_x, title_y, text_area_width, title_scale)

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