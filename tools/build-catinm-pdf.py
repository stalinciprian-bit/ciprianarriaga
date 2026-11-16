#!/usr/bin/env python3
"""Genera el PDF del catálogo para recepción: python3 -I tools/build-catinm-pdf.py [salida.pdf]"""
import json, sys, base64, datetime, pathlib, html
from playwright.sync_api import sync_playwright
R = pathlib.Path(__file__).resolve().parent.parent
out = sys.argv[1] if len(sys.argv) > 1 else str(R/'Catalogo Inmuebles para Recepcion.pdf')
d = json.load(open(R/'catinm/inmuebles.json'))
e = html.escape
def money(i):
    if not i.get('precio'): return 'Consultar'
    return ('USD$' if i.get('moneda')=='USD' else 'RD$') + f"{float(i['precio']):,.2f}" + (' al mes' if i.get('operacion')=='Alquiler' else '')
def img(p):
    f = R/'catinm'/p
    return 'data:image/jpeg;base64,'+base64.b64encode(f.read_bytes()).decode() if f.exists() else ''
act = [i for i in d if not i.get('oculto') and not i.get('cerrado')]
prep = [i for i in d if i.get('oculto') and i.get('preparacion')]
logo = 'data:image/webp;base64,'+base64.b64encode((R/'logo-ca.webp').read_bytes()).decode()
hoy = datetime.date.today().strftime('%d/%m/%Y')
rows = ''.join(f"<tr><td><b>{e(i['letrero'])}</b></td><td>{e(i['tipo'])}</td><td>{e(i.get('operacion',''))}</td><td>{e(money(i))}</td><td>{e(i['zona'])}</td><td>{i.get('m2','')} m²</td><td>{i.get('habitaciones','—')}</td></tr>" for i in act)
pg = ''
for i in act:
    car = ''.join(f'<li>{e(c)}</li>' for c in i.get('caracteristicas',[]))
    mant = f"<p><b>Mantenimiento:</b> {e(i['mantenimiento'][0].upper()+i['mantenimiento'][1:])}</p>" if i.get('mantenimiento') else ''
    dest = f"<span class='dest'>{e(i['destacado']).upper()}</span>" if i.get('destacado') else ''
    ph = img(i['fotos'][0]) if i.get('fotos') else ''
    url = f"ciprianarriaga.com/catinm/{i['letrero']}/"
    pg += f"""<section class="pg"><div class="h"><h2>Inmueble No. {e(i['letrero'])} · {e(i['codigo'])} {dest}</h2><div class="op">{e(i.get('operacion',''))}</div></div>
<h3>{e(i['titulo'])}</h3><p class="z">{e(i['zona'])}</p>
<div class="g"><div><div class="pr">{e(money(i))}</div>{mant}
<p><b>Área:</b> {i.get('m2','')} m² · {('<b>Hab.:</b> '+str(i['habitaciones'])+' · ') if i.get('habitaciones') else ''} <b>Baños:</b> {i.get('banos','')} · <b>Parqueos:</b> {i.get('parqueos','')}</p>
<p>{e(i.get('descripcion',''))}</p><ul>{car}</ul>
<p class="u">Ficha con fotos: {url}</p></div>{f'<img src="{ph}">' if ph else ''}</div>
<div class="say"><b>Al contestar:</b> «Ciprián Arriaga & Asociados, buenas. Sí, el Inmueble No. {e(i['letrero'])} está disponible en {e(i.get('operacion','venta').lower())}.» <b>Todas las llamadas por inmuebles se pasan al Lic. Stalin Ciprián</b> (que pregunten por él). Si no está: tomar nombre y teléfono para que él devuelva la llamada.</div></section>"""
prp = ''
if prep:
    prp = f"<p class='n'><b>Inmuebles {', '.join(i['letrero'] for i in prep)}:</b> reservados, aún sin información. Si llaman por uno de ellos: tomar nombre y teléfono y avisar al Lic. Stalin.</p>"
doc = f"""<html><meta charset=utf-8><style>
@page{{size:Letter;margin:14mm}}body{{font:11pt Arial,sans-serif;color:#1b2a41}}
.top{{display:flex;align-items:center;gap:12px;border-bottom:3px solid #1b2a41;padding-bottom:8px}}.top img{{height:50px}}
.top h1{{font-size:16pt;margin:0}}.top small{{color:#666}}
table{{width:100%;border-collapse:collapse;margin:14px 0;font-size:10pt}}th{{background:#1b2a41;color:#fff;text-align:left}}
td,th{{padding:6px;border:1px solid #ccd}}.pg{{page-break-before:always}}.h{{display:flex;justify-content:space-between;align-items:center}}
h2{{margin:0;font-size:15pt}}h3{{margin:6px 0 0}}.z{{color:#555;margin:2px 0 10px}}.op{{background:#1b2a41;color:#fff;padding:4px 12px;border-radius:4px;font-weight:700}}
.dest{{background:#F2C230;color:#1b2a41;padding:2px 8px;border-radius:3px;font-size:9pt}}.g{{display:grid;grid-template-columns:1fr 200px;gap:14px}}
.g img{{width:200px;border-radius:6px}}.pr{{font-size:20pt;font-weight:700;margin-bottom:6px}}ul{{padding-left:18px;font-size:10pt}}
.say{{background:#f3f5f9;border-left:4px solid #F2C230;padding:10px;margin-top:12px;font-size:10.5pt}}.u,.n{{font-size:9.5pt;color:#555}}
</style>
<div class="top"><img src="{logo}"><div><h1>Catálogo de inmuebles · Guía para recepción</h1><small>Actualizado: {hoy} · Tel. oficina 809-533-3060</small></div></div>
<h3>Resumen ({len(act)} disponible{'s' if len(act)!=1 else ''})</h3>
<table><tr><th>N°</th><th>Tipo</th><th>Operación</th><th>Precio</th><th>Zona</th><th>Área</th><th>Hab.</th></tr>{rows}</table>{prp}{pg}</html>"""
with sync_playwright() as p:
    b = p.chromium.launch(); pgx = b.new_page(); pgx.set_content(doc); pgx.pdf(path=out, format='Letter', print_background=True, prefer_css_page_size=True); b.close()
print(out)
