from PIL import Image, ImageDraw, ImageFont
from scenes import SC, HEAD, CREDIT
F=lambda s: ImageFont.truetype('/tmp/ph.ttf', s)
src=Image.open('source.png').convert('RGB'); K=2500/1932
def wrap(d,t,f,w):
    out=[];cur=''
    for wd in t.split():
        if d.textlength((cur+' '+wd).strip(),font=f)<=w: cur=(cur+' '+wd).strip()
        else: out.append(cur);cur=wd
    return out+[cur]
def frame(s):
    W,H=1080,1920; im=Image.new('RGB',(W,H),'white'); d=ImageDraw.Draw(im)
    d.rectangle([440,0,640,40],fill=(226,214,184))
    d.text((W//2,345),HEAD,font=F(34),fill=(120,90,60),anchor='mm')
    d.text((W//2,430),s['head'],font=F(60),fill=(80,55,35),anchor='mm')
    if s['cite']: d.text((W//2,490),s['cite'],font=F(30),fill=(120,90,60),anchor='mm')
    x,y,w,h=s['cam']; card=src.crop((int(x*K),int(y*K),int((x+w)*K),int((y+h)*K))).resize((1000,int(1000*h/w)))
    ch=card.size[1]; top=610
    # nét doodle (xem trước vị trí)
    cd=ImageDraw.Draw(card); sx=1000/w
    P=lambda a,b:((a-x)*sx,(b-y)*sx)
    for k,v in s['dd']:
        if k=='line':
            x1,y1=P(v[0],v[1]);x2,y2=P(v[2],v[3])
            n=int(abs(y2-y1)//22)
            for i in range(0,n,2): cd.line([x1,y1+i*22,x1,y1+i*22+12],fill='white',width=6)
            cd.line([x1+2,y1,x1+2,y2],fill=(40,40,40),width=1)
        elif k=='ellipse':
            a=P(v[0],v[1]);b=P(v[2],v[3]); cd.ellipse([a,b],outline='white',width=6)
        elif k=='poly':
            cd.line([P(*p) for p in v]+[P(*v[0])],fill='white',width=6)
        elif k in('arrow','arrow2'):
            a=P(v[0],v[1]);b=P(v[2],v[3]); cd.line([a,b],fill='white',width=6); cd.ellipse([b[0]-9,b[1]-9,b[0]+9,b[1]+9],fill='white')
            if k=='arrow2': cd.ellipse([a[0]-9,a[1]-9,a[0]+9,a[1]+9],fill='white')
        elif k=='text':
            p=P(v[0],v[1]); cd.text((p[0]+2,p[1]+2),v[2],font=F(34),fill=(60,40,30)); cd.text(p,v[2],font=F(34),fill='white')
    im.paste(card,(40,top))
    d.text((W//2,top+ch+30),CREDIT,font=F(26),fill=(150,130,110),anchor='mm')
    ys=top+ch+80
    for ln in wrap(d,s['loi'],F(40),960)[:5]:
        d.text((W//2,ys),ln,font=F(40),fill=(70,50,35),anchor='mm'); ys+=52
    return im
fr=[frame(s) for s in SC]
import os; os.makedirs('frames',exist_ok=True)
for i,f in enumerate(fr,1): f.save(f'frames/c{i}.png')
tw,th=360,640
sheet=Image.new('RGB',(tw*3+40,th*2+30),(235,235,235))
for i,f in enumerate(fr):
    sheet.paste(f.resize((tw,th)),(10+(i%3)*(tw+10),10+(i//3)*(th+10)))
sheet.save('storyboard.png')
# kiểm tra vùng an toàn: chữ y 330..1500
for i,f in enumerate(fr,1): print(i,'ok')
