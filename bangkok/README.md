# PT Bangkok KB — Simple Calculator

> **Mulai 9 Okt 2026 kandungan KB dan `calc-config.json` datang dari PT R&D Costing Hub** (`prod-at22/pt-calculator-hub`, `data/kb/bangkok.json`). Fail di sini ditulis semula oleh mirror — **jangan edit di GitHub repo ini**; edit di hub. Skema di bawah masih terpakai.

Halaman live: **https://prod-at22.github.io/pt-kb-house/bangkok/**

Repo ini ada dua fail yang penting:

| Fail | Apa dia | Boleh PO edit? |
|---|---|---|
| `calc-config.json` | **semua nombor dan itinerary kalkulator** — harga tier, kadar peak, kadar transport ikut kawasan, blok itinerary, add-on, surcaj | **Ya** — edit terus di sini |
| `index.html` | halaman KB penuh + enjin kalkulator | Tidak — perlu bina semula |

Halaman membaca `calc-config.json` **setiap kali dibuka**. Jadi ubah nombor dalam fail
itu, commit, refresh halaman — terus naik. Tak perlu bina semula `index.html`.

---

## Cara edit

1. Klik `calc-config.json` di atas.
2. Klik ikon pensel (**Edit this file**).
3. Ubah nombor yang perlu.
4. Scroll bawah → **Commit changes**.
5. Tunggu ~30 saat, refresh halaman KB.

### Jaring keselamatan

Kalau JSON tersalah tulis (koma tertinggal, kurungan tak tutup) atau bentuknya salah,
halaman **tidak** rosak. Ia guna balik config lama yang terbenam dalam `index.html`
dan papar notis merah di atas tab Simple Calculator. Kalau notis itu keluar, maksudnya
**suntingan tak terpakai** — betulkan JSON dan commit semula.

---

## Sumber nombor

| Bahagian | Sumber |
|---|---|
| Tier harga, single supplement, peak, late booking, deposit, upgrade hotel, add-on Day 3, Long Tail Boat, Giraffe Encounter, Dinner Cruise | Katalog **PT BANGKOK STANDARD (4D3N) 2026 v3** (kemas kini 1 Julai 2026) |
| Kadar transport ikut tour & kelas kenderaan (tambah / tolak), malam tambahan hotel per bilik, tolak malam per pax, hidangan tambahan RM 20, tiket attraction | **Rate Card Operasi PT Bangkok**, PO 3 September 2026 |

Rate card penuh dipapar dalam tab **Simple Customisation** halaman KB.

---

## Di mana benda yang biasa diubah

### Harga katalog (tier per pax)

`variants[0].tiers` — `a` = adult, `c` = Child With Bed, `n` = Child No Bed.

```json
{"from": 4, "to": 5, "a": 1297, "c": 1197, "n": 1097}
```

Hanya satu varian: `std` = PT Bangkok Standard 4D3N.

### Kadar peak season

`peak` — RM 80 per pax per malam peak.

```json
"peak": {"mode": "perNight", "value": 80,
         "windows": [["2026-12-20","2027-01-05"],
                     ["2027-02-05","2027-02-07"],
                     ["2027-04-13","2027-04-15"]]}
```

Nak tambah tetingkap baharu: tambah satu baris `["2027-12-20","2028-01-05"]`.

### Kadar transport ikut kawasan

`variants[0].ext.rates.day` — kunci = tag kawasan, nilai = band pax.

```json
"[Pattaya]": [{"from":1,"to":4,"normal":525},
              {"from":5,"to":8,"normal":610},
              {"from":9,"to":16,"normal":610}]
```

Band ikut **kelas kenderaan** rate card: 1–4 pax SUV, 5–8 pax Minivan. Band 9–16
ialah 2 kenderaan (`paxPerVehicle` = 8), jadi kadarnya didarab 2 oleh enjin.

`ext.rates.dayDed` ialah lajur **Harga Tolak** rate card (nombor negatif) — dipakai
bila TC tukar hari berpandu jadi Free & Easy.

`_default` sengaja `null`: hari tambahan tanpa blok kawasan akan papar cip merah
`kadar?`, bukan RM 0. Itu memang niatnya — TC mesti pilih blok day tour.

### Malam tambahan hotel

Rate card memberi kadar **per bilik**, bukan per pax, jadi malam tambahan ialah
**add-on asas unit** dalam `addons` (TC isi bilangan bilik):

```json
["Malam tambahan hotel 3 bintang - per bilik", 160, 0, "unit"]
["Malam tambahan hotel 3 bintang PEAK - per bilik", 210, 0, "unit"]
```

Peak dikira sebagai baris berasingan (160 + 50 peak = 210; 4★ dan 5★ + 80).

Upgrade tier pada malam **pakej** kekal per pax ikut katalog —
`ext.rates.up4` (RM 50/pax/malam) dan `ext.rates.up5` (RM 60/pax/malam).

Tolak malam pakej ialah `ext.rates.nightShort` / `nightShort4` / `nightShort5`
(−50 / −100 / −150 per pax per malam, rate card).

### Hidangan tambahan

`mealDelta` — RM 20 per pax setiap hidangan yang TC tambah.

```json
"mealDelta": {"add": 20, "drop": 0}
```

`drop` sengaja 0: pakej Bangkok Standard breakfast sahaja, jadi tiada lunch/dinner
untuk ditolak.

### Add-on / tiket

`addons` — `["Nama", hargaDewasa, hargaKanak, asas]`.
`asas` = `"pax"` (kuantiti diisi sendiri ikut pax) atau `"unit"` (per bot / per
group / per bilik — TC isi kuantiti).

Nombor **negatif** = buang item yang sudah ada dalam pakej.

---

## Percanggahan katalog vs rate card (keputusan PO 3 September 2026)

| Item | Rate card | Katalog | Yang dipakai |
|---|---|---|---|
| Long Tail Boat Damnoen Saduak | RM 260 / bot (maks 6 pax) | RM 280 / bot | **Katalog RM 280** |
| Giraffe Encounter | RM 125 / pax | RM 135 / pax | **Katalog RM 135** |
| Malam tambahan 4★ / 5★ | tertulis "per person" | — | **per bilik** (sama seperti 3★; "person" salah taip) |
| Lunch / dinner RM 20 | di lajur "Tolak 1 Meal" | — | **harga tambah**, bukan tolak |
| Asas jam transport | 10 jam | 12 jam | pakej **12 jam**, hari tambahan **10 jam** |

Dua perkara lagi yang masih terbuka dan patut disahkan dengan operasi:

- **9–10 pax** tiada band khusus dalam rate card. Kalkulator kira **2 × kadar Minivan**.
- Katalog tulis peak Christmas/New Year sebagai *"20 Dec 2026 – 5 Jan **2026**"* —
  jelas salah taip; config guna **5 Jan 2027**.
