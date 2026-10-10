# ARBA Krabi KB (TC Reference) — Simple Calculator

> **Mulai 9 Okt 2026 kandungan KB dan `calc-config.json` datang dari PT R&D Costing Hub** (`prod-at22/pt-rnd-hub`, `data/kb/krabi.json`). Fail di sini ditulis semula oleh mirror — **jangan edit di GitHub repo ini**; edit di hub. Skema di bawah masih terpakai.

Halaman live: **https://prod-at22.github.io/pt-kb-house/krabi/**

Repo ini ada dua fail yang penting:

| Fail | Apa dia | Boleh PO edit? |
|---|---|---|
| `calc-config.json` | **semua nombor dan itinerary kalkulator** — harga katalog, kadar peak, kadar malam tambah/tolak, kadar meal, blok itinerary, add-on | **Ya** — edit terus di sini |
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
dan papar notis merah di atas tab Simple Calculator, contoh:

> **Notis:** gagal guna calc-config.json (JSON tidak sah — Unexpected token …).
> Kalkulator sedang guna config terbenam (versi terakhir yang dibina), jadi angka
> mungkin bukan yang terbaru.

Kalau notis itu keluar, maksudnya **suntingan tak terpakai** — betulkan JSON dan commit
semula.

---

## Di mana benda yang biasa diubah

Varian: `budget` Krabi Budget 4D3N · `std` Krabi Standard 4D3N · `hny` Krabi Honeymoon 4D3N

### Harga katalog (tier per pax)

`variants[].tiers` — `a` = adult, `c` = CWB (3–11), `n` = CNB (3–7).
Katalog Krabi 2026 beri harga **rata untuk 2–10 pax**, jadi satu baris sahaja per varian:

```json
{"from": 2, "to": 10, "a": 1497, "c": 1297, "n": 1097}
```

> Ini **harga katalog**, bukan Tier 2. Diskaun Tier 2 (−RM200/pax) tidak dikira dalam
> kalkulator — tolak sendiri kalau quote guna Tier 2.
>
> Honeymoon RM2,897/pasangan ditulis sebagai `a` = `1448.5` (per pax), jadi 2 pax = RM2,897.

### Kadar peak season

`variants[].peak` — mod `flat`: satu amaun **rata per pax** untuk seluruh trip
(bukan per malam). Setiap tetingkap: `[mula, tamat, id_varian, kadar, label]`.

```json
"peak": {"mode": "flat", "value": 250, "windows": [
  ["2026-01-11", "2026-04-30", "std", 250, "High Season"],
  ["2026-12-01", "2026-12-31", "std", 300, "Year-End Peak"],
  ["2027-01-01", "2027-12-31", "std", "request", "Travel 2027 (luar tempoh katalog)"]
]}
```

Perhatian — tetingkap Year-End **tidak sama** antara varian, ikut katalog:
Budget & Honeymoon mula **1 Nov 2026**, Standard mula **1 Dis 2026**.

`"request"` (bukan nombor) = kalkulator tidak kenakan surcaj tetapi tandakan
"sebut harga" — dipakai untuk 2027 sebab katalog hanya sah hingga 31 Dis 2026.
Bila katalog 2027 keluar, tukar `"request"` kepada kadar sebenar.

### Kadar malam tambah / tolak (rate card operasi)

Rate card beri kadar **per bilik**; config simpan **per pax** (÷ 2, asas 2 pax sebilik).

`ext.night` = malam tambahan hotel 3 bintang dalam pakej:

```json
"night": {"normal": 125, "peak": 225}
```

`ext.rates` — kadar malam ikut hotel:

| Kunci | Hotel | per bilik (rate card) | per pax (config) |
|---|---|---|---|
| `ext.night` | 3 star (dalam pakej) | +250 / +450 peak | 125 / 225 |
| `n4` | 4 star Cha-Da / Heritage | +325 / +600 peak | 162.5 / 300 |
| `nBuri` | Aonang Buri | +250 / +500 peak | 125 / 250 |
| `nAva` | AVA Sea Aonang Resort | +325 / +520 peak | 162.5 / 260 |
| `nAnanta` | Anantaburin Resort | +280 / +600 peak | 140 / 300 |
| `nightShort` | tolak 1 malam pakej (3 star) | −80 / −100 peak | −40 / −50 |
| `upPrem` | Aonang Princeville | sebut harga | `0` → cip merah |
| `day` / `dayDed` | transport hari tambahan | **tiada kadar tersiar** | `0` → cip merah |

Kalau nak ubah kadar per bilik, **bahagi 2 dahulu** sebelum tulis dalam JSON.

Kadar `0` bermakna "tiada harga jual tersiar" — halaman papar cip merah `kadar?` pada
hari itu supaya TC sebut harga dengan operator, bukan quote RM 0. Isi nombornya di sini
bila operator dah bagi (contoh `day` untuk hari tambahan, `upPrem` untuk Princeville).

### Kadar meal tambah / tolak

`mealDelta` — per pax **per hidangan**, berbanding apa yang blok hari itu isytiharkan:

```json
"mealDelta": {"add": 55, "drop": 30}
```

Breakfast **neutral** — ia dipaksa oleh `variants[].breakfast: true` (semua pakej Krabi
termasuk breakfast hotel), jadi tukar dropdown meal tidak akan caj atau tolak breakfast.
Itu sepadan dengan rate card: breakfast "suggested makan di hotel sahaja", tiada kadar.

`meals` sengaja diset `{"lunch": 0, "dinner": 0}` supaya makan yang **sudah** ada dalam
harga katalog tidak dikira dua kali. Jangan tukar ini — guna `mealDelta`.

### Upgrade hotel pada malam pakej

Dalam `accOptions`, `perPax` = amaun rata per pax per malam:

```json
{"v": "up4", "t": "Upgrade 4 bintang &middot; Krabi Cha-Da / Krabi Heritage",
 "cost": "incl", "perPax": 240, "hotel": "4-Star Hotel"}
```

Semua tiga hotel 4 bintang (Cha-Da/Heritage, Aonang Buri, AVA Sea, Anantaburin) guna
+RM240/pax ikut R&D. Kalau katalog naikkan ke RM250, ubah `perPax` di keempat-empat.

### Blok itinerary

`variants[].itin[]` = itinerary default pakej — bilangannya **mesti** sama dengan `days`.
`library[]` = blok tambahan yang muncul dalam dropdown Itinerary setiap hari.

```json
{"v": "d3p", "region": "[Island SIC]",
 "t": "Phi Phi Island / Maya Bay (SIC speedboat)",
 "en": "PHI PHI ISLAND AND MAYA BAY TOUR",
 "acc": "incl", "meal": "l", "trp": "sic",
 "act": ["Via speedboat (sharing basis)", "Bamboo Island dan Maya Bay"],
 "eact": ["Via speedboat on sharing basis", "Bamboo Island and Maya Bay"]}
```

| Medan | Maksud |
|---|---|
| `v` | kunci unik — **jangan sama** dengan blok lain |
| `g` | kumpulan dalam dropdown (untuk `library[]` sahaja) |
| `region` | tag kawasan → menentukan kadar transport hari itu |
| `t` / `act` | nama & aktiviti **Bahasa Melayu** — dipapar pada baris hari dalam kalkulator |
| `en` / `eact` | nama & aktiviti **Bahasa Inggeris** — untuk PDF quotation |
| `acc` / `meal` / `trp` | pilihan default bila blok ini dipilih |

Kod `meal`: `nobf` (hari ketibaan, tiada breakfast) · `none` (breakfast sahaja) ·
`l` lunch · `d` dinner · `ld` lunch + dinner · `cld` candlelight dinner.

> Kalau nak tulis simbol `&` dalam `t`, `en`, `act`, `eact`, `inclusions`,
> `exclusions` — tulis `&` biasa sahaja, jangan `&amp;`.

### Add-on / optional activity

`addons[]` — `["Nama", hargaAdult, hargaChild]`. Nama ini masuk PDF quotation, jadi
**tulis dalam Bahasa Inggeris**. Kuantiti diisi sendiri ikut bilangan pax.

### Lain-lain

| Nak ubah | Di mana |
|---|---|
| Single supplement (RM450/pax) | `variants[].single` |
| Harga infant (FOC) | `variants[].infant` |
| Deposit per pax (RM250) | `deposit` |
| Late booking surcharge (RM50/booking, <45 hari) | `lateBooking` |
| Inclusions / exclusions PDF | `variants[].inclusions`, `exclusions`, `exclusionsTail` |
| Teks bawah PDF quotation | `validity` |
| Nota ikut saiz group | `paxNotes[]` |
| Teks pengenalan atas kalkulator | `intro` |

`"{auto}"` dalam `inclusions` = baris itinerary dijana sendiri daripada hari yang
dibina, jadi ia tidak jadi basi bila TC tukar hari. Jangan buang penanda itu.

---

## Yang masih perlu dibina semula (bukan dalam JSON)

- Isi tab lain: FAQ, Harga & Pakej, **Simple Customisation**, Surcharge, Transport,
  Accommodation, Flight, FreeGift
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

## Percanggahan sumber yang belum disahkan

Kalkulator ikut nombor di sebelah **kiri**. Sahkan dengan operator, kemudian betulkan
`calc-config.json`.

| Perkara | Dipakai | Bercanggah dengan |
|---|---|---|
| Upgrade 4 bintang | RM240/pax (R&D Surcharges + baris atas katalog) | katalog Basic & Standard p1 juga tulis "Upgrade 4 Star Hotel : RM250/person" |
| Aonang Princeville | sebut harga (`0`, cip merah) | R&D Hotels tulis +500, nota Costing tulis +700, KB tulis 500–700 anggaran |
| Peak Year-End Standard | 1 Dis – 31 Dis 2026 | Basic & Honeymoon tulis 1 Nov – 31 Dis |
| Peak amaun | +RM250 / +RM300 per pax (katalog + R&D) | rate card kongsi dalam tab Surcharge tulis +RM150/pax (CNY, Songkran, Christmas) dan +RM80/pax/malam untuk Nov–Dis 2026 |
| Honeymoon | RM2,897/pasangan ÷ 2 = RM1,448.50/pax | katalog HNY p1 ada sel "7-15  RM 857" yang tidak jelas maksudnya |
| Kadar malam | per bilik ÷ 2 (asas 2 pax sebilik) | katalog benarkan 2–3 pax sebilik, jadi bilik triple akan over-charge sedikit |

---

*Sumber nombor: katalog PT Krabi Basic v2 / Standard v1 / Honeymoon v3 (last updated
7 Aug 2026), `PT KRABI R&D - reformatupload.xlsx` (tab Costing / Surcharges / Add-Ons /
Hotels), dan rate card operasi Tambah/Tolak Malam & Meal (PO, 3 Sep 2026).
Repo ini public — ia mengandungi harga dalaman.*
