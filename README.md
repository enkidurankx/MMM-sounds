# MMM Sound Library (privat)

Zentrale, generative Sound Library (keine Samples). Das öffentliche Repo `enkidurankx/MMM` enthält die Web-Apps und den Hub; alles zu den Sounds gehört hierher.

## Aufbau
| Pfad | Inhalt |
|---|---|
| `MMM-SOUNDS-HANDOVER.md` | Übergabe: Arbeitsweise, Karten, Plattform-Fakten, Konventionen |
| `sounds-library/inventory.csv` | eine Zeile pro Klang und Gerät (Karten 00, 01, 03) |
| `sounds-library/gamelan/README.md` | Karte 03, Benutzung und Ungeprüft-Liste |
| `sounds-library/tools/` | Generatoren (Karte 01, Gamelan, Inventar) |
| `sounds-library/saiten-baustelle/` | pausiert: Koto und Shamisen, nicht anfassen |
| `presets/_Sound Collection Asia/MMM-Gamelan/` | Karte 03: `Operator/` (44 Operator- und Tension-Presets), `Collision/` (43), berechnet, nichts gehört |
| `presets/_Sound Collection Asia/MMM-Japan/` | `Patches/` (Ableton, FM-1, MicroFreak, Volca Drum, Web) und `Audio-Referenz/`; enthält auch die pausierten Koto/Shamisen-Stücke |
| `presets/_Sound Collection Drums/` | `Patches/` (Ableton, FM-1, MicroFreak, Volca Drum) |
| `templates/` | die leeren `.adv` des Owners (Operator, Collision, Tension); die Skripte ersetzen nur `<Manual Value>` darin |
| `docs/` | japanische Instrumenten- und Rhythmusliste (Quellen zu Karte 00) |

`sounds-library/` entspricht 1:1 dem Ordner, der bisher im öffentlichen Repo lag; die Pfade der Skripte gelten unverändert.

## Skripte
Die Gamelan-Generatoren lesen die App `gamelan-v2_0.html` aus dem öffentlichen Repo. Beide Repos nebeneinander auschecken und den Pfad angeben, zum Beispiel:

```
python3 sounds-library/tools/build_gamelan_adv.py ../MMM/gamelan-v2_0.html templates/Operator.adv templates/Tension.adv "presets/_Sound Collection Asia/MMM-Gamelan/Operator"
python3 sounds-library/tools/build_gamelan_collision.py ../MMM/gamelan-v2_0.html templates/Collision.adv "presets/_Sound Collection Asia/MMM-Gamelan/Collision"
```

## Regeln
- Status im Inventar bleibt `berechnet`, bis der Owner sagt, dass er es in Live gehört hat.
- Neue Karten ab 04; die Karten 00, 01 und 03 nicht umnummerieren.
- Nach Änderungen an der Gamelan-App die Presets mit den Skripten neu erzeugen und das Inventar nachziehen.
