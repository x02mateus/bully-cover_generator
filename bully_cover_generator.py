from PIL import Image, ImageFont, ImageDraw

def wrap_text(text, font, max_width, draw):
    # isso ficou meio estranho mas até agora funcionou
    words = text.split()
    lines = []
    current_line = ""

    for word in words:
        test_line = current_line + " " + word if current_line else word
        bbox = draw.textbbox((0, 0), test_line, font=font)
        line_width = bbox[2] - bbox[0]

        if line_width <= max_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word

    if current_line:
        lines.append(current_line)

    return lines

def generate_only_text(text, size, invert_colors):
    if invert_colors == "Y":
        bg_color = 255  # Branco pro bg
        txt_color = 0  # Preto pro texto
    else:
        bg_color = 0  # Preto pro bg
        txt_color = 255  # Branco pro texto

    img = Image.new('RGB', (size, size), (bg_color, bg_color, bg_color))

    try:
        font = ImageFont.truetype("resources/Luke-Thick400.ttf", size // 8) # ajuste fino
    except IOError:
        print("Font file not found! Make sure 'resources/Luke-Thick400.ttf' is in the script folder.")
        return

    draw = ImageDraw.Draw(img)

    max_width = size * 0.9 
    lines = wrap_text(text, font, max_width, draw)
    
    line_spacing = font.size * 1.2
    total_text_height = len(lines) * line_spacing

    y = (size - total_text_height) // 2 

    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font)
        text_width = bbox[2] - bbox[0]
        x = (size - text_width) // 2
        draw.text((x, y), line, (txt_color, txt_color, txt_color), font=font)
        y += line_spacing

    img.save(f'bully_cover_text_{size}.png')
    print(f'Image saved: bully_cover_text_{size}.png')

def generate_full_cover(text, size):
    txt_color = 255  # Branco pro texto

    try:
        img = Image.open(f"resources/covers/{size}.jpg")
    except FileNotFoundError:
        print(f"Error: Cover image 'resources/covers/{size}.jpg' not found.")
        return

    try:
        font = ImageFont.truetype("resources/Luke-Thick400.ttf", size // 8)
    except IOError:
        print("Font file not found! Make sure 'resources/Luke-Thick400.ttf' is in the script folder.")
        return

    draw = ImageDraw.Draw(img)

    max_width = size * 0.9
    lines = wrap_text(text, font, max_width, draw)
    
    line_spacing = font.size * 1.2
    total_text_height = len(lines) * line_spacing

    y = (size - total_text_height) // 2

    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font)
        text_width = bbox[2] - bbox[0]
        x = (size - text_width) // 2
        draw.text((x, y), line, (txt_color, txt_color, txt_color), font=font)
        y += line_spacing

    img.save(f'bully_full_cover_{size}.png')
    print(f'Image saved: bully_full_cover_{size}.png')

mode = input('Choose mode (1 for only text + bg/2 for full album cover): ')

try:
    mode = int(mode)
except ValueError:
    print("Invalid mode input. Please enter 1 or 2.")
    exit()

text = input('Text input: ')

try:
    size = int(input('Size input (256, 512, 1024, 2048): '))
except ValueError:
    print("Invalid size input. Please enter a number.")
    exit()

if mode == 1:
    invert_colors = input('Invert colors? (Y or N): ').strip().upper()
    generate_only_text(text, size, invert_colors)
elif mode == 2:
    generate_full_cover(text, size)
else:
    print("Invalid mode! Please enter 1 or 2.")