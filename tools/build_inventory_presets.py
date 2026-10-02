#!/usr/bin/env python3
"""MMM Sound Library: baut inventory.csv aus dem, was wirklich unter sound_library/ liegt (Stand 02.10.2026, Struktur vom Owner aufgeräumt).

usage: python3 tools/build_inventory_presets.py   (im Repo-Root)
- Karte 00 (Japan Operator-Set, Bestand des Owners) liegt nicht im Repo, die Zeilen bleiben aus der bisherigen CSV.
- Karte 01 Drums + Tsuzumi, Karte 02 Saiten (pausiert) und Karte 03 Gamelan werden aus den Dateien unter sound_library/ erzeugt.
- Gleiche Datei in mehreren Ordnern: eine Zeile, Spalte Pfad enthält alle Fundorte, Notiz 'doppelt abgelegt'.
- Gamelan-Zeilen übernehmen Gruppe/Notiz aus der bisherigen CSV (gmln.4 v2.0), nur die Spalte Pfad kommt neu hinzu.
Status 'berechnet' = nichts in Live/am Gerät gehört; 'pausiert' = Koto/Shamisen, Thema ruht.
"""
import csv, os, re
ROOT = 'sound_library'; OUT = 'sound_library/inventory.csv'
HEAD = ['Karte', 'Gruppe', 'Instrument', 'Kürzel', 'Variante', 'Gerät', 'Datei', 'Quelle', 'Status', 'Notiz', 'Pfad']
old = list(csv.reader(open(OUT, encoding='utf8')))
meta = {r[6]: r for r in old[1:] if r and r[0].startswith('03 ')}
rows = [HEAD] + [r + [''] * (11 - len(r)) for r in old[1:] if r and r[0].startswith('00 ')]

found = {}                                           # Dateiname → [Pfade]
for d, _, fs in os.walk(ROOT):
    for f in fs:
        if f.startswith('.') or f == 'inventory.csv': continue
        found.setdefault(f, []).append(os.path.relpath(os.path.join(d, f), ROOT))
STRING = re.compile(r'KOTO|SHAMI|SHM_|koto_|shami_', re.I)

def classify(f, paths):
    p0 = paths[0]; ext = os.path.splitext(f)[1].lower(); name = os.path.splitext(f)[0]
    if 'MMM-Gamelan' in p0:
        m = meta.get(f)
        if m: return m[:10]
        return None
    saiten = bool(STRING.search(f)) or 'strings' in f or 'Sounds-02' in f
    karte = '02 Saiten (pausiert)' if saiten else '01 Drums + Tsuzumi'
    quelle = 'strings.js (Karte 02)' if saiten else 'cards.js (Karte 01)'
    status = 'pausiert' if saiten else 'berechnet'
    g = i = kz = v = dev = n = ''
    if 'Ableton' in p0:
        dev = 'Operator'
        if ext == '.als': g, i, dev, n = 'Set', 'Live Set mit allen Operator-Spuren', 'Ableton Live', 'Live 12.3.2, aus Played_12.als'
        elif f.startswith('MMM_DS_'):
            dev = 'Drum Synth'; part = name.split('_')[2]; v = name.split('_')[3] if len(name.split('_')) > 3 else ''
            g = {'Snare': 'Snare', 'HH': 'Hi-Hat', 'Clap': 'Clap'}[part]; i = g
            if v == 'CymbalLike': g, i, n = 'Becken', 'Cymbal (DS-HH-Näherung)', 'DS HH ist eine Hi-Hat, Näherung'
            else: n = 'Parameter-Mapping DS unbekannt, Startwerte'
        elif 'Cymbal_Plate' in f: g, i, v, dev = 'Becken', 'Cymbal (Platte)', 'Plate', 'Collision'
        elif f.startswith('MMM_KCK_'): g, i, kz, v = 'Kick', 'Kick (Glide + Rumble)', 'KCK', name.split('_')[2]; n = 'Rumble: eigene Spur unter dem Kick' if v == 'Rumble' else ''
        elif f.startswith('MMM_KOT_'):
            g, i, kz = 'Trommeln', 'Ko-Tsuzumi', 'KOT'; parts = name.split('_'); v = parts[2]
            if name.endswith('_Collision'): dev, n = 'Collision', 'String-Resonator'
        elif f.startswith('MMM_OTS_'):
            g, i, kz = 'Trommeln', 'Ō-Tsuzumi', 'OTS'; parts = name.split('_'); v = parts[2]
            if name.endswith('_Collision'): dev, n = 'Collision', 'Membrane-Resonator'
        elif f.startswith('MMM_KOTO_'): g, i, kz, v, dev = 'Saite', 'Koto', 'KOTO', name.split('_', 2)[2], 'Tension'
        elif f.startswith('MMM_SHAMISEN_'): g, i, kz, v, dev = 'Saite', 'Shamisen', 'SHM', name.split('_', 2)[2], 'Tension'
    elif 'FM-1' in p0:
        dev = 'M-VAVE FM-1'
        if 'bank' in f: g, i, n = 'Bank', 'Bank (32 Voices)', 'DX7-32-Voice-SysEx, 4104 Byte'
        else:
            tag = re.sub(r'^\d+-', '', name); a, b = tag.split('_', 1); g = 'Voice'
            i = {'KCK': 'Kick', 'KOT': 'Ko-Tsuzumi', 'OTS': 'Ō-Tsuzumi', 'KOTO': 'Koto', 'SHM': 'Shamisen'}.get(a, a); kz, v = a, b.replace('_', ' '); n = 'VCED 163 Byte; Raten/Pitch-EG geschätzt'
    elif 'MicroFreak' in p0:
        dev = 'Arturia MicroFreak'; tag = name.replace('mf-MMM_', ''); a = tag.split('_')[0]; g = 'Patch'
        i = {'KCK': 'Kick', 'RUMBLE': 'Kick (Rumble)', 'KOT': 'Ko-Tsuzumi', 'OTS': 'Ō-Tsuzumi', 'KOTO': 'Koto', 'SHAMI': 'Shamisen'}.get(a, a); kz = a; v = tag; n = 'Matrix-Beträge am Gerät von Hand'
    elif 'Volca' in p0: dev, g, i, n = 'Korg Volca Drum', 'Set', ('Parts 1-4 (Koto, Shamisen)' if saiten else 'Parts 1-4 (Kick, Rumble, KOT, OTS)'), 'CC-Setup + Hörprobe; Wert->Modell ungeprüft'
    elif 'Web' in p0: dev, g, i, n = 'Browser', 'Hörprobe', 'Audition-Seite (Referenz-Renderer)', 'nicht im Hub'
    elif 'Audio-Referenz' in p0: dev, g, i, n, kz = 'WAV (Referenz)', 'Audio', ('Koto' if 'koto' in f else 'Shamisen'), 'Referenz-Renderer, keine Hörprobe am Gerät', 'KOTO' if 'koto' in f else 'SHM'; v = name.split('_', 1)[1]
    if len(paths) > 1: n = (n + '; ' if n else '') + 'doppelt abgelegt'
    return [karte, g, i, kz, v, dev, f, quelle, status, n]

for f in sorted(found, key=lambda x: (found[x][0], x)):
    r = classify(f, sorted(found[f]))
    if r is None: print('keine Metadaten:', f); continue
    rows.append(r + [' | '.join(sorted(found[f]))])
rows = [rows[0]] + sorted(rows[1:], key=lambda r: (r[0], r[1], r[2], r[5], r[6]))
csv.writer(open(OUT, 'w', newline='', encoding='utf8')).writerows(rows)
from collections import Counter
print(len(rows) - 1, 'Zeilen', dict(Counter(r[0] for r in rows[1:])))
