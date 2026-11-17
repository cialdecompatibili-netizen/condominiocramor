from PIL import Image, ImageDraw, ImageFont
import os
R = r'C:\Users\mirco\Desktop\repository\condominiocramor\assets\images'
W, H = 1200, 630
im = Image.new('RGB', (W, H))
d = ImageDraw.Draw(im)
for y in range(H):
    t = y / H
    d.line([(0, y), (W, y)], fill=(int(54 - 22 * t), int(95 - 32 * t), int(135 - 38 * t)))
ic = Image.open(os.path.join(R, 'favicon-512.png')).convert('RGBA').resize((340, 340), Image.LANCZOS)
im.paste(ic, (90, 145), ic)
b = ImageFont.truetype(r'C:\Windows\Fonts\arialbd.ttf', 78)
s = ImageFont.truetype(r'C:\Windows\Fonts\arial.ttf', 38)
d.text((480, 210), 'Condominio', font=b, fill='white')
d.text((480, 300), 'Cramor', font=b, fill=(170, 190, 210))
d.text((480, 410), 'Amministrazione condominiale a Roma', font=s, fill='white')
im.save(os.path.join(R, 'og-condominio.png'), optimize=True)
