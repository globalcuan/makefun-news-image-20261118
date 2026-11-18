from PIL import Image, ImageDraw, ImageFont
import os

W = H = 1024
PAPER = "#f6f1e5"
INK = "#14181f"
RED = "#b3202c"
NAVY = "#1d3557"
TEAL = "#14666b"
GREEN = "#2e6b34"
SAND = "#c9a86a"
ORANGE = "#e07b24"

SERIF_PATH = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SANS_BOLD_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS_PATH = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"

def font(path, size):
    if not os.path.exists(path):
        path = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf" if "Serif" in path else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    return ImageFont.truetype(path, size)

im = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(im)
serif = lambda n: font(SERIF_PATH, n)
bold = lambda n: font(SANS_BOLD_PATH, n)
sans = lambda n: font(SANS_PATH, n)

def wrapped(text, f, max_width):
    words = text.split()
    lines, line = [], ""
    for word in words:
        test = word if not line else line + " " + word
        if d.textlength(test, font=f) <= max_width:
            line = test
        else:
            if line:
                lines.append(line)
            line = word
    if line:
        lines.append(line)
    return lines

def draw_text_block(text, xy, f, fill, max_width, line_gap=3, max_lines=None):
    x, y = xy
    lines = wrapped(text, f, max_width)
    if max_lines:
        lines = lines[:max_lines]
    for line in lines:
        d.text((x, y), line, font=f, fill=fill)
        y += f.size + line_gap
    return y

def centered(text, y, f, fill):
    d.text(((W - d.textlength(text, font=f)) / 2, y), text, font=f, fill=fill)

def star(cx, cy, outer, inner, points=12, fill=ORANGE):
    coords = []
    import math
    for i in range(points * 2):
        a = -math.pi / 2 + i * math.pi / points
        r = outer if i % 2 == 0 else inner
        coords.append((cx + math.cos(a) * r, cy + math.sin(a) * r))
    d.polygon(coords, fill=fill)

def jet(cx, cy, scale=1):
    pts = [(cx-53*scale,cy),(cx-9*scale,cy-8*scale),(cx+2*scale,cy-35*scale),(cx+11*scale,cy-36*scale),(cx+10*scale,cy-8*scale),(cx+45*scale,cy-2*scale),(cx+52*scale,cy+4*scale),(cx+10*scale,cy+7*scale),(cx+12*scale,cy+27*scale),(cx+5*scale,cy+28*scale),(cx-7*scale,cy+8*scale)]
    d.polygon(pts, fill=PAPER)

# Masthead
d.rectangle((32, 18, 992, 23), fill=RED)
centered("THE WORLD IN ONE DAY", 30, serif(61), INK)
d.rectangle((32, 108, 992, 153), fill=RED)
centered("WEDNESDAY, 18 NOVEMBER 2026", 113, bold(29), PAPER)
d.line((32, 160, 992, 160), fill=INK, width=2)
d.line((32, 165, 992, 165), fill=INK, width=1)

# Lead story panel
px, py, ps = 42, 179, 300
d.rectangle((px, py, px+ps, py+ps), fill=NAVY)
d.rectangle((px+12, py+12, px+ps-12, py+ps-12), fill=TEAL)
# coastline / island viewed from above
d.polygon([(px+21,py+54),(px+78,py+34),(px+119,py+51),(px+150,py+39),(px+186,py+60),(px+231,py+52),(px+275,py+83),(px+266,py+124),(px+282,py+150),(px+250,py+180),(px+265,py+221),(px+220,py+261),(px+178,py+244),(px+148,py+263),(px+116,py+239),(px+79,py+247),(px+56,py+214),(px+25,py+187),(px+38,py+148),(px+23,py+119),(px+40,py+92)], fill=SAND)
d.ellipse((px+88,py+82,px+142,py+105), fill=GREEN)
d.ellipse((px+177,py+185,px+225,py+208), fill=GREEN)
star(px+172, py+130, 36, 17, fill=ORANGE)
d.ellipse((px+128, py+86, px+216, py+174), outline=RED, width=2)
jet(px+215, py+101, .88)
d.text((px+20,py+266), "QESHM ISLAND", font=bold(14), fill=PAPER)
d.text((px+190,py+245), "PERSIAN GULF", font=bold(9), fill=PAPER)

tx = 374
d.text((tx, 180), "US-IRAN WAR ESCALATES", font=bold(22), fill=RED)
draw_text_block("US BOMBS IRAN'S QESHM ISLAND", (tx, 207), serif(47), INK, 605, line_gap=-1, max_lines=3)
draw_text_block("Jets strike a Revolutionary Guard missile site; Iran answers with drones on US bases in Bahrain and Kuwait, its third Bahrain attack in a week", (tx, 312), sans(22), INK, 605, line_gap=3, max_lines=4)
d.line((32, 489, 992, 489), fill=INK, width=2)

# Four compact illustrated stories
def bridge_icon(x,y):
    d.rectangle((x,y,x+92,y+92), fill=NAVY)
    d.line((x+9,y+66,x+83,y+66), fill=PAPER, width=4)
    for xx in (x+25,x+68):
        d.rectangle((xx-4,y+33,xx+4,y+67), fill=PAPER)
        d.line((x+10,y+65,xx,y+35), fill=PAPER, width=2)
        d.line((xx,y+35,x+82,y+65), fill=PAPER, width=2)
    star(x+72,y+20,12,6,points=8)

def virus_icon(x,y):
    d.rectangle((x,y,x+92,y+92), fill=RED)
    cx,cy=x+46,y+46
    import math
    for i in range(12):
        a=i*math.pi/6
        x1,y1=cx+24*math.cos(a),cy+24*math.sin(a)
        x2,y2=cx+34*math.cos(a),cy+34*math.sin(a)
        d.line((x1,y1,x2,y2),fill=PAPER,width=4)
        d.ellipse((x2-3,y2-3,x2+3,y2+3),fill=PAPER)
    d.ellipse((cx-24,cy-24,cx+24,cy+24),fill=PAPER)
    for dx,dy in [(-9,-7),(7,-12),(11,6),(-6,11)]:
        d.ellipse((cx+dx-3,cy+dy-3,cx+dx+3,cy+dy+3),fill=RED)

def flags_icon(x,y):
    d.rectangle((x,y,x+92,y+92), fill="#6f1c24")
    fx,fy=x+7,y+18
    d.rectangle((fx,fy,fx+23,fy+48),fill=RED)
    d.ellipse((fx+5,fy+5,fx+12,fy+12),fill="#f4d35e")
    fx2=x+35
    for i in range(6):
        yy=fy+i*8
        d.rectangle((fx2,yy,fx2+23,yy+4),fill=PAPER if i%2==0 else RED)
    d.rectangle((fx2,fy,fx2+11,fy+22),fill=NAVY)
    fx3=x+63
    d.rectangle((fx3,fy,fx3+22,fy+16),fill=PAPER)
    d.rectangle((fx3,fy+16,fx3+22,fy+32),fill="#3974a8")
    d.rectangle((fx3,fy+32,fx3+22,fy+48),fill=RED)

def capitol_icon(x,y):
    d.rectangle((x,y,x+92,y+92), fill=NAVY)
    d.rectangle((x+14,y+59,x+78,y+73),fill=PAPER)
    d.rectangle((x+19,y+73,x+73,y+79),fill=PAPER)
    for xx in (24,36,48,60,72):
        d.rectangle((x+xx-2,y+39,x+xx+2,y+59),fill=PAPER)
    d.pieslice((x+25,y+18,x+67,y+58),180,360,fill=PAPER)
    d.rectangle((x+25,y+38,x+67,y+43),fill=PAPER)
    d.rectangle((x+44,y+12,x+48,y+20),fill=PAPER)

def story(x,y,icon,kicker,headline,sub):
    icon(x,y+6)
    xx=x+108
    d.text((xx,y),kicker,font=bold(18),fill=RED)
    end=draw_text_block(headline,(xx,y+24),serif(27),INK,356,line_gap=-1,max_lines=2)
    draw_text_block(sub,(xx,end+1),sans(14),INK,356,line_gap=1,max_lines=3)

story(42, 501, bridge_icon, "UKRAINE WAR", "KERCH BRIDGE HIT AGAIN", "Ukraine strikes the Crimea bridge for a second day and launches its biggest drone attack of the war; Washington scolds Kyiv over deep strikes")
story(530, 501, virus_icon, "HEALTH", "EBOLA DOUBLES IN DR CONGO", "The UN counts over 11,000 cases and 5,400 deaths in three months; three in four infected children under five die")
story(42, 683, flags_icon, "APEC SUMMIT", "XI HOSTS PUTIN IN SHENZHEN", "Xi urges lower trade barriers and attacks protectionism; Trump arrives Thursday for the first trilateral summit")
story(530, 683, capitol_icon, "US POLITICS", "DEMOCRATS TAKE 56 SENATE SEATS", "Mary Peltola's Alaska victory is confirmed two weeks after the midterms, capping a Democratic rout of the Senate")
d.line((32, 867, 992, 867), fill=INK, width=2)

# Israel strip
ix, iy = 42, 878
d.rectangle((ix,iy,ix+58,iy+58),fill=PAPER,outline=NAVY,width=2)
d.polygon([(ix+8,iy+11),(ix+50,iy+11),(ix+29,iy+48)],outline=NAVY,fill=None)
d.polygon([(ix+8,iy+45),(ix+50,iy+45),(ix+29,iy+8)],outline=NAVY,fill=None)
d.text((114, 876), "HERZOG PICKS EISENKOT TO FORM ISRAEL'S GOVERNMENT", font=serif(24), fill=INK)
d.text((114, 912), "The president bypasses Netanyahu as the new Knesset is sworn in amid coalition deadlock", font=sans(19), fill=INK)
d.line((32, 940, 992, 940), fill=INK, width=1)

# Ticker and footer
tick_text = "ALSO ON WEDNESDAY: Category 5 Cyclone Xavier hits the Cook Islands • World Court to rule on Myanmar genocide case • Cyber-attack freezes supermarket freezers in 7 European countries • GTA VI launches at midnight"
d.rectangle((32, 946, 992, 990), fill=INK)
tick_font = bold(13)
tick_prefix = "ALSO ON WEDNESDAY:"
d.text((45, 949), tick_prefix, font=tick_font, fill=ORANGE)
tick_rest = tick_text[len(tick_prefix):].lstrip()
tick_rest_x = 45 + d.textlength(tick_prefix + " ", font=tick_font)
draw_text_block(tick_rest, (tick_rest_x, 949), tick_font, PAPER, 934 - (tick_rest_x - 45), line_gap=1, max_lines=2)
footer = "The world's news of Wednesday 18 November 2026, summed up in one image"
# Footer sits in the final safe margin, centered and fully visible.
d.text(((W-d.textlength(footer,font=sans(14)))/2,993), footer, font=sans(14), fill=INK)

im.save("entry.png", format="PNG", optimize=True)
