import sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter
F='/root/.claude/plugins/synced/e81de710-9b8b-4ec0-a06a-05f593170cdd_e674f652-3c2a-4772-984c-db5160d57a6a/lesson-follow-up/skills/study-notes/assets/fonts/'
SRC='/mnt/user-data/uploads/Claude-exchange/'
TEAL=(14,131,136); TEAL_D=(10,92,96); CORAL=(251,106,90); BG=(236,247,247)
cards=[('notes','src-study-notes.jpg','Study Notes'),('practice','src-practice.jpg','Practice Exercises'),
       ('quiz','src-quiz.jpg','Self-check Quiz'),('workbook','src-workbook.jpg','Workbook')]
W,H=480,600; R=36; S=2  # supersample
def card(slug,src,label):
    w,h=W*S,H*S
    im=Image.new('RGBA',(w,h),(0,0,0,0))
    mask=Image.new('L',(w,h),0); ImageDraw.Draw(mask).rounded_rectangle([0,0,w-1,h-1],R*S,fill=255)
    base=Image.new('RGBA',(w,h),(255,255,255,255))
    d=ImageDraw.Draw(base)
    # mascot area
    m=Image.open(SRC+src).convert('RGB'); m=m.resize((w,w),Image.LANCZOS)
    base.paste(m,(0,0))
    # label bar
    bar_y=w-int(10*S)
    d.rectangle([0,bar_y,w,h],fill=TEAL)
    d.rectangle([0,bar_y,w,bar_y+8*S],fill=CORAL)
    fb=ImageFont.truetype(F+'Montserrat-Bold.ttf',38*S); fr=ImageFont.truetype(F+'Montserrat-Bold.ttf',22*S)
    size=38*S
    while d.textlength(label,font=fb)>w-60*S: size-=2*S; fb=ImageFont.truetype(F+'Montserrat-Bold.ttf',size)
    cy=bar_y+8*S+(h-bar_y-8*S)//2
    d.text((w//2,cy-16*S),label,font=fb,fill='white',anchor='mm')
    d.text((w//2,cy+30*S),'OPEN  ›',font=fr,fill=(255,214,208),anchor='mm')
    im.paste(base,(0,0),mask)
    # thin teal border
    ImageDraw.Draw(im).rounded_rectangle([S,S,w-1-S,h-1-S],R*S,outline=TEAL+(255,),width=4*S)
    im=im.resize((W,H),Image.LANCZOS)
    out=f'goodman-card-{slug}.png'
    im.quantize(colors=256,method=Image.Quantize.FASTOCTREE,dither=Image.Dither.FLOYDSTEINBERG).save(out,optimize=True)
    return out
outs=[card(*c) for c in cards]
ims=[Image.open(o).convert('RGBA') for o in outs]
sheet=Image.new('RGBA',(W*4+60,H+40),(255,255,255,255))
for i,x in enumerate(ims): sheet.alpha_composite(x,(12+i*(W+12),20))
sheet.convert('RGB').save('preview.jpg',quality=85)
print(outs)
