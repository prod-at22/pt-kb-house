# PT Bali KB — Simple Calculator

> **Mulai 9 Okt 2026 kandungan KB dan `calc-config.json` datang dari PT R&D Costing Hub** (`prod-at22/pt-rnd-hub`, `data/kb/bali.json`). Fail di sini ditulis semula oleh mirror — **jangan edit di GitHub repo ini**; edit di hub. Skema di bawah masih terpakai.

Halaman live: **https://prod-at22.github.io/pt-kb-house/bali/**

Repo ini ada dua fail yang penting:

| Fail | Apa dia | Boleh PO edit? |
|---|---|---|
| `calc-config.json` | **semua nombor dan itinerary kalkulator** — harga tier, kadar peak, upgrade hotel, kadar transport, blok itinerary, add-on, surcaj | **Ya** — edit terus di sini |
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

## Tiga varian

| `id` | Pakej | Model harga |
|---|---|---|
| `std` | PT Bali Standard 4D3N | per pax, 5 band (2–3 … 10–15 pax) |
| `hnystd` | PT Bali Honeymoon Standard 4D3N | **flat per pasangan** RM 2,197 |
| `hnyprem` | PT Bali Honeymoon Premium 4D3N | **flat per pasangan** RM 3,797 |

> **Kenapa tier Honeymoon tertulis 1098.5 dan 1898.5?**
> Enjin mengira per pax. Harga katalog per pasangan dibahagi 2 supaya 2 pax
> menghasilkan RM 2,197 / RM 3,797 tepat. Kalau katalog naikkan harga pasangan,
> **bahagi 2** sebelum masukkan di sini.

---

## Di mana benda yang biasa diubah

### Harga katalog (tier)

`variants[].tiers` — `a` = adult, `c` = CWB (6–11), `n` = CNB (2–5).

```json
{"from": 4, "to": 5, "a": 997, "c": 957, "n": 897}
```

### Kadar peak season

`variants[].peak` — `value` = RM **per pax per malam** peak. Setiap varian ada
kadarnya sendiri sebab katalog menetapkan kadar berbeza ikut kelas hotel pakej:

| Varian | `value` | Asal katalog |
|---|---|---|
| `std` | 40 | 3★ RM40/pax/malam |
| `hnystd` | 40 | 3★ RM80/pasangan/malam |
| `hnyprem` | 60 | 4★ RM120/pasangan/malam |

Elemen **keempat** dalam satu tetingkap = kadar khas tetingkap itu. Ia dipakai untuk
1–5 Jan 2027, di mana rate sheet menetapkan RM40/pax/malam untuk semua varian:

```json
"windows": [["2026-08-01","2026-08-31"],
            ["2027-01-01","2027-01-05", null, 40]]
```

Nak tambah tetingkap baharu: tambah satu baris `["2027-08-01","2027-08-31"]`.

### Upgrade hotel pada malam pakej

`ext.rates.up4a` / `up4b` / `upvPool` / `upvPrem` / `upvLux` — RM **per pax per malam**.

> **Baca ini sebelum edit lajur `peak`.**
> `normal` = harga upgrade seperti dalam katalog (dibahagi 2 untuk kadar per pasangan).
> `peak` = harga upgrade **campur beza surcaj peak season** hotel itu berbanding
> surcaj asas varian (RM40/pax). Contoh Adhi Jaya: upgrade RM80/pax, peak season
> hotel itu RM100/pax berbanding 3★ RM40/pax → `peak` = 80 + (100 − 40) = **140**.
> Sebabnya enjin hanya ada satu kadar peak per varian, jadi beza hotel dibawa di sini.

| Kunci | Hotel | `normal` | `peak` |
|---|---|---|---|
| `up4a` | The One / Sun Island / Akmani Legian | 60 | 80 |
| `up4b` | Adhi Jaya / Wyndham Garden | 80 | 140 |
| `upvPool` | Asa Bali / Sakaye / Maca Umalas | 230 | 270 |
| `upvPrem` | Alaya Dedaun / Lumbini | 325 | 410 |
| `upvLux` | Asterra Seminyak | 390 | 475 |

### Malam villa pakej Honeymoon dalam peak season — perlu satu klik TC

Malam villa dalam pakej Honeymoon kena surcaj peak season lebih tinggi daripada malam
hotel (RM160 vs RM80 sepasangan untuk HNY Standard; RM250 vs RM120 untuk HNY Premium).
Enjin hanya ada **satu** kadar peak per varian, jadi bezanya dibawa sebagai pilihan
Accommodation yang TC pilih pada hari villa:

| Pilihan | Varian | Tambah |
|---|---|---|
| `vpk1` | HNY Standard | RM40/pax = RM80/pasangan |
| `vpk2` | HNY Premium | RM65/pax = RM130/pasangan |

Bila tarikh **bukan** peak, biarkan pada `villa` / `lvilla` (tiada kos).
Nota ini juga dipapar di atas kalkulator supaya TC tak terlepas pandang.

### Kadar transport

`ext.rates.day` — RM **per transport** (bukan per pax), dikongsi seluruh group.
Kunci = jenis tour hari itu; nilai = band ikut kapasiti kenderaan.

```json
"[Full Day]": [{"from":2,"to":4,"normal":250,"peak":250},
               {"from":5,"to":6,"normal":350,"peak":350},
               {"from":7,"to":12,"normal":450,"peak":450}]
```

| Kunci | Jenis tour | 2–4 pax (Avanza) | 5–6 (Innova) | 7–12 (Hiace) |
|---|---|---|---|---|
| `[Full Day]` | Full Day Tour 12 jam | 250 | 350 | 450 |
| `[Half Day]` | Half Day Tour 5–6 jam | 150 | 200 | 400 |
| `[Airport + Half Day]` | Airport transfer + half day 6 jam | 200 | 200 | 200 |
| `[Airport Transfer]` | Airport transfer sahaja | 150 | 200 | 200 |

`ext.rates.dayDed` = lajur **Harga Tolak** untuk jenis tour yang sama (nombor negatif).
Ia dipakai bila TC tukar hari berpandu jadi Free & Easy.

### Malam tambahan hotel

`ext.night` = malam tambahan 3★ (RM80 normal / RM120 peak, per pax).
Kategori lain dalam `ext.rates`:

| Kunci | Kategori | normal | peak |
|---|---|---|---|
| `h4a` | 4★ The One / Sun Island / Akmani | 120 | 180 |
| `h4b` | 4★ Adhi Jaya / Wyndham | 140 | 220 |
| `vPool` | Private Pool Villa | 280 | 460 |
| `vPrem` | Premium Private Pool Villa | 380 | 660 |
| `vLux` | Luxury Private Pool Villa | 450 | 890 |
| `nightShort` | tolak 1 malam pakej | −50 | **0** |

`nightShort` lajur peak sengaja `0` sebab rate card **tiada** kadar tolak untuk peak
season. Kalau TC cuba tolak malam dalam peak, halaman papar cip merah `kadar?` —
itu memang niatnya, bukan pepijat. Isi nombor di situ hanya bila operator bagi kadar.

### Blok itinerary

`library[]` — blok yang muncul dalam dropdown Itinerary setiap hari (5 tour tambahan
full day + Nusa Dua + Nusa Penida + hari tambahan + transfer).
`variants[].itin[]` = itinerary default pakej; bilangannya **mesti** sama dengan `days`.

```json
{"v": "tanahlot", "g": "Tour tambahan - full day", "region": "[Full Day]",
 "t": "Tanah Lot Full Day Tour", "en": "TANAH LOT FULL DAY TOUR",
 "acc": "incl", "meal": "b", "trp": "incl",
 "act": ["..."], "eact": ["..."]}
```

| Medan | Maksud |
|---|---|
| `v` | kunci unik — **jangan sama** dengan blok lain |
| `g` | kumpulan dalam dropdown |
| `region` | jenis tour → menentukan kadar transport hari itu |
| `t` / `act` | nama & aktiviti **Bahasa Melayu** (dipapar dalam kalkulator) |
| `en` / `eact` | nama & aktiviti **Bahasa Inggeris** (untuk PDF quotation) |

Blok tour tambahan default kepada transport **dalam pakej**, jadi menukar salah satu
hari pakej kepada tour lain adalah RM 0 (memang substitusi). Bila TC tekan
**+ Tambah Hari**, enjin sendiri tukar kepada malam + transport berbayar.

> Tulis simbol `&` biasa sahaja dalam `t`, `en`, `act`, `eact`, `inclusions`,
> `exclusions` — jangan `&amp;`.

### Add-on / optional activity

`addons[]` — `["Nama", hargaAdult, hargaChild]`. Elemen keempat `"unit"` bermakna
harga **per pasangan / per unit**, bukan per pax (dipakai untuk honeymoon dinner
dan room decoration). Kuantiti diisi sendiri ikut pax.

### Lain-lain

| Nak ubah | Di mana |
|---|---|
| Single supplement | `variants[].single` (250 / 800 / 1500) |
| Deposit per pax | `deposit` (250) |
| Late booking RM50 | `lateBooking` |
| Surcaj travel date 2027 | `extraSurcharge[]` (RM50 std & hnystd, RM100 hnyprem) |
| Harga tambah/tolak meal | `mealDelta` (tambah 35, tolak 20) |
| Inclusions / exclusions PDF | `variants[].inclusions`, `exclusions`, `exclusionsTail` |
| Teks bawah PDF quotation | `validity` |
| Nota ikut saiz group | `paxNotes[]` |
| Nota di atas kalkulator | `intro` |

---

## Yang kalkulator TIDAK buat

- **Blackout dates tidak menyekat**. Hari Nyepi 18–20 Mac 2026, Hari Raya 20–23 Mac
  2026, dan Nyepi 2027 (5–10 Mac, 9–12 Mac) tetap boleh dikira. Amaran dipapar dalam
  `intro` dan `validity`; TC kena semak sendiri.
- Peak dikira ikut **malam**, tetapi kadar upgrade hotel dan villa dipilih ikut
  **trip** (peak kalau ada mana-mana malam peak). Untuk trip yang separuh peak
  separuh normal, semak semula secara manual.
- Tiada tier harga untuk group > 15 pax dan tiada kadar transport melebihi Hiace
  12 pax — nota ini muncul sendiri bila pax ≥ 13.

## Kadar yang perlu disahkan

Datang dari rate card ARBA (PT_DPS) / sheet customisation, **bukan** katalog v3:

- Semua kadar tambah/tolak transport, accommodation dan meal
- Infant bawah 2 tahun = FOC
- Tiket masuk tour tambahan (Ulun Danu, Wanagiri, Handara, Lempuyang, Tirta Empul,
  Tirta Gangga, Tegallalang, Kintamani Lookout, Tegenungan) — sheet tour lama;
  sahkan dengan operator sebelum quote tarikh jauh
- Kadar villa dalam jadual Accommodation ditulis **per pax/malam**, sedangkan jadual
  Surcharge menulis villa **per pasangan/malam**. Config ikut jadual masing-masing;
  sahkan yang mana betul.

---

## PENTING — elak kerja PO ditimpa

Selepas PO mula edit `calc-config.json` di sini, **fail ini jadi sumber sebenar**.
Kalau halaman dibina semula dari config lama, suntingan PO akan hilang.

Jadi bila minta apa-apa perubahan pada enjin atau tab lain, sebut sekali:
**"config sudah diedit dalam GitHub, ambil versi terbaru dari repo dahulu."**

---

*Sumber nombor: katalog PT BALI STANDARD / HONEYMOON STANDARD / HONEYMOON PREMIUM
(4D3N) v3 — 2 Februari 2026, rate sheet 2026/2027 Date Surcharge, rate card PT_DPS,
sheet customisation tambah/tolak PT Bali, sheet tour add-on PT Bali.
Repo ini public — ia mengandungi harga dalaman.*
