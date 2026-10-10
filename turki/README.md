# PT Turki KB — Simple Calculator

> **Mulai 9 Okt 2026 kandungan KB dan `calc-config.json` datang dari PT R&D Costing Hub** (`prod-at22/pt-rnd-hub`, `data/kb/turki.json`). Fail di sini ditulis semula oleh mirror — **jangan edit di GitHub repo ini**; edit di hub. Skema di bawah masih terpakai.

Halaman live: **https://prod-at22.github.io/pt-kb-house/turki/**

Repo ini ada dua fail yang penting:

| Fail | Apa dia | Boleh PO edit? |
|---|---|---|
| `calc-config.json` | **semua nombor dan itinerary kalkulator** — harga tier, peak, kadar transport 17 segmen, blok itinerary, add-on, surcaj | **Ya** — edit terus di sini |
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
semula. Semakan yang dibuat: JSON sah, ada `variants`, setiap varian ada `tiers` penuh
(`from`,`to`,`a`,`c`,`n`), dan bilangan hari dalam `itin` sama dengan `days`.

---

## Di mana benda yang biasa diubah

### Harga katalog (tier per pax)

`variants[].tiers` — `a` = adult, `c` = CWB, `n` = CNB.

```json
{"from": 4, "to": 4, "a": 6397, "c": 6197, "n": 5997}
```

Varian: `klasikstd` Turki Klasik STANDARD 8D7N · `klasikbasic` Turki Klasik BASIC 8D7N ·
`istcap` Istanbul–Cappadocia 6D5N · `istbur` Istanbul–Bursa 5D4N.

### Kadar peak season

Turki guna model **peratus** (bukan RM per malam) — dikenakan **sekali** atas harga tier
adult bila ada mana-mana malam jatuh dalam tetingkap peak.

```json
"peak": {"mode": "percent", "value": 10,
         "windows": [["2026-09-01","2026-11-30","klasikstd"],
                     ["2026-12-20","2027-01-01","klasikstd"]]}
```

Elemen **ketiga** = had kepada satu varian sahaja (`null` = semua varian).
Elemen **keempat** (pilihan) = kadar % khas untuk tetingkap itu.
Nak tambah tetingkap baharu: tambah satu baris dalam `windows`.

### Kadar transport ikut segmen rate card

`ext.rates.day` — kunci = segmen rate card, nilai = band saiz kenderaan.
**Band 1–7 = Vito · band 8–16 = Sprinter/Crafter.**

```json
"[Istanbul Day Tour]": [{"from":1,"to":7,"normal":5000,"peak":5000},
                        {"from":8,"to":16,"normal":12300,"peak":12300}]
```

17 segmen ada di sini — sama persis dengan jadual *Transport + Driver* dalam tab
**Simple Customisation → Raw Costing — Rate Card Operator**. Kadar adalah
**per kenderaan**, bukan per pax (enjin darab dengan bilangan kenderaan sendiri).

> **Tiada `_default` dengan sengaja.** Hari komposit (contoh *Cappadocia – Konya –
> Pamukkale* = dua segmen) memang tiada satu kadar tersiar, jadi halaman papar cip
> merah `kadar?` pada hari itu. Itu gap yang **kelihatan** — lebih selamat daripada
> satu kadar rata yang menyembunyikannya. Jangan tambah `_default` melainkan operator
> memang bagi satu kadar rata.

Kunci lain dalam `ext.rates`:

| Kunci | Maksud |
|---|---|
| `dayDed` | lajur **Tolak** rate card — dipakai bila hari berpandu jadi free & easy |
| `nightShort` | tolak per pax bila malam kurang dari pakej (−150 normal / −200 peak) |
| `up4` | upgrade hotel 4 bintang per malam (200 normal / 300 peak) |
| `up5` | upgrade hotel 5 bintang per malam (400 normal / 500 peak) |

`ext.night` = malam tambahan hotel 3 bintang (300 normal / 400 peak, per pax).

`ext.autoNights` = biar `true`. Bilangan malam dikira daripada **panjang perjalanan**:
`n hari = n-1 malam`, tolak malam yang TC sengaja buang (pilihan *Tanpa hotel*).
Jadi tambah hari, salin hari, atau tarik return date — semuanya terus mengenakan
malam hotel dengan betul. Jangan letak `perPaxRate` pada pilihan *Tanpa hotel*:
enjin sudah tolak malam itu, dan menambah `perPaxRate` akan tolak dua kali.

`ext.shareVehicle` = biar `true`. Kos per kenderaan (transport segmen + tour guide)
ialah kos yang **dikongsi seluruh group**, jadi ia dibahagi dengan bilangan pax
berbayar dan dilipat ke **harga per pax**. Kesannya: harga per pax dalam ringkasan
ialah harga akhir sebenar, dan tab kalkulator memaparkan **breakdown** baris demi
baris (harga katalog → setiap segmen transport / guide / peak / surcaj → harga final
per pax) supaya TC boleh audit angka itu tanpa mengira sendiri. Setiap baris transport
menyebut segmennya dan jumlah kumpulan sebelum dibahagi, contoh
`Transport [Konya Tour] (1 hari x 1 kenderaan, RM 6,550 / 9 pax) +RM 728`.

### Transport vs tour guide — Turki tidak membundelkan

Kadar `ext.rates.day` ialah **transport + driver sahaja**. Tour guide RM 480/hari
(per group) dicaj berasingan:

| Pilihan Transport | Apa yang dikira |
|---|---|
| `ext` Private Transport + Driver | kadar segmen sahaja |
| `extg` + Tour Guide | kadar segmen **+ RM 480** |
| `guide` Tour Guide sahaja | RM 480 sahaja |
| `ded` Tolak transport dari pakej | kadar `dayDed` segmen itu (negatif) |

Hari yang TC tambah sendiri default kepada `ext` (`extDefaults.trp`). Kalau nak
default terus bersama guide, tukar `"extDefaults": {"trp": "extg"}`.

### Blok itinerary

`library[]` — senarai blok yang muncul dalam dropdown Itinerary setiap hari.

```json
{"v": "sg_konyatour", "g": "Day Tour", "region": "[Konya Tour]",
 "t": "Konya Tour", "en": "KONYA TOUR",
 "acc": "incl", "meal": "b", "trp": "incl",
 "act": ["Sultanhani Caravanserai", "Mevlana Museum"],
 "eact": ["Sultanhani Caravanserai", "Mevlana Museum"]}
```

| Medan | Maksud |
|---|---|
| `v` | kunci unik — **jangan sama** dengan blok lain |
| `g` | kumpulan dalam dropdown (Transfer Airport · Day Tour · Pemanduan Antara Bandar · Umum) |
| `region` | tag segmen → menentukan kadar transport hari itu |
| `t` / `act` | nama & aktiviti **Bahasa Melayu** — dipapar pada baris hari |
| `en` / `eact` | nama & aktiviti **Bahasa Inggeris** — untuk PDF quotation |
| `acc` / `meal` / `trp` | pilihan default bila blok ini dipilih |

**Kenapa `trp` blok pustaka ialah `incl`, bukan `ext`:** supaya menukar blok pada hari
yang memang sudah berpandu dalam pakej = **RM 0** (harga katalog dah termasuk). Enjin
tukar sendiri kepada pilihan berkos bila hari itu hari tambahan, atau bila hari yang
tiada transport ditukar kepada blok berpandu. Kalau `trp` ditulis `ext`, setiap swap
akan tersalah caj.

Blok hari **berlepas** (`sg_istanbul_iga_out`, `sg_istanbul_saw_out`) bawa `acc:"none"`
supaya menukar hari checkout tidak menambah malam secara senyap.

`variants[].itin[]` = itinerary default pakej. Bentuknya sama, dan bilangannya
**mesti** sama dengan `days`.

> Kalau nak tulis simbol `&` dalam `t`, `en`, `act`, `eact`, `inclusions`,
> `exclusions` — tulis `&` biasa sahaja, jangan `&amp;`.

### Extension & Custom sengaja dibuang

Dua entri generik &mdash; *Extension - hari tambahan* dan *Custom (tulis sendiri)* &mdash;
**tidak** ada dalam dropdown Itinerary Turki (`"hideGeneric": ["ext","cus"]`). Sebabnya
kedua-duanya hari tanpa segmen rate card, jadi kos transportnya tidak boleh dijamin, dan
*Custom* mengenakan RM 0 secara senyap.

Ganti: satu placeholder **`- Pilih blok segmen rate card -`** (blok `ext` dalam `library`,
bertanda `"mustPick": true`). Bila TC tekan **+ Tambah Hari**, hari baharu bermula pada
placeholder ini:

- malam hotel **tetap dikira** (RM 300/400 per pax) &mdash; panjang trip yang menentukannya
- transport **RM 0** sampai TC pilih blok segmen sebenar
- baris hari papar cip merah **`pilih blok`** dan ringkasan papar amaran, jadi hari yang
  belum berlabuh tidak boleh terlepas senyap ke dalam quotation

Nak benarkan semula Extension/Custom: buang `"ext"` / `"cus"` dari senarai `hideGeneric`.

### Tambah / tolak meal &mdash; `mealDelta`

```json
"meals": {"lunch": 0, "dinner": 0},
"mealDelta": {"add": 45, "drop": 30}
```

`meals` kekal **0** &mdash; kalau tidak enjin akan caj setiap lunch/dinner dalam itinerari,
termasuk yang sudah ada dalam harga katalog (double-count).

`mealDelta` mengenakan kadar rate card hanya pada **perbezaan** antara meal yang TC pilih
dan meal yang **blok itinerary itu sendiri** isytiharkan:

| Tindakan pada satu hari | Kesan |
|---|---|
| Biar seperti blok | RM 0 &mdash; tiada double-count |
| Tambah hidangan | `add` RM 45 per pax per hidangan |
| Buang hidangan | `drop` RM 30 per pax per hidangan |

Kadar memang **tidak simetri** (tambah 45, tolak 30) &mdash; itu ikut rate card operator.
Baseline ialah `meal` blok itu, bukan indeks hari, jadi ia kekal betul walaupun hari
disusun semula, ditambah atau dibuang.

> Bilangan **breakfast** dalam inclusions PDF ikut `{nights}` (breakfast dihidang pagi
> selepas setiap malam), bukan dropdown meal &mdash; itu padan katalog (`7x Breakfast` untuk
> 7 malam). Lunch dan dinner pula ikut dropdown. Kalau nak breakfast ikut dropdown juga,
> tukar `{nights} breakfasts` dalam `inclusions` kepada nombor tetap.

### Setiap tambah/tolak diflagkan pada baris hari

Setiap pelarasan pada satu hari muncul sebagai **cip berasingan** pada baris hari itu,
lengkap dengan amaunnya &mdash; jadi TC boleh lihat item mana sudah ditolak dan mana belum,
bukan sekadar satu jumlah bersih:

```
Tolak 2 meal -RM 60/pax  ·  -RM 120
4-Star hotel upgrade +RM 200/pax  ·  +RM 400
Transport [Konya Tour]  ·  +RM 2,800
Tolak 1 malam pakej -RM 150/pax  ·  -RM 300     <- bergaris putus-putus
```

Cip **bergaris putus-putus** bermaksud amaun itu dikira di peringkat **keseluruhan trip**
(contoh tolakan malam), bukan pada hari itu &mdash; ia dipapar di sana supaya tidak
terlepas pandang, tetapi tidak dikira dua kali.

### Add-on / optional activity

`addons[]` — `["Nama", hargaAdult, hargaChild, asas]`.

- `asas` `"pax"` → kuantiti diisi sendiri ikut bilangan pax
- `asas` `"unit"` → kuantiti 1 (kos per hari / per transport, contoh Tour Guide RM 480)
- Letak `0` untuk harga kanak-kanak kalau tiada — kuantiti kanak jadi 0 automatik

Nama ini masuk PDF quotation, jadi **tulis dalam Bahasa Inggeris**.

### Lain-lain

| Nak ubah | Di mana |
|---|---|
| Single supplement | `variants[].single` (RM 1,000 flat) |
| Harga infant | `variants[].infant` |
| Deposit per pax | `deposit` |
| Late booking surcharge | `lateBooking` (lead < 45 hari → RM 50 sekali) |
| Surcaj travel 2027 / winter | `extraSurcharge[]` |
| Harga lunch / dinner | `meals` — **biar 0**; harga katalog Turki sudah termasuk makan. Tambah/tolak meal guna add-on. |
| Inclusions / exclusions PDF | `variants[].inclusions`, `exclusions`, `exclusionsTail` |
| Teks bawah PDF quotation | `validity` |
| Nota ikut saiz group | `paxNotes[]` (kapasiti Vito/Sprinter, guide berasingan) |
| Teks pengenalan tab | `intro` |

---

## Yang masih perlu dibina semula (bukan dalam JSON)

- Isi tab lain: FAQ, Harga & Pakej, Surcharge, Transportation & Guide, Accommodation, dan lain-lain
- Logik enjin kalkulator (cara ia mengira)
- Susun atur / warna
- "Last updated" pada topbar

---

## Perlu disahkan dengan operator

- **`[Istanbul <-> Ankara]` Sprinter RM 37,000** — jauh lebih tinggi daripada segmen
  lain (Ankara ↔ Cappadocia RM 16,800 untuk jarak serupa). Dalam rate card asal baris
  ini bertajuk sama seperti *Istanbul Day Tour*; ia dipadankan sebagai
  Istanbul ↔ Ankara ikut susunan baris. Sahkan sebelum quote group besar.
- **Kapasiti dalam Istanbul** — Sprinter/Crafter max 13 pax dalam Istanbul, max 16 pax
  luar Istanbul. Band `8–16` tidak boleh bezakan ini sendiri; `paxNotes` memberi amaran
  pada 14–16 pax.
- **Segmen yang tiada dalam rate card** — *Istanbul ↔ Bolu*, *Cappadocia Day Tour*,
  *Pamukkale ↔ Bursa*. Hari pakej yang guna laluan ini akan papar `kadar?` bila
  ditanda sebagai hari tambahan.

---

## PENTING — elak kerja PO ditimpa

Selepas PO mula edit `calc-config.json` di sini, **fail ini jadi sumber sebenar**.
Kalau halaman dibina semula dari config lama, suntingan PO akan hilang.

Jadi bila minta apa-apa perubahan pada enjin atau tab lain, sebut sekali:
**"config sudah diedit dalam GitHub, ambil versi terbaru dari repo dahulu."**

---

*Sumber nombor: katalog PT TURKI CLASSIC BASIC & STD 8D7N 2026, PT Istanbul+Cappadocia
6D5N v5, PT ISTANBUL-BURSA 5D4N v4, dan rate card operator (Transport + Driver, Tour
Guide, Accommodation, Meals) seperti disiarkan dalam tab Simple Customisation KB.
Turki **tiada** fail ProdReq — kadar transport ikut segmen datang dari rate card
operator itu. Repo ini public — ia mengandungi harga dalaman.*
