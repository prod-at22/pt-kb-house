# PT Melbourne KB — Simple Calculator

> **Mulai 9 Okt 2026 kandungan KB dan `calc-config.json` datang dari PT R&D Costing Hub** (`prod-at22/pt-calculator-hub`, `data/kb/melbourne.json`). Fail di sini ditulis semula oleh mirror — **jangan edit di GitHub repo ini**; edit di hub. Skema di bawah masih terpakai.

Halaman live: **https://prod-at22.github.io/pt-kb-house/melbourne/**

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

## Sumber setiap kadar

Semua kadar transport, accommodation, meals dan entrance datang dari tab
**Rate Card Operasi** dalam KB (`Transport + Driver`, `Accommodation`, `Meals`,
`Entrance / Activity`). Rate card itu sendiri menyatakan ia untuk kalkulator:
*"Kalkulator pilih kelas kenderaan dan buat pembahagian ini automatik."*

Band kelas kenderaan rate card:

| Band | Pax | Nota |
|---|---|---|
| 5 Seater | 2&ndash;3 | |
| 8 Seater | 4&ndash;6 | |
| 12 Seater | 7&ndash;9 | |
| 21 Seater | 10&ndash;18 | rate card tulis **Sebut harga** &rarr; kalkulator papar cip merah `kadar?` |

Kadar tier pakej, peak RM 125/pax/malam, single supplement RM 2,500, infant
RM 1,000, upgrade 4&#9733; RM 125/pax/malam dan late booking RM 50 datang dari
**katalog** + tab Surcharge.

### Percanggahan yang masih terbuka

| Item | Katalog | Rate Card / KB | Dipakai kalkulator |
|---|---|---|---|
| Mornington Peninsula | 8 jam, RM 1,600 rata | **10 jam**, RM 2,550 / 2,950 / 3,500 | rate card |
| Puffing Billy & Dandenong | 8 jam, RM 1,500 rata | **10 jam**, RM 2,450 / 2,850 / 3,400 | rate card |
| Great Ocean Road | RM 2,800 rata | RM 3,350 / 3,750 / 4,300 | rate card |
| Winter Snow Trip | RM 3,200 rata | RM 3,500 / 3,900 / 4,450 | rate card |
| City Tour full-day | RM 1,500 rata | RM 2,300 / 2,700 / 3,250 | rate card |
| City Tour half-day | RM 800 rata | RM 1,450 / 1,750 / 2,200 | rate card |
| Late booking | p5: tiada jumlah | Surcharge KB: RM 50/**pax** &middot; R&D sheet: RM 50/**booking** | per booking |

Keputusan PO 2 Sep 2026: **rate card** untuk transport (satu sumber, konsisten
dengan Phillip Island / airport transfer / baris tolak yang memang sudah ikut
rate card), dan late booking kekal **per booking**.

**Katalog p3 masih tersiar harga rata yang lebih rendah** (contoh GOR RM 2,800
berbanding RM 3,350). Kalau katalog itu yang betul untuk customer, katalog perlu
dikemas kini &mdash; atau beritahu saya untuk tukar balik.

---|---|---|
| Airport transfer pick up tambahan | `airPick` | 1400 / 1700 / 2150 (2–3 / 4–6 / 7–9 pax) |
| Airport transfer drop off tambahan | `airDrop` | 1300 / 1600 / 2050 |
| Tolak airport transfer pick up | `airPickCut` | −1100 / −1300 / −1700 |
| Tolak airport transfer drop off | `airDropCut` | −1000 / −1200 / −1600 |
| Phillip Island 10 jam (hari extension) | `day` → `[Phillip Island]` | 2600 / 3000 / 3600 |
| Phillip Island + Penguin Parade 12 jam | `piPeng12` | 2950 / 3350 / 3900 |
| Free & Easy transport standby | `feStandby` | 500 / 650 / 1000 |
| Tolak Free & Easy transport standby | `feStandbyCut` | −300 / −500 / −700 |
| Tolak hari berpandu dari katalog | `dayDed` (ikut kawasan) | Basic: PI −2000/−2400/−2800, City −1800/−2100/−2600 · Std: PI −2300/−2600/−3100, GOR −2600/−3000/−3400 |
| Malam tambahan 3 bintang | `ext.night` | 300 normal / 450 peak (per pax/malam) |
| Malam tambahan 4 bintang | `hGrand`, `hPegasus` | 450 normal / 600 peak |
| Tolak malam pakej | `nightShort` | −200 per pax |
| Surcaj travel date 2027 | `extraSurcharge` | RM 100 per pax (1 Jan – 30 Jun 2027) |
| Lunch / dinner tambahan | `meals` | RM 100 per pax per hidangan |
| Tolak tiket Maru / Churchill / Penguin | `addons` | −85 / −45 / −85 per pax |

Kadar **bersumber** (jangan ubah tanpa katalog baharu): tier semua varian, peak
RM 125/pax/malam × 4 tetingkap, single supplement RM 2,500, infant RM 1,000,
late booking RM 50, upgrade 4 bintang RM 125/pax/malam, dan semua kadar hari ikut
kawasan kecuali Phillip Island (lihat jadual di bawah).

---

## ⚠ Dua soalan harga yang masih terbuka

Kedua-dua ini **tidak** diubah — ia perlu keputusan PO.

**1. Surcaj tarikh acara khas (Christmas / New Year / CNY) tidak dikira.**
Katalog p1 tulis *"Special Event Date Surcharge (e.g. Christmas/New Year/Chinese
New Year) not included – please enquire prior booking"* tanpa jumlah. Jadi quotation
untuk departure 24 Dis hanya kenakan peak RM 125/pax/malam, dan ayat tentang acara
khas hanya muncul dalam perenggan *Validity* di bawah. **Risiko: quote terkurang
harga untuk tarikh Christmas/NY.** Kalau PO ada jumlahnya, tambah sebagai
`extraSurcharge` dengan `dateIn` tetingkap Christmas/NY — kalkulator terus kira.

**2. Peak dikenakan dua kali pada malam tambahan?**
`ext.night` ada dua nilai — `normal: 300` dan `peak: 450`. Bila trip jatuh dalam
tetingkap peak, enjin kenakan RM 450 untuk malam tambahan itu **dan** juga peak
RM 125/pax/malam pada malam yang sama (contoh: 5 malam peak = RM 625 + malam
tambahan RM 450). Jadi malam tambahan naik dua kali: +150 (kadar peak) dan +125
(surcaj peak).

Kalau RM 450 itu memang bermaksud *kos penuh satu malam peak*, maka surcaj RM 125
tidak patut dikenakan lagi pada malam itu — betulkan dengan set `ext.night.peak`
kepada `300` (sama seperti normal), supaya hanya surcaj peak katalog yang terpakai.
Kalau RM 450 bermaksud *kos asas sebelum surcaj*, biarkan seperti sekarang.
Kadar 300/450 tiada sumber, jadi hanya PO boleh tentukan.

---

## Breakfast

Breakfast ialah pilihan dalam **dropdown Meals** setiap hari (bukan optional
activity), jadi ia dikira **per pax per malam** dan ikut bilangan malam sebenar.

| Pilihan | Kos | Guna bila |
|---|---|---|
| `Breakfast (termasuk pakej Standard)` | RM 0 | hari pakej Standard &mdash; breakfast sudah dalam harga katalog |
| `Breakfast buffet (tambahan)` | **RM 125 per pax per malam** | pakej **Basic** (Basic tiada breakfast), dan malam extension Standard |

Kadar diubah di satu tempat sahaja: `variants[].ext.rates.bfAdd`. Ada juga
gabungan dengan Lunch / Dinner untuk kedua-dua keluarga.

Basic **tiada** breakfast dalam katalog, jadi untuk Basic guna sentiasa
*Breakfast buffet (tambahan)*. Pilihan *termasuk pakej Standard* memang RM 0 &mdash;
ia untuk Standard.

---

## Hari tambahan &mdash; kenapa ada cip merah `kadar?`

Entri **Extension** dan **Custom (tulis sendiri)** sudah **dibuang** dari dropdown
Itinerary (`hideGeneric`), sebab kos hari generik belum pasti. Generik **Free & Easy**
enjin juga dibuang &mdash; ia bagi breakfast percuma dan melepaskan hari berpandu
tanpa tolakan; guna *Free & Easy - tolak driving guide dari katalog* atau
*Free & Easy + transport standby* yang sudah ada dalam pustaka.

Bila TC tekan **+ Tambah Hari**, hari itu bermula sebagai *Hari tambahan - pilih
blok day tour di bawah*: malam tambahan dikenakan, tetapi transport papar cip merah
`kadar?` sampai TC pilih satu blok day tour yang ada kadar katalog (Dandenong,
Mornington, Great Ocean Road, Snow, City Tour, Phillip Island).

Kalau nak hidupkan harga hari generik, isi `variants[].ext.rates.day._default`
(`"normal": null` &rarr; nombor). Rujukan tab Add-Ons R&D: Private Day Tour
5-seater RM 700, 7/8-seater RM 1,000, 12-seater RM 1,500 sehari &mdash; **belum
disahkan**, sebab itu ia dibiarkan kosong.

---

## Di mana benda yang biasa diubah

### Harga katalog (tier per pax)

`variants[].tiers` — `a` = adult, `c` = CWB (adult − 200), `n` = CNB (adult − 500).

```json
{"from": 4, "to": 4, "a": 4197, "c": 3997, "n": 3697}
```

Varian: `basic` PT Melbourne Basic 5D4N · `std` PT Melbourne Standard 5D4N.

### Kadar peak season

`peak` — `mode: perNight`, RM 125 per pax per **malam** yang jatuh dalam tetingkap.

```json
"peak": {"mode": "perNight", "value": 125,
  "windows": [["2026-09-20","2026-09-30"],
              ["2026-10-30","2026-11-08"],
              ["2026-12-01","2027-01-31"],
              ["2027-03-01","2027-04-12"]]}
```

### Kadar transport ikut kawasan

`variants[].ext.rates.day` — kunci kawasan → band pax. Ini yang menentukan kos bila TC
tambah hari dan pilih satu blok itinerary. Semua kadar ini **per transport** (satu
kenderaan dikongsi group), diambil dari halaman *ADD-ON PRIVATE DAY TOUR* katalog p3.

| Kawasan | Kadar | Ada pada varian |
|---|---|---|
| `_default` (Private Day Tour generik) | 700 / 1000 / 1500 ikut kelas kenderaan | kedua-dua |
| `[Dandenong]` Puffing Billy 8 jam | 1500 | kedua-dua |
| `[Mornington]` 8 jam | 1600 | kedua-dua |
| `[Snow]` Winter Snow Trip 12 jam | 3200 | kedua-dua |
| `[Great Ocean Road]` 12 jam | 2800 | **Basic sahaja** (Std sudah ada GOR pada D3) |
| `[Melbourne City]` full-day 10 jam | 1500 | **Standard sahaja** (Basic sudah ada city pada D3) |
| `[Melbourne City Half]` half-day 5 jam | 800 | **Standard sahaja** |
| `[Phillip Island]` 10 jam | 2600 / 3000 / 3600 | kedua-dua — ⚠ tiada sumber |

**11 pax ke atas sengaja tiada kadar.** WAE hanya quote sehingga 10 pax, jadi kalkulator
papar cip merah `kadar?` dan bukan RM 0 — quote manual dengan WAE. Kalau WAE sudah bagi
kadar 11+, tukar `"normal": null` kepada nombornya.

### Blok itinerary

`variants[].library` — senarai blok yang muncul dalam dropdown **Itinerary** setiap hari.
`g` = tajuk kumpulan dalam dropdown, `region` = kunci kadar transport di atas.
Basic ada 11 blok, Standard ada 12 (senarai berbeza kerana add-on setiap katalog berbeza).

### Add-on tiket

`addons` — `["Nama", hargaAdult, hargaChild, "pax"]`. Kuantiti diisi sendiri ikut pax.
Tour per-transport **bukan** add-on lagi — ia kini kadar hari ikut kawasan di atas,
supaya tiada dua jalan untuk kos yang sama (elak double-count).

---

## Nota

Repo ini public dan KB mengandungi harga dalaman serta analisis pesaing.
