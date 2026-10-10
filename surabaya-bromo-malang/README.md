# ARBA — Surabaya · Bromo · Malang KB (TC Reference) + Simple Calculator

> **Mulai 9 Okt 2026 kandungan KB dan `calc-config.json` datang dari PT R&D Costing Hub** (`prod-at22/rnd-hub`, `data/kb/surabaya-bromo-malang.json`). Fail di sini ditulis semula oleh mirror — **jangan edit di GitHub repo ini**; edit di hub. Skema di bawah masih terpakai.

Halaman live: **https://prod-at22.github.io/pt-kb-house/surabaya-bromo-malang/**

Repo ini ada dua fail yang penting:

| Fail | Apa dia | Boleh PO edit? |
|---|---|---|
| `calc-config.json` | **semua nombor dan itinerary kalkulator** — harga tier, kadar peak, kadar transport/malam, blok itinerary, add-on | **Ya** — edit terus di sini |
| `index.html` | halaman KB penuh + enjin kalkulator | Tidak — perlu bina semula |

Halaman membaca `calc-config.json` **setiap kali dibuka**. Ubah nombor dalam fail itu,
commit, refresh halaman — terus naik. Tak perlu bina semula `index.html`.

> ⚠️ Data dalaman: KB ini mengandungi harga katalog ARBA, jadual surcharge dan kod
> kempen free-gift. Repo ini public — sesiapa yang ada URL boleh lihat.

---

## Cara edit

1. Klik `calc-config.json` di atas.
2. Klik ikon pensel (**Edit this file**).
3. Ubah nombor yang perlu.
4. Scroll bawah → **Commit changes**.
5. Tunggu ~30 saat, refresh halaman KB.

### Jaring keselamatan

Kalau JSON tersalah tulis, halaman **tidak** rosak — ia guna balik config terbenam
dalam `index.html` dan papar notis merah di atas tab Simple Calculator. Kalau notis itu
keluar, maksudnya suntingan **tak terpakai** — betulkan JSON dan commit semula.

---

## Empat varian

| id | Pakej |
|---|---|
| `sbm3` | Surabaya–Bromo–Malang 4D3N · Hotel 3★ |
| `sbm4` | Surabaya–Bromo–Malang 4D3N · Upgrade Hotel 4★ (tier + RM240/pax) |
| `sm3` | Surabaya–Malang 4D3N (tanpa Bromo) · Hotel 3★ |
| `sm4` | Surabaya–Malang 4D3N (tanpa Bromo) · Upgrade Hotel 4★ |

Upgrade 4★ dibuat sebagai **varian berasingan**, bukan add-on, sebab caj peak season
berbeza ikut tier hotel (3★ RM130/pax/malam vs 4★ RM180/pax/malam).

---

## Di mana benda yang biasa diubah

### Harga katalog (tier per pax)

`variants[].tiers` — `a` = adult, `c` = CWB (6–11), `n` = CNB (2–5).

```json
{"from": 4, "to": 6, "a": 1397, "c": 1197, "n": 997}
```

Kalau tier 3★ berubah, **jangan lupa** varian 4★ yang sepadan — nilainya = tier 3★ + 240.

### Kadar peak season

`variants[].peak` — `value` = RM per pax per malam peak.

```json
"peak": {"mode": "perNight", "value": 130,
         "windows": [["2026-03-15","2026-03-30"],
                     ["2026-12-20","2027-01-05"]]}
```

`sbm3`/`sm3` guna 130 · `sbm4`/`sm4` guna 180. Nak tambah tetingkap: tambah satu baris
`["YYYY-MM-DD","YYYY-MM-DD"]` pada **setiap** varian yang terjejas.

### Surcaj travel date

`extraSurcharge` sengaja **kosong** (`[]`) — arahan PO: travel date 1 Jan – 30 Jun 2027
tiada surcharge. Kalau senarai Date Surcharge berubah, tambah:

```json
{"label":"Travel date 2027","dateIn":["2027-01-01","2027-06-30"],"perPax":120}
```

### Kadar transport hari tambahan (Rate Card Operasi)

`ext.rates.day` — band ikut bilangan pax; `dayDed` = amaun tolak.

```json
"day": {"_default":[{"from":1,"to":4,"normal":300,"peak":300},
                    {"from":5,"to":10,"normal":900,"peak":900},
                    {"from":11,"to":15,"normal":null,"peak":null}]}
```

Band 11–15 pax sengaja `null` — rate card berhenti pada Hiace 10 pax. Halaman papar cip
merah `kadar?` pada hari itu. Isi nombornya bila operator dah bagi.

### Kadar malam tambahan / tolak (ikut kawasan)

| Kunci | Guna |
|---|---|
| `nAdd` | tambah 1 malam, hotel 3★ — Bromo 130, Malang 100, Surabaya 100 |
| `nAdd4` | tambah 1 malam, hotel 4★ — kadar 3★ + RM85 (kadar upgrade katalog) |
| `nightShort` | tolak 1 malam — Bromo −30, Malang −50, Surabaya −50 |

Kunci kawasan ialah tag yang dipapar sebagai cip pada baris hari: `[Bromo]`,
`[Malang-Batu]`, `[Surabaya]`.

### Meal

`mealDelta` — `add` 35, `drop` 20 (per pax per hidangan, Rate Card Operasi).

### Add-on

`addons` — `["Nama", hargaDewasa, hargaKanak, "pax"|"unit"]`. `"pax"` = kuantiti diisi
sendiri ikut bilangan pax; `"unit"` = TC taip sendiri (contoh local guide Tumpak Sewu,
RM150 untuk 1–5 pax).

### Blok itinerary

`library[]` — blok yang TC boleh pilih pada mana-mana hari. `g` = kumpulan dalam
dropdown, `region` = tag kawasan (menentukan kadar malam/transport hari itu).

Blok `lb_tumpak`, `lb_ijen`, `lb_semeru` sengaja `"trp":"none"` — harga add-on mereka
sudah termasuk transport, jadi hari itu tidak dicaj transport lagi.

---

## Nota sumber

- Katalog: `PT SURABAYA-BROMO-MALANG 4D3N v2` dan `PT SURABAYA-MALANG 4D3N v2`
  (Last Updated 9 Mac 2026).
- Kadar tambah/tolak: Rate Card Operasi Surabaya – Bromo – Malang (transport, accom,
  meals, attraction) — dipapar penuh dalam tab **Simple Customisation**.
- Travel date 1 Jan – 30 Jun 2027: **tiada surcharge** (arahan PO).
