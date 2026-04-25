"""
Extract distribution pipes (diameter >= 25mm) from EPANET .inp file
and convert UTM Zone 35S coordinates to WGS84 lat/lng.
Outputs JavaScript-ready pipe data for the Leaflet map.
"""
import re, json, math

INP = '2020-Rwamagana-Karenge_Rev1.inp'

def utm35s_to_wgs84(easting, northing):
    a=6378137.0; f=1/298.257223563; b=a*(1-f); e_sq=1-(b/a)**2; e_prime_sq=(a/b)**2-1
    k0=0.9996; e1=(1-math.sqrt(1-e_sq))/(1+math.sqrt(1-e_sq))
    x=easting-500000.0; y=northing-10000000.0  # Zone 35S, southern hemisphere
    lon_origin_rad=math.radians(27)  # Zone 35 central meridian
    M=y/k0; mu=M/(a*(1-e_sq/4-3*e_sq**2/64-5*e_sq**3/256))
    phi1=mu+(3*e1/2-27*e1**3/32)*math.sin(2*mu)+(21*e1**2/16-55*e1**4/32)*math.sin(4*mu)+(151*e1**3/96)*math.sin(6*mu)
    N1=a/math.sqrt(1-e_sq*math.sin(phi1)**2); T1=math.tan(phi1)**2
    C1=e_prime_sq*math.cos(phi1)**2; R1=a*(1-e_sq)/(1-e_sq*math.sin(phi1)**2)**1.5
    D=x/(N1*k0)
    lat=phi1-(N1*math.tan(phi1)/R1)*(D**2/2-(5+3*T1+10*C1-4*C1**2-9*e_prime_sq)*D**4/24+(61+90*T1+298*C1+45*T1**2-252*e_prime_sq-3*C1**2)*D**6/720)
    lon_rad=(D-(1+2*T1+C1)*D**3/6+(5-2*C1+28*T1-3*C1**2+8*e_prime_sq+24*T1**2)*D**5/120)/math.cos(phi1)
    return round(math.degrees(lat),6), round(math.degrees(lon_origin_rad+lon_rad),6)

with open(INP) as f:
    raw = f.read()

def get_section(name):
    m = re.search(r'\['+name+r'\](.*?)(?=\n\[)', raw, re.DOTALL)
    return m.group(1) if m else ''

# ── COORDINATES (all nodes) ──────────────────────────────────────────
coords = {}
for line in get_section('COORDINATES').splitlines():
    line = re.sub(r';.*','', line).strip()
    parts = line.split()
    if len(parts) >= 3:
        try:
            coords[parts[0]] = utm35s_to_wgs84(float(parts[1]), float(parts[2]))
        except:
            pass

print(f'Loaded {len(coords)} node coordinates')

# ── VERTICES (intermediate points for bent pipes) ────────────────────
vertices = {}
for line in get_section('VERTICES').splitlines():
    line = re.sub(r';.*','', line).strip()
    parts = line.split()
    if len(parts) >= 3:
        try:
            pid = parts[0]
            pt = utm35s_to_wgs84(float(parts[1]), float(parts[2]))
            vertices.setdefault(pid, []).append(pt)
        except:
            pass

print(f'Loaded vertices for {len(vertices)} pipes')

# ── PIPES (filter by diameter) ──────────────────────────────────────
pipes_by_diam = {}  # diameter -> list of polylines [[lat,lng],...]
missing = 0

for line in get_section('PIPES').splitlines():
    line = re.sub(r';.*','', line).strip()
    parts = line.split()
    if len(parts) < 5:
        continue
    try:
        pid, n1, n2, length, diam = parts[0], parts[1], parts[2], float(parts[3]), float(parts[4])
    except:
        continue
    
    if diam < 25:
        continue  # Keep modeled distribution/service pipes, skip very tiny links
    
    if n1 not in coords or n2 not in coords:
        missing += 1
        continue
    
    # Build polyline: start → vertices → end
    pts = [coords[n1]]
    pts.extend(vertices.get(pid, []))
    pts.append(coords[n2])
    
    d_key = int(diam)
    pipes_by_diam.setdefault(d_key, []).append(pts)

print(f'Missing coords for {missing} pipes')
for d, pl in sorted(pipes_by_diam.items(), reverse=True):
    print(f'  Ø {d}mm: {len(pl)} pipes')

# ── TANK COORDINATES (for updating dashboard) ──────────────────────
tanks = ['GAHKIBRE1','GAHKIBRE2','GAHKIBRE3','KARBICRE1','KARBICRE3','KARBICRE6',
         'KARKANRE','KARKANRE2','KARNYARE1','KARNYARE2','KARNYARE5','KARRUGRE1',
         'MUYBUJRE4','MUYMURRE2','MUYMURRE6','NYABIHRE1','NYABIHRE2','NYABIHRE4',
         'NYABIHRE7','NYAGATRE1','NYAGATRE4','NYAGATRE5','NYARWIRE1','NYARWIRE2',
         'NZIAKARE2','NZIAKARE5','NZIKIGRE1','NZIKIGRE2','NZIKIGRE4','NZIMURRE2',
         'NZIMURRE6','NZIRUGRE1']
print('\n--- TANK COORDINATES (UTM Zone 35S -> WGS84) ---')
for t in tanks:
    if t in coords:
        lat, lng = coords[t]
        print(f"  {{ id:'{t}', lat:{lat}, lng:{lng} }},")
    else:
        print(f"  {t}: NOT FOUND")

wtp = coords.get('KARRUGTP1')
if wtp:
    print(f'\n  WTP (KARRUGTP1): lat={wtp[0]}, lng={wtp[1]}')

# ── Centroid ─────────────────────────────────────────────────────────
all_lats = [v[0] for v in coords.values()]
all_lngs = [v[1] for v in coords.values()]
print(f'\nNetwork extent: lat [{min(all_lats):.4f}, {max(all_lats):.4f}], lng [{min(all_lngs):.4f}, {max(all_lngs):.4f}]')
print(f'Centroid: lat={(min(all_lats)+max(all_lats))/2:.4f}, lng={(min(all_lngs)+max(all_lngs))/2:.4f}')

# ── Write JS output ───────────────────────────────────────────────────
lines = ['const PIPE_LAYERS = {']
color_map = {600:'#c0392b', 200:'#e74c3c', 110:'#e67e22', 90:'#f39c12', 63:'#27ae60', 50:'#2980b9'}

for d in sorted(pipes_by_diam.keys(), reverse=True):
    pls = pipes_by_diam[d]
    color = color_map.get(d, '#7f8c8d')
    weight = 5 if d>=200 else 3.5 if d>=100 else 2.5 if d>=50 else 1.5
    lines.append(f'  "d{d}": {{ diam:{d}, color:"{color}", weight:{weight}, pipes:[')
    for pl in pls:
        coord_str = ','.join(f'[{p[0]},{p[1]}]' for p in pl)
        lines.append(f'    [{coord_str}],')
    lines.append('  ]},')
lines.append('};')

with open('pipe_data.js', 'w') as f:
    f.write('\n'.join(lines))

print(f'\nWrote pipe_data.js ({sum(len(v) for v in pipes_by_diam.values())} pipes >=25mm)')
