import badger2040
import jpegdec
import pngdec

# Global Constants
WIDTH = badger2040.WIDTH
HEIGHT = badger2040.HEIGHT

IMAGE_WIDTH = 104

COMPANY_HEIGHT = 30
DETAILS_HEIGHT = 20
NAME_HEIGHT = HEIGHT - COMPANY_HEIGHT - (DETAILS_HEIGHT * 2) - 2
TEXT_WIDTH = WIDTH - IMAGE_WIDTH - 1

COMPANY_TEXT_SIZE = 2
DETAILS_TEXT_SIZE = 2

LEFT_PADDING = 5
NAME_PADDING = 20
DETAIL_SPACING = 10

BADGE_PATH = "/badges/badge.txt"

DEFAULT_TEXT = """mustelid inc
H. Badger
RP2040
2MB Flash
E ink
296x128px
/badges/badge.jpg
"""


# ------------------------------
#      Utility functions
# ------------------------------


# Reduce the size of a string until it fits within a given width
def truncatestring(text, text_size, width):
    while True:
        length = display.measure_text(text, text_size)
        if length > 0 and length > width:
            text = text[:-1]
        else:
            text += ""
            return text


# ------------------------------
#      Drawing functions
# ------------------------------

# Draw the badge, including user text
def draw_badge():
    display.set_pen(0)
    display.clear()

    try:
        # Draw badge image
        png.open_file(badge_image)
        png.decode(WIDTH - IMAGE_WIDTH, 0)
    except (OSError, RuntimeError):
        try:
            # Draw badge image
            jpeg.open_file(badge_image)
            jpeg.decode(WIDTH - IMAGE_WIDTH, 0)
        except (OSError, RuntimeError):
            display.set_pen(15)
            display.rectangle(WIDTH - IMAGE_WIDTH, 0, IMAGE_WIDTH, HEIGHT)
            display.set_pen(0)
            display.text("Image", WIDTH - IMAGE_WIDTH + 4, (HEIGHT // 2) - 4, 1.0)
            display.text("not found", WIDTH - IMAGE_WIDTH + 4, (HEIGHT // 2) + 4, 1.0)


    # Draw a border around the image
    display.set_pen(0)
    display.line(WIDTH - IMAGE_WIDTH, 0, WIDTH - 1, 0)
    display.line(WIDTH - IMAGE_WIDTH, 0, WIDTH - IMAGE_WIDTH, HEIGHT - 1)
    display.line(WIDTH - IMAGE_WIDTH, HEIGHT - 1, WIDTH - 1, HEIGHT - 1)
    display.line(WIDTH - 1, 0, WIDTH - 1, HEIGHT - 1)

    # Uncomment this if a white background is wanted behind the company
    # display.set_pen(15)
    # display.rectangle(1, 1, TEXT_WIDTH, COMPANY_HEIGHT - 1)

    # Draw the company
    display.set_pen(15)  # Change this to 0 if a white background is used
    display.set_font("bitmap8")

    # Integer scale for bitmap fonts, must be 1 or greater
    company_scale = int(COMPANY_TEXT_SIZE)
    if company_scale < 1:
        company_scale = 1

    # Calculate the scaled dimensions of the text
    company_width = display.measure_text(company, company_scale)
    company_height = 6 * company_scale  # Height of the "bitmap6" font multiplied by the scale

    # Calculate text position for horizontal and vertical centering
    company_x = (TEXT_WIDTH - company_width) // 2
    company_y = (COMPANY_HEIGHT - company_height) // 2

    display.text(company, company_x, company_y, WIDTH, company_scale)

    # Draw a white background behind the name
    display.set_pen(20)
    display.rectangle(1, COMPANY_HEIGHT + 1, TEXT_WIDTH, NAME_HEIGHT)

    # Draw the name, scaling it to fit and centering it
    display.set_pen(0)
    display.set_font("bitmap8")

    # Find the largest integer scale that fits
    name_size = 4  # A sensible starting scale
    while name_size > 0:
        name_width = display.measure_text(name, name_size)
        name_height = 6 * name_size
        if name_width < (TEXT_WIDTH - NAME_PADDING) and name_height < NAME_HEIGHT:
            break
        name_size -= 1

    if name_size == 0:  # If no scale fits, use scale 1 and let it clip
        name_size = 1

    # Recalculate final dimensions with the chosen scale
    name_width = display.measure_text(name, name_size)
    name_height = 6 * name_size

    # Calculate position for horizontal and vertical centering
    name_x = (TEXT_WIDTH - name_width) // 2
    name_y = COMPANY_HEIGHT + 1 + (NAME_HEIGHT - name_height) // 2

    display.text(name, name_x, name_y, WIDTH, name_size)

    # Draw a white backgrounds behind the details
    display.set_pen(15)
    display.rectangle(1, HEIGHT - DETAILS_HEIGHT * 2, TEXT_WIDTH, DETAILS_HEIGHT - 1)
    display.rectangle(1, HEIGHT - DETAILS_HEIGHT, TEXT_WIDTH, DETAILS_HEIGHT - 1)

    # Draw the first detail's title and text
    display.set_pen(0)
    display.set_font("bitmap8")

    # Integer scale for bitmap fonts, must be 1 or greater
    details_scale = int(DETAILS_TEXT_SIZE)
    if details_scale < 1:
        details_scale = 1

    # Calculate the scaled height of the font for vertical centering
    scaled_font_height = 6 * details_scale

    # Calculate the Y position for the first detail line
    detail1_y = (HEIGHT - DETAILS_HEIGHT * 2) + (DETAILS_HEIGHT - scaled_font_height) // 2

    name_length = display.measure_text(detail1_title, details_scale)
    display.text(detail1_title, LEFT_PADDING, detail1_y, WIDTH, details_scale)
    display.text(detail1_text, 5 + name_length + DETAIL_SPACING, detail1_y, WIDTH, details_scale)

    # Calculate the Y position for the second detail line
    detail2_y = (HEIGHT - DETAILS_HEIGHT) + (DETAILS_HEIGHT - scaled_font_height) // 2

    # Draw the second detail's title and text
    name_length = display.measure_text(detail2_title, details_scale)
    display.text(detail2_title, LEFT_PADDING, detail2_y, WIDTH, details_scale)
    display.text(detail2_text, LEFT_PADDING + name_length + DETAIL_SPACING, detail2_y, WIDTH, details_scale)

    display.update()


# ------------------------------
#        Program setup
# ------------------------------

# Create a new Badger and set it to update NORMAL
display = badger2040.Badger2040()
display.led(128)
display.set_update_speed(badger2040.UPDATE_NORMAL)
display.set_thickness(2)

jpeg = jpegdec.JPEG(display.display)
png = pngdec.PNG(display.display)

# Open the badge file
try:
    badge = open(BADGE_PATH, "r")
except OSError:
    with open(BADGE_PATH, "w") as f:
        f.write(DEFAULT_TEXT)
        f.flush()
    badge = open(BADGE_PATH, "r")

# Read in the next 6 lines
company = badge.readline()  # "mustelid inc"
name = badge.readline()  # "H. Badger"
detail1_title = badge.readline()  # "RP2040"
detail1_text = badge.readline()  # "2MB Flash"
detail2_title = badge.readline()  # "E ink"
detail2_text = badge.readline()  # "296x128px"
badge_image = badge.readline()  # /badges/badge.jpg

# Truncate all of the text (except for the name as that is scaled)
company_scale = int(COMPANY_TEXT_SIZE)
if company_scale < 1:
    company_scale = 1
company = truncatestring(company, company_scale, TEXT_WIDTH)

details_scale = int(DETAILS_TEXT_SIZE)
if details_scale < 1:
    details_scale = 1

detail1_title = truncatestring(detail1_title, details_scale, TEXT_WIDTH)
detail1_text = truncatestring(detail1_text, details_scale,
                              TEXT_WIDTH - DETAIL_SPACING - display.measure_text(detail1_title, details_scale))

detail2_title = truncatestring(detail2_title, details_scale, TEXT_WIDTH)
detail2_text = truncatestring(detail2_text, details_scale,
                              TEXT_WIDTH - DETAIL_SPACING - display.measure_text(detail2_title, details_scale))

# ------------------------------
#       Main program
# ------------------------------

draw_badge()

while True:
    # Sometimes a button press or hold will keep the system
    # powered *through* HALT, so latch the power back on.
    display.keepalive()

    # If on battery, halt the Badger to save power, it will wake up if any of the front buttons are pressed
    display.halt()
