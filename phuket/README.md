# PT Phuket KB — Simple Calculator

> **Mulai 9 Okt 2026 kandungan KB dan `calc-config.json` datang dari PT R&D Costing Hub** (`prod-at22/rnd-hub`, `data/kb/phuket.json`). Fail di sini ditulis semula oleh mirror — **jangan edit di GitHub repo ini**; edit di hub. Skema di bawah masih terpakai.

Halaman live: **https://prod-at22.github.io/pt-kb-house/phuket/**

Repo ini ada dua fail yang penting:

| Fail | Apa dia | Boleh PO edit? |
|---|---|---|
| `calc-config.json` | **semua nombor dan itinerary kalkulator** — harga tier, kadar peak, malam tambahan, add-on, meal, inclusions | **Ya** — edit terus di sini |
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

Kalau JSON tersalah tulis (koma tertinggal, kurungan tak tutup), halaman **tidak**
rosak. Ia guna balik config lama yang terbenam dalam `index.html` dan papar notis
merah di atas tab Simple Calculator. Kalau notis itu keluar, maksudnya **suntingan
tak terpakai** — betulkan JSON dan commit semula.

---

## Empat varian pakej

Upgrade hotel 4 bintang ialah **+RM 300/pax sekali** untuk keseluruhan pakej (bukan
per malam), jadi ia jadi varian tersendiri dan bukan pilihan harian:

| `id` | Pakej | Adult | CWB | CNB |
|---|---|---|---|---|
| `std3` | Standard 4D3N · 3★ | 1,797 | 1,597 | 1,397 |
| `std4` | Standard 4D3N · 4★ | 2,097 | 1,897 | 1,697 |
| `bsc3` | Basic 4D3N · 3★ | 1,397 | 1,197 | 997 |
| `bsc4` | Basic 4D3N · 4★ | 1,697 | 1,497 | 1,297 |

**Kalau harga asas berubah, ubah KEDUA-DUA varian.** `std4` mesti sentiasa
`std3 + 300`, dan `bsc4` mesti `bsc3 + 300`.

### Harga katalog (tier per pax)

`variants[].tiers` — `a` = adult, `c` = CWB (child with bed), `n` = CNB (child no bed).

```json
{"from": 2, "to": 10, "a": 1797, "c": 1597, "n": 1397}
```

Katalog hanya siarkan tier 2–10 pax. 11 pax ke atas guna tier terakhir dan kalkulator
papar nota "sebut harga operasi".

---

## Malam tambahan & tolak malam — dikira PER BILIK

Rate card operasi bagi kadar **per bilik per malam**, tetapi enjin kalkulator caj
malam secara per pax. Jadi ia dimodelkan sama seperti Bangkok:

1. **Dropdown Accommodation** hanya *menanda* hari itu — `Malam tambahan 3★`,
   `Malam tambahan 4★`, atau `Tanpa hotel – tolak malam pakej`. Tanda ini yang
   betulkan lajur Accommodation dan baris inclusions dalam PDF. Ia **tidak berkos**.
2. **Kosnya datang dari add-on**, dan TC isi **bilangan bilik** dalam kotak kuantiti:

| Add-on | Kadar |
|---|---|
| `Additional night, 3-Star Hotel - per room` | RM 265 / bilik / malam |
| `Additional night, 4-Star Hotel - per room` | RM 330 / bilik / malam |
| `Package night removed - per room` | −RM 150 / bilik / malam |

Untuk ubah kadar ini: `addons[]`, elemen **kedua** setiap baris.

> Rate card hanya beri kadar **normal** — tiada kadar malam tambahan waktu peak.
> Kalau operasi bagi kadar peak kemudian, tambah dua add-on baharu (`... PEAK - per room`).

---

## Meal

`mealDelta` — kadar per pax **per hidangan** berbanding apa yang blok itinerary itu
sendiri isytiharkan:

```json
"mealDelta": {"add": 80, "drop": 50}
```

Breakfast **neutral**: ia komponen bilik, jadi tukar antara *Breakfast sahaja* dan
*Tiada meal* tidak menambah atau mengkredit apa-apa. Itu sepadan dengan rate card
(breakfast: cadang makan di hotel, tiada harga tolak).

`meals` sengaja `{"lunch": 0, "dinner": 0}` — kalau diisi, setiap lunch pakej akan
dicaj dua kali.

---

## Tolak day tour

Pilihan **Transport** → `Tolak 1 day tour dari pakej` = −RM 50/pax
(`trpOptions[].perPax`).

Ikut nota rate card: lunch sudah termasuk dalam island package, jadi kalau customer
tak nak pergi island, **tukar juga Meal hari itu ke `Breakfast sahaja`** supaya
lunchnya (−RM 50/pax) ditolak sekali. Kalkulator tidak buat ini automatik — dua
tindakan berasingan, sebab customer boleh drop tour tapi kekalkan lunch.

Rate card **tiada** harga tambahan day tour. Jadi blok `Hari tambahan - day tour`
sengaja papar cip merah **kadar?** dan tidak menambah RM apa-apa. Itu betul — dapatkan
sebut harga operasi. Kalau operasi bagi kadar, isi `ext.rates.day._default`.

---

## Kadar peak season

`peak.mode` ialah `"flat"` — satu amaun rata per pax untuk keseluruhan trip, bukan
per malam. Setiap tetingkap: `[mula, tamat, id varian, kadar, label]`.

```json
["2026-12-21", "2027-01-10", "std3", 300, "Peak Season"]
```

Setiap tetingkap didaftarkan **dua kali**, sekali untuk varian 3★ dan sekali untuk 4★.
Kalau tambah tetingkap baharu, jangan lupa pasangannya.

| Varian | Tetingkap | Kadar |
|---|---|---|
| Standard | 21 Dis 2026 – 10 Jan 2027 | RM 300/pax |
| Standard | 11 Jan – 30 Apr 2027 | RM 250/pax |
| Basic | 1 Nov – 31 Dis 2026 | RM 300/pax |
| Basic | 11 Jan – 30 Apr 2026 | RM 250/pax |
| Basic | 11 Jan – 30 Apr 2027 | RM 250/pax |
| Kedua-dua | Mei – Jun | tiada surcharge |

> **PERLU DISAHKAN PO.** Katalog Basic cetak tetingkap kedua sebagai
> **11 Jan – 30 Apr 2026**, yang sudah lepas. Katalog Standard cetak tetingkap
> setara sebagai **2027**. Kedua-dua tahun dimasukkan: yang 2026 kekal setia pada
> cetakan katalog, dan yang 2027 ditambah supaya departure Basic Jan–Apr 2027 tidak
> terlepas surcaj. **Kalau 2026 memang betul, buang dua baris `bsc3`/`bsc4` yang
> bertarikh 2027.**

---

## Itinerary & pustaka blok

`variants[].itin[]` = itinerary default (bilangannya **mesti** sama dengan `days`).
`library[]` = blok tambahan dalam dropdown Itinerary.

| Medan | Maksud |
|---|---|
| `v` | kunci unik |
| `g` | kumpulan dalam dropdown |
| `t` / `act` | nama & aktiviti **Bahasa Melayu** (dipapar dalam kalkulator) |
| `en` / `eact` | nama & aktiviti **Bahasa Inggeris** (untuk PDF quotation) |
| `acc` / `meal` / `trp` | pilihan default bila blok ini dipilih |

Blok `b3pp` (Hari 3 Phi Phi, +RM 100/pax) hanya ada dalam
`variants[].library` bagi `bsc3` dan `bsc4` — varian Standard sudah ada Phi Phi
sebagai Hari 3.

> Kalau nak tulis simbol `&` dalam `t`, `en`, `act`, `eact`, `inclusions`,
> `exclusions`, atau nama add-on — tulis `&` biasa sahaja, **jangan** `&amp;`,
> `&mdash;` atau `&#9733;`. Medan itu dipapar sebagai teks, bukan HTML.

---

## Lain-lain

| Nak ubah | Di mana |
|---|---|
| Upgrade Phi Phi Basic (+RM 100/pax) | `trpOptions[]` → `ppup` → `perPax` |
| Single supplement Standard (RM 450) | `variants[].single` |
| Deposit per pax (RM 250) | `deposit` |
| Late booking (RM 50/booking) | `lateBooking` |
| Tiket Aquaria / Andamanda | `addons[]` |
| Inclusions / exclusions PDF | `variants[].inclusions`, `exclusions`, `exclusionsTail` |
| Teks bawah PDF quotation | `validity` (Bahasa Inggeris — ia masuk PDF customer) |
| Nota ikut saiz group | `paxNotes[]` |

---

## Perkara yang kalkulator TIDAK caj

- **Single supplement Basic** — katalog tulis *quoted upon request*, jadi kalkulator
  caj RM 0. Dapatkan kadar dari operasi dahulu sebelum quote bilik single Basic.
- **Harga tambahan day tour** — tiada dalam rate card (lihat di atas).
- **Buang hari tanpa menanda** — kalau TC buang satu hari tetapi tidak pilih
  `Tanpa hotel – tolak malam pakej` pada hari lain, tiada tolakan dikira. Tanda hari
  itu dan isi add-on bilik.
- **Banana boat / parasailing Coral Island** — katalog tulis RM 67–87 dan RM 157–197,
  bayar sendiri tunai di pulau (own expenses), jadi ia tidak masuk quotation.

---

## Yang masih perlu dibina semula (bukan dalam JSON)

- Isi tab lain: FAQ, Harga & Pakej, Simple Customisation, Surcharge, Travel Map,
  Accommodation, dan lain-lain
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

*Sumber nombor: katalog `PT PHUKET STANDARD 4D3N 2026 v2.pdf` dan
`PT PHUKET BASIC 4D3N 2026 v2.pdf` (last updated 5 Ogos 2026), serta rate card
operasi PT Phuket (accommodation / meals / day tour).
Repo ini public — ia mengandungi harga dalaman.*
