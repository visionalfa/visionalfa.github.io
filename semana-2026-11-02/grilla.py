# Simula la grilla de Instagram (3 columnas, lo más nuevo arriba a la izquierda) para chequear que los estilos queden mezclados.
# Uso: python3 grilla.py salida.jpg "27/10|ruta.png" "28/10|ruta.png" ...  (en orden cronológico; ruta "-" = sin imagen)
import sys
from PIL import Image, ImageDraw, ImageFont
# uso: grilla.py salida.jpg item... (item = fecha|ruta ; ruta '-' = desconocido). orden cronologico
out=sys.argv[1]; items=[a.split('|') for a in sys.argv[2:]][::-1]
tw,th=270,338; g=6
rows=(len(items)+2)//3
img=Image.new('RGB',(3*tw+4*g,rows*(th+g)+g),'white'); d=ImageDraw.Draw(img)
f=ImageFont.truetype('/usr/share/fonts/opentype/inter/Inter-Bold.otf',20)
for i,(fe,p) in enumerate(items):
    x=g+(i%3)*(tw+g); y=g+(i//3)*(th+g)
    if p=='-': d.rectangle([x,y,x+tw,y+th],fill='#888')
    else:
        im=Image.open(p).convert('RGB'); r=max(tw/im.width,th/im.height)
        im=im.resize((int(im.width*r)+1,int(im.height*r)+1)); l=(im.width-tw)//2; t=(im.height-th)//2
        img.paste(im.crop((l,t,l+tw,t+th)),(x,y))
    d.rectangle([x,y,x+64,y+28],fill='black'); d.text((x+5,y+3),fe,font=f,fill='yellow')
img.save(out,quality=85)
