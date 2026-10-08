# PT JPN Japan KB — Simple Calculator

> **Mulai 9 Okt 2026 kandungan KB dan `calc-config.json` datang dari PT R&D Costing Hub** (`prod-at22/pt-calculator-hub`, `data/kb/jepun.json`). Fail di sini ditulis semula oleh mirror — **jangan edit di GitHub repo ini**; edit di hub. Skema di bawah masih terpakai.

Halaman live: **https://prod-at22.github.io/pt-kb-house/jepun/**

Repo ini ada dua fail yang penting:

| Fail | Apa dia | Boleh PO edit? |
|---|---|---|
| `calc-config.json` | **semua nombor dan itinerary kalkulator** — harga tier, tetingkap peak, kadar transport ikut kawasan, blok itinerary, add-on, surcaj | **Ya** — edit terus di sini |
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

## PALING PENTING — 11 kadar yang masih kosong

Kalkulator ini sengaja **tidak meneka** kadar yang Jepun belum terbitkan harga jual.
Setiap kadar `0` di bawah akan papar cip merah **`kadar?`** pada baris hari dan satu
baris amaran dalam ringkasan. Isi nombornya di sini bila Sales / operator dah bagi.

### a) Kawasan transport tanpa harga jual — `variants[].ext.rates.day`

| Kawasan | Ada dalam ProdReq? | Nota |
|---|---|---|
| `[Disneyland]` | 5.2 kos mentah RM 527 / 620 / 775 sehala | tiada harga jual |
| `[USJ]` | 5.3 kos mentah RM 465 / 620 / 775 sehala | tiada harga jual |
| `[Kamakura]` | 5.2 kos mentah RM 2,325 / 2,635 / 2,945 | tiada harga jual |
| `[Kobe]` | tiada dalam ProdReq | Kobe hanya ada entrance fee |
| `[Nara+Kyoto]` | 5.3 kos mentah RM 1,550 / 2,015 / 2,325 | tiada harga jual |
| `[Shinkansen]` | 5.2 transfer hotel↔stesen RM 527 / 620 / 775 | tiada harga jual |
| `[Haneda]` `[Narita]` `[Kansai]` | 5.2 / 5.3 kos mentah | airport transfer tambahan |
| `[Hokkaido]` | **ProdReq tidak meliputi Hokkaido** | semua hari tambahan Hokkaido = RM 0 |
| `_default` | — | sengaja gap: paksa TC pilih blok berkawasan |

### b) Kunci kadar lain yang kosong — `variants[].ext.rates`

| Kunci | Maksud | Kesan sekarang |
|---|---|---|
| `dayDed` | tolak dari katalog bila hari berpandu jadi free & easy | pilihan *tolak driving guide* tidak menolak apa-apa |
| `airport` | airport transfer tambahan | pilihan *Airport Transfer tambahan* = RM 0 |
| `airportDed` | airport transfer dibuang dari katalog | tidak menolak apa-apa |
| `nightShort` | tolak per pax bila malam kurang dari pakej | *Tanpa hotel* tidak menolak apa-apa |
| `cityTransfer` | transfer hotel↔stesen Shinkansen (2 kali setiap perpindahan) | blok *Pindah bandar* kira Shinkansen sahaja |

### c) Malam tambahan Hokkaido — `variants[].ext.night`

Hokkaido `ext.night` = `0`. Tokyo / Osaka / Tokyo–Osaka guna ProdReq 5.4
(**Basic RM 250**, **Standard RM 300** per pax per malam) — ProdReq tidak meliputi Hokkaido.

---

## Di mana benda yang biasa diubah

### Harga katalog (tier per pax)

`variants[].tiers` — `a` = adult, `c` = CWB, `n` = CNB.

```json
{"from": 4, "to": 5, "a": 3497, "c": 3297, "n": 3097}
```

Varian: `tokyob` Tokyo Basic · `tokyos` Tokyo Standard · `osakab` Osaka Basic ·
`osakas` Osaka Standard · `tobab` Tokyo–Osaka Basic · `tobas` Tokyo–Osaka Standard ·
`hokkaido` Hokkaido-Sapporo.

### Tetingkap peak season

Peak Jepun ialah **peratus atas harga tier**, bukan RM per malam.

`peak` peringkat atas dipakai untuk Tokyo / Osaka / Tokyo–Osaka (`+10%`, dari katalog):

```json
"peak": {"mode": "percent", "value": 10,
         "windows": [["2026-09-19","2026-09-23"],
                     ["2026-12-30","2027-01-03"]]}
```

`variants[].peak` untuk **Hokkaido** ada dua tahap. Elemen **keempat** dalam satu
tetingkap = kadar khas tetingkap itu:

```json
["2026-12-20","2027-01-05", null, 15]
```

Bila dua tetingkap bertindih (contoh 20 Disember), kalkulator ambil yang **paling
tinggi** — jadi susunan senarai tidak penting.

> **Tetingkap 2027 untuk Tokyo / Osaka / Tokyo–Osaka ialah unjuran**, bukan dari
> katalog (katalog 2026 sah hingga 31 Dis 2026 sahaja). Yang dimasukkan hanya
> 4 perayaan bertarikh tetap: Sakura 28 Mac–15 Apr, Golden Week 29 Apr–6 Mei,
> Obon 13–16 Ogos, New Year 30 Dis–3 Jan. **Silver Week 2027 sengaja ditinggalkan**
> kerana tarikhnya berubah setiap tahun — tambah bila PO dah tahu tarikhnya.

### Kadar transport ikut kawasan

`variants[].ext.rates.day` — kunci = tag kawasan, nilai = band pax.
Band ikut ProdReq 5.1: **1–7 pax** 7-seater · **8 pax** Hiace · **9–12 pax** Coaster.

```json
"[Tokyo City]": [{"from":1,"to":7,"normal":3000,"peak":3000},
                 {"from":8,"to":8,"normal":4300,"peak":4300},
                 {"from":9,"to":12,"normal":4600,"peak":4600},
                 {"from":13,"to":99,"normal":0,"peak":0}]
```

Kawasan yang **ada** harga jual sekarang: `[Tokyo City]` dan `[Fuji]`
(3,000 / 4,300 / 4,600) · `[Osaka City]` (3,000 / 3,400 / 3,800) ·
`[Nara]` dan `[Kyoto]` (3,300 / 3,700 / 4,400). Sumber: tab
*Simple Customisation* — jadual "Add-on Private Transport, sewa satu trip".

Kadar tersiar lain dalam `ext.rates`:

| Kunci | Maksud | Nilai |
|---|---|---|
| `upg3` | upgrade apartment / hotel 3 bintang, malam pakej | 300 per pax per malam |
| `bf` | breakfast tambahan | 47 per pax (ProdReq 5.7: RM 46.50) |
| `legShin` | Shinkansen Tokyo ↔ Osaka, sehala | 600 per pax (ProdReq 5.6) |

### Blok itinerary

`library[]` — 33 blok yang muncul dalam dropdown Itinerary setiap hari, dikumpulkan
ikut `g`: *Tokyo - ketibaan & pulang · Tokyo - bandar · Tokyo - Fuji & luar bandar ·
Tokyo - theme park · Osaka - ketibaan & pulang · Osaka - bandar · Osaka - Kyoto, Nara
& Kobe · Osaka - theme park · Pindah bandar · Hokkaido · Umum*.

```json
{"v": "tkf", "g": "Tokyo - Fuji & luar bandar", "region": "[Fuji]",
 "t": "Fuji Tour (private transport)", "en": "MOUNT FUJI TOUR",
 "acc": "incl", "meal": "none", "trp": "incl",
 "act": ["Iyashi No Sato (Samurai Village)", "Oishi Park", "Fujikawaguchiko"],
 "eact": ["Iyashi No Sato (Samurai Village)", "Oishi Park", "Fujikawaguchiko"]}
```

| Medan | Maksud |
|---|---|
| `v` | kunci unik — **jangan sama** dengan blok lain |
| `g` | kumpulan dalam dropdown |
| `region` | tag kawasan → menentukan kadar transport hari itu |
| `t` / `act` | nama & aktiviti **Bahasa Melayu** — dipapar pada baris hari |
| `en` / `eact` | nama & aktiviti **Bahasa Inggeris** — untuk PDF quotation |
| `acc` / `meal` / `trp` | pilihan default bila blok ini dipilih |

`variants[].itin[]` = itinerary default pakej. Bentuknya sama, dan bilangannya
**mesti** sama dengan `days`.

> Kalau nak tulis simbol `&` dalam `t`, `en`, `act`, `eact`, `inclusions`,
> `exclusions` — tulis `&` biasa sahaja, jangan `&amp;`.

### Add-on / optional activity

`addons[]` — `["Nama", hargaAdult, hargaChild, "pax"]`. Elemen ke-4 `"pax"` bermakna
kuantiti diisi sendiri ikut bilangan pax berbayar; `"unit"` bermakna TC taip sendiri.
Nama masuk PDF quotation, jadi **tulis dalam Bahasa Inggeris**.

### Lain-lain

| Nak ubah | Di mana |
|---|---|
| Single supplement Tokyo / Osaka / Tokyo–Osaka | `variants[].single` |
| Single supplement Hokkaido (per malam) | `variants[].singlePerNight` |
| Harga infant | `variants[].infant` |
| Deposit per pax | `deposit` |
| Late booking surcharge | `lateBooking` |
| Last minute surcharge | `lastMinute` |
| Surcaj travel date 2027 | `extraSurcharge[]` |
| Harga lunch / dinner | `meals` |
| Nota ikut saiz group | `paxNotes[]` |
| Inclusions / exclusions PDF | `variants[].inclusions`, `exclusions`, `exclusionsTail` |
| Teks bawah PDF quotation | `validity` |

---

## Yang masih perlu dibina semula (bukan dalam JSON)

- Isi tab lain: FAQ, Harga & Pakej, Surcharge, Travel Map, Accommodation, dan lain-lain
- Logik enjin kalkulator (cara ia mengira)
- Susun atur / warna
- "Last updated" pada topbar

---

## PENTING — elak kerja PO ditimpa

Selepas PO mula edit `calc-config.json` di sini, **fail ini jadi sumber sebenar**.
Kalau halaman dibina semula dari config lama, suntingan PO akan hilang.

Jadi bila minta apa-apa perubahan pada enjin atau tab lain, sebut sekali:
**"config sudah diedit dalam GitHub, ambil versi terbaru dari repo dahulu."**

---

## Percanggahan sumber yang PO perlu putuskan

1. **Tetingkap peak.** Katalog dan ProdReq 4C **tidak sama**. Kalkulator ikut
   **katalog**. ProdReq 4C jauh lebih lebar: 22 Dis–5 Jan · 25 Jan–10 Feb ·
   15 Mac–15 Apr · 28 Apr–7 Mei · 10 Jul–25 Ogos · 28 Sep–7 Okt · 1 Nov–10 Dis.
   Kalau ProdReq yang betul, banyak lagi tarikh kena +10%.
2. **Jadual harga.** ProdReq 10 memberi harga yang **berbeza** daripada katalog 2026
   (contoh Tokyo Basic 2 pax: ProdReq RM 3,897 vs katalog RM 4,997). Kalkulator ikut
   **katalog** kerana itulah dokumen customer-facing yang bertarikh 9 Mac 2026.
3. **Kadar ProdReq 5 ialah kos mentah** (rate 0.031), belum tolak margin RM 600–900.
   Yang dipakai dalam kalkulator: 5.4 malam tambahan, 5.6 Shinkansen, 5.7 breakfast.

---

*Sumber nombor: katalog PT Tokyo Basic v6 / Tokyo Standard v1 / Osaka Basic v1 /
Osaka Standard v1 / Tokyo-Osaka Basic v1 / Tokyo-Osaka Standard v1 (9 Mac 2026),
PT HOKKAIDO-SAPPORO 5D4N 2026 v3 (8 Ogos 2026), tab Simple Customisation KB Jepun,
dan `PT JPN ProdReq.md` seksyen 5.1 / 5.4 / 5.6 / 5.7 / 9.
Repo ini public — ia mengandungi harga dalaman.*
