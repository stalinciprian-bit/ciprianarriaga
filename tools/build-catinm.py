#!/usr/bin/env python3
"""Genera catinm/<letrero>/index.html (presentación de cada inmueble) desde catinm/inmuebles.json.
Uso: python3 tools/build-catinm.py   (desde la raíz del repositorio)
URL pública: https://www.ciprianarriaga.com/catinm/<letrero>"""
import json, html, re, pathlib
root = pathlib.Path(__file__).resolve().parent.parent
cat = root / 'catinm'
data = json.loads((cat / 'inmuebles.json').read_text(encoding='utf8'))
css = re.search(r'<style>(.*?)</style>', (cat / 'index.html').read_text(encoding='utf8'), re.S).group(1)
extra = '''
.crumb{padding-block:22px 0;font-size:14px;color:var(--muted)}
.crumb a{color:var(--plum)}
.top{display:grid;grid-template-columns:minmax(0,1.5fr) minmax(0,1fr);gap:36px;padding-block:20px 48px;align-items:start}
@media(max-width:820px){.top{grid-template-columns:1fr;gap:24px}}
.gal .main{aspect-ratio:4/3;background:var(--navy);overflow:hidden;position:relative}
.cerr{background:#EFE9E6;border-left:3px solid var(--rose);padding:14px 16px;margin:0 0 18px;font-size:15px}
.mantl{margin:14px 0 0;font-size:15px}
.gal .main img{width:100%;height:100%;object-fit:cover;display:block}
.gal .main .none{position:absolute;inset:0;display:grid;place-items:center;background:var(--logo-bg)}
.gal .main .none img{width:40%;height:auto}
.thumbs{display:flex;gap:8px;margin-top:8px;overflow-x:auto;padding-bottom:4px}
.thumbs button{border:2px solid transparent;padding:0;background:none;cursor:pointer;flex:0 0 84px}
.thumbs button[aria-current="true"]{border-color:var(--brass)}
.thumbs img{width:84px;height:62px;object-fit:cover;display:block}
.side h1{font-size:clamp(28px,3.6vw,40px);margin:10px 0 6px}
.side .zona{font-size:17px}
.side .precio{font-size:32px;margin:16px 0}
.side .specs{margin-block:6px 18px;font-size:15px}
.side .btn{display:block;text-align:center;margin-top:10px;padding:14px 18px}
.side .btn.alt{background:none;color:var(--navy);border:1px solid var(--navy)}
.side .btn.alt:hover{background:var(--navy);color:var(--paper)}
.let{display:inline-block;margin-top:18px;font-size:13px;color:var(--muted);letter-spacing:.08em;border-left:2px solid var(--rose);padding-left:10px}
.prep{background:var(--brass-soft);border-left:3px solid var(--brass);padding:12px 16px;margin:0 0 18px;font-size:15px}
.det{padding-bottom:64px;max-width:760px}
.det h2{font-size:24px;margin:28px 0 10px}
.det ul{margin:0;padding-left:20px}
.det li{margin:4px 0}
.det p{color:var(--ink)}
.pdfl{display:inline-block;margin-top:8px}
'''
def esc(x): return html.escape(str(x if x is not None else ''), quote=True)
def money(n, m): return ('USD ' if m == 'USD' else 'RD$ ') + f'{int(n):,}'
tpl = '''<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{titulo} · Letrero N° {let} · Ciprián Arriaga &amp; Asocs.</title>
<meta name="description" content="{titulo}, {zona}. Presentación del inmueble del letrero N° {let}. Ciprián Arriaga &amp; Asocs., Abogados Notarios.">
<meta property="og:title" content="{titulo}">
<meta property="og:description" content="{zona} · Letrero N° {let}">
<meta property="og:image" content="https://www.ciprianarriaga.com/{ogimg}">
<link rel="icon" href="../../logo-ca.webp">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=EB+Garamond:wght@400;600;700&family=Tinos:ital,wght@0,400;0,700;1,400;1,700&display=swap">
<style>{css}{extra}</style>
</head>
<body>
<header>
  <div class="wrap">
    <a class="brand" href="../../"><b>Ciprián Arriaga &amp; Asocs.</b><span>Abogados · Notarios</span></a>
    <nav aria-label="Secciones">
      <a href="../../#areas">Práctica</a>
      <a href="../../#equipo">Equipo</a>
      <a href="../" aria-current="page">Catálogo Inmb.</a>
      <a href="../../#contacto">Contacto</a>
    </nav>
  </div>
</header>
<main class="wrap">
  <p class="crumb"><a href="../">Catálogo inmobiliario</a> › Letrero N° {let}</p>
  <div class="top">
    <div class="gal">
      <div class="main" id="main">{cinta}{main}</div>
      {thumbs}
    </div>
    <div class="side">
      {prep}{cerr}
      {dest}<span class="eyebrow">{tipo}{oper}</span>
      <h1>{titulo}</h1>
      <div class="zona">{zona}</div>
      <div class="precio">{precio}</div>
      {specs}{mant}
      {btns}
      {pdf}
      <span class="let">Letrero N° {let} · {codigo}</span>
    </div>
  </div>
  <div class="det">
    {desc}{feat}{legal}{mapa}
    <p class="note" style="border:0;padding:20px 0 0">Precios y disponibilidad sujetos a confirmación. Consulte con nuestro despacho antes de cualquier oferta o reserva.</p>
  </div>
</main>
<footer>
  <a class="foot-logo" href="../../" aria-label="Ir al inicio"><img src="../../logo-ca.webp" alt="Ciprián Arriaga &amp; Asoc." width="1000" height="442" loading="lazy"></a>
  <div class="wrap"><span>© 2026 Ciprián Arriaga &amp; Asocs. · Abogados Notarios</span><span>ciprianarriaga.com · <a href="mailto:info@ciprianarriaga.com">info@ciprianarriaga.com</a></span></div>
</footer>
<script>
document.querySelectorAll('.thumbs button').forEach(function(b){{b.addEventListener('click',function(){{
  document.querySelector('#main img').src=b.dataset.src;
  document.querySelectorAll('.thumbs button').forEach(function(x){{x.setAttribute('aria-current',x===b)}});
}})}});
</script>
</body>
</html>
'''
for i in data:
    let = str(i['letrero'])
    fotos = [f if f.startswith('http') else '../' + f for f in i.get('fotos', [])]
    if fotos:
        main = f'<img src="{esc(fotos[0])}" alt="{esc(i["titulo"])}">'
        thumbs = ('<div class="thumbs">' + ''.join(
            f'<button type="button" data-src="{esc(f)}" aria-current="{"true" if n == 0 else "false"}"><img src="{esc(f)}" alt="Foto {n+1}" loading="lazy"></button>'
            for n, f in enumerate(fotos)) + '</div>') if len(fotos) > 1 else ''
        ogimg = 'catinm/' + i['fotos'][0]
    else:
        main = '<div class="none"><img src="../../logo-ca.webp" alt=""></div>'; thumbs = ''; ogimg = 'logo-completo.webp'
    sp = []
    if i.get('m2'): sp.append(f'<span><b>{esc(i["m2"])}</b> m²</span>')
    if i.get('habitaciones'): sp.append(f'<span><b>{esc(i["habitaciones"])}</b> hab.</span>')
    if i.get('banos'): sp.append(f'<span><b>{esc(i["banos"])}</b> baños</span>')
    if i.get('parqueos'): sp.append(f'<span><b>{esc(i["parqueos"])}</b> parqueos</span>')
    precio = (money(i['precio'], i.get('moneda')) + (' <small>/ mes</small>' if i.get('operacion') == 'Alquiler' else '')) if i.get('precio') else '<small>Precio a consultar</small>'
    wa = 'https://wa.me/18098155997?text=' + __import__('urllib.parse').parse.quote(f'Hola, me interesa el inmueble del letrero N° {let} ({i["titulo"]}) del catálogo de Ciprián Arriaga & Asocs.')
    feat_ = ('<h2>Características</h2><ul>' + ''.join(f'<li>{esc(c)}</li>' for c in i['caracteristicas']) + '</ul>') if i.get('caracteristicas') else ''
    legal = f'<h2>Situación legal</h2><p>{esc(i["legal"])}</p>' if i.get('legal') else ''
    mapa = f'<p><a href="{esc(i["mapa"])}" target="_blank" rel="noopener">Ver ubicación en el mapa</a></p>' if i.get('mapa') else ''
    pdf = f'<a class="pdfl" href="{esc(i["pdf"])}">Descargar presentación (PDF)</a>' if i.get('pdf') else ''
    oper = i.get('operacion')
    cinta = (f'<span class="cinta{" alq" if oper=="Alquiler" else (" vya" if oper not in ("Venta","Alquiler") else "")}">' +
             esc('En venta' if oper == 'Venta' else 'En alquiler' if oper == 'Alquiler' else oper) + '</span>') if oper and not i.get('cerrado') else ''
    mant = f'<p class="mantl"><b>Mantenimiento:</b> {esc(i["mantenimiento"])}</p>' if i.get('mantenimiento') else ''
    if i.get('mantenimiento'):
        i['caracteristicas'] = list(i.get('caracteristicas', [])) + ['Mantenimiento: ' + i['mantenimiento']]
    cerr = '<p class="cerr"><b>Este inmueble ya no está disponible.</b> Vea otras opciones en el <a href="../">catálogo</a>.</p>' if i.get('cerrado') else ''
    btns = '' if i.get('cerrado') else (f'<a class="btn" href="{wa}" target="_blank" rel="noopener">Consultar por WhatsApp</a>\n      <a class="btn alt" href="tel:+18095333060">Llamar al 809-533-3060</a>')
    dest = f'<span class="dest" style="margin-bottom:14px">★ {esc(i["destacado"])} ★</span><br>' if i.get('destacado') else ''
    page = tpl.format(dest=dest, cinta=cinta, mant=mant, cerr=cerr, btns=btns, 
        css=css, extra=extra, titulo=esc(i['titulo']), zona=esc(i['zona']), let=esc(let), codigo=esc(i.get('codigo', '')), ogimg=ogimg,
        main=main, thumbs=thumbs, tipo=esc(i['tipo']), oper=(' · ' + esc(i['operacion'])) if i.get('operacion') else '',
        precio=precio, specs=('<div class="specs">' + ''.join(sp) + '</div>') if sp else '', wa=wa, pdf=pdf,
        prep='<p class="prep">Presentación en preparación. Escríbanos y le damos todos los detalles.</p>' if i.get('preparacion') else '',
        desc=(f'<h2>Descripción</h2><p>{esc(i["descripcion"])}</p>' if i.get('descripcion') and not i.get('preparacion') else ''),
        feat=('<h2>Características</h2><ul>' + ''.join(f'<li>{esc(c)}</li>' for c in i['caracteristicas']) + '</ul>') if i.get('caracteristicas') else '', legal=legal, mapa=mapa)
    out = cat / let; out.mkdir(exist_ok=True)
    (out / 'index.html').write_text(page, encoding='utf8')
    print('ok', f'catinm/{let}/')
