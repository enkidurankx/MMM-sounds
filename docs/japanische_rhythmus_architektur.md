# Traditionelle Japanische Rhythmus-Strukturen (für MIDI-Sequencing)

Dieses Dokument bündelt die essenziellen Rhythmus- und Strukturkonzepte der traditionellen japanischen Musik (insbesondere Taiko und Percussion), übersetzt in algorithmische und MIDI-basierte Logik.

## 1. Fundamentale Makro- und Mikrostrukturen

Die japanische Musik bricht mit dem westlichen Rasterdenken (starre BPM, feste Taktarten). Die Essenz liegt in der Elastizität der Zeit.

### Jo-ha-kyū (Die Makro-Zeitachse)
Eine exponentielle Spannungskurve, die die klassische westliche Songstruktur ersetzt.
*   **Jo (Einleitung):** Langsam, suchend, frei im Metrum. Keine festen Beats. (Hohe Wahrscheinlichkeit für Pausen).
*   **Ha (Entwicklung):** Etablierung eines festen Rhythmus. Zunehmende Dichte und Beschleunigung.
*   **Kyū (Kulmination):** Extrem hohes Tempo, rapides und hartes Ende.
*   *App-Integration:* Benötigt eine variable Master-Clock, bei der das Tempo basierend auf dem Fortschritt im Zyklus exponentiell ansteigt.

### Ma (Der bewusste Raum / Mikro-Zeit)
*Ma* ist nicht einfach das Auslassen einer Note, sondern eine lokale Zeit-Dilatation. Es erzeugt Spannung durch Stille.
*   *App-Integration:* Ein deterministischer Algorithmus streut asymmetrische Pausen ein. Die Zeit bis zum nächsten Anschlag wird algorithmisch gedehnt (z.B. multipliziert mit einem Faktor wie $1.618$), während der Makro-Rhythmus im Hintergrund weiterläuft. Der Anschlag *nach* einem *Ma* erfordert oft eine extrem hohe MIDI-Velocity zur Spannungsentladung.

### Kuchi Shōga (Phonetisches MIDI-Mapping)
Rhythmen werden gesungen. Die Silben definieren Anschlagsort (Timbre/MIDI-Kanal) und Intensität (Velocity).
*   **DON / DO:** Mitte, stark (Velocity 100-127). Tiefe Oszillatoren/Taiko.
*   **tsu / ko / ro:** Mitte, schwach (Velocity 30-60). Ghost Notes.
*   **KA / ka:** Rand/Rim, stark (Velocity 90-120). Scharfe Transienten.
*   **su:** Pause / Leere (*Ma*).

---

## 2. Traditionelle Pattern-Bausteine (Jiuchi)

Die Basis-Grooves (*Jiuchi*) bilden das Fundament. Die folgenden JavaScript-Arrays (1 Step = 1 Sechzehntel) dienen als Baupläne für die Sequencer-Engine.

### 2.1 Matsuri Ji (Der Festival-Groove)
Ein treibender Rhythmus mit einem charakteristischen asymmetrischen Swing (zwischen geraden 16teln und harten Triolen).
```javascript
// Raster: 16tel Schritte (1 Takt)
const patternMatsuri = [
  { hit: "DON", vel: 120 }, { hit: null }, { hit: null }, { hit: null },
  { hit: "DON", vel: 110 }, { hit: null }, { hit: "ko", vel: 50 }, { hit: null },
  { hit: "DON", vel: 120 }, { hit: null }, { hit: null }, { hit: null },
  { hit: "DON", vel: 110 }, { hit: null }, { hit: "ko", vel: 50 }, { hit: null }
];
```

### 2.2 Miyake (Die physische Schwere)
Tief, langsam und kraftvoll. Nutzt *Ma* exzessiv vor dem finalen, triolischen Einschlag. Perfekt für dröhnende Sub-Bässe.
```javascript
// Raster: 8tel Schritte
const patternMiyake = [
  { hit: "DON", vel: 127 }, { hit: null }, { hit: null }, { hit: "DON", vel: 110 },
  { hit: "DON", vel: 110 }, { hit: null }, { hit: null }, { hit: "DON", vel: 110 },
  { hit: "DON", vel: 127 }, { hit: "DON", vel: 127 }, { hit: "DON", vel: 127 }, { hit: null }
];
```

### 2.3 Hachijō (Poly-Rhythmik und Rim-Shots)
Dichter, triolischer Teppich, der fast ausschließlich auf dem Rand (KA) gespielt wird, während Soli auf dem Fell (DON) darüber synkopieren.
```javascript
// Raster: 8tel-Triolen (6/8 oder 12/8 Feel)
const patternHachijoJi = [
  { hit: null }, { hit: "KA", vel: 100 }, { hit: "KA", vel: 90 }, 
  { hit: null }, { hit: "KA", vel: 100 }, { hit: "KA", vel: 90 }
];
```

### 2.4 Yatai-Bayashi (Die kinetische Welle)
Triolisches Raster, das durch kontinuierliches Crescendo und Decrescendo lebt (Nami / Welle). Erfordert LFO-Modulation der Velocity.
```javascript
// Raster: 8tel-Triolen (12/8 Feel)
const patternYatai = [
  { hit: "DON", vel: 100 }, { hit: "ko", vel: 40 }, { hit: "ko", vel: 40 },
  { hit: "DON", vel: 90 },  { hit: "ko", vel: 40 }, { hit: "ko", vel: 40 },
  { hit: "DON", vel: 120 }, { hit: null },          { hit: "tsu", vel: 70 },
  { hit: "DON", vel: 127 }, { hit: null },          { hit: null }
];
```

### 2.5 Gion Matsuri / Kon-Chiki-Chin (Interlocking)
Verzahnung zweier Timbres: Tiefe Taiko und metallische Glocke (Kane). Synkopiert und ideal für FM-Synthese-Layering.
```javascript
// Raster: 16tel
const patternGion = {
    kane: [ // FM-Synth / Metall (Negative Delay anwenden!)
        { hit: "Kon", vel: 110 }, { hit: null }, { hit: "chi", vel: 60 }, { hit: "ki", vel: 70 },
        { hit: "Chin", vel: 127 }, { hit: null }, { hit: null }, { hit: null }
    ],
    taiko: [ // Analoger Sub
        { hit: "DON", vel: 100 }, { hit: null }, { hit: null }, { hit: null },
        { hit: "DON", vel: 90 }, { hit: null }, { hit: "DON", vel: 110 }, { hit: null }
    ]
};
```

### 2.6 Shishimai (Der gebrochene Puls)
Der Löwentanz. Ungerade Taktarten (z.B. 5/4) oder asymmetrische Gruppierungen brechen die Erwartungshaltung auf.
```javascript
// Raster: 8tel (Gruppierung 3 + 3 + 2)
const patternShishimai = [
  { hit: "DON", vel: 110 }, { hit: "tsu", vel: 50 }, { hit: "DON", vel: 120 },
  { hit: "DON", vel: 110 }, { hit: "tsu", vel: 50 }, { hit: "DON", vel: 120 },
  { hit: "DON", vel: 127 }, { hit: null }
];
```

### 2.7 Noh Hayashi (State-Machine statt Loop)
Event-basiert ohne festes Raster. Ruf (Kakegoe) -> Pause (Ma) -> Anschlag -> Nachhall.
```javascript
const nohEvent = {
    call: { type: "vocal", midiAction: "sweep", durationBase: 1.5 },
    tension_gap: { type: "ma", multiplier: 1.2 },
    strike: { type: "hit", midiAction: "ping", vel: 127 },
    decay_gap: { type: "ma", multiplier: 2.5 }
};
```