# KB KK–Kundasang (TC Reference) + Simple Calculator

> **Mulai 9 Okt 2026 kandungan KB dan `calc-config.json` datang dari PT R&D Costing Hub** (`prod-at22/pt-rnd-hub`, `data/kb/kk-kundasang.json`). Fail di sini ditulis semula oleh mirror — **jangan edit di GitHub repo ini**; edit di hub. Skema di bawah masih terpakai.

Halaman rujukan dalaman untuk Travel Consultant PT KK–Kundasang, termasuk tab
**Simple Calculator** yang mengira quotation dan menjana PDF quotation format ARBA.

| Fail | Guna |
|---|---|
| `index.html` | KB penuh + kalkulator. Ini yang disajikan sebagai halaman. |
| `calc-config.json` | **Semua harga kalkulator ada di sini.** Edit fail ini untuk tukar kadar. |

Kalkulator membaca `calc-config.json` pada masa runtime, jadi **PO boleh ubah harga
tanpa bina semula KB**. Edit fail itu di GitHub, commit, tunggu ~30 saat, refresh.
Kalau JSON rosak, kalkulator jatuh balik ke config terbenam dan papar notis merah —
jadi kesilapan tidak akan menyebabkan harga salah secara senyap.

## Sumber harga

| Sumber | Untuk apa |
|---|---|
| Katalog `PAKEJ SABAH 3D2N (3 STAR) 2026 v3.pdf` | tier 3D2N, surcharge, add-on, itinerary |
| Katalog `PT SABAH 4D3N (3 STAR) 2026 v3.pdf` | tier 4D3N, surcharge, add-on, itinerary |
| Rate Card Operasi KB — Kota Kinabalu / Kundasang | kadar tambah & tolak transport, hotel, meal, entrance |

Kedua-dua katalog: *last updated 1 Julai 2026*, sah hingga **31 Disember 2026**.

**Keputusan PO (3 Sept 2026):** bila katalog v3 dan rate card bercanggah,
**katalog v3 menang** — untuk harga add-on customer-facing dan untuk surcharge/polisi.
Rate card dipakai untuk kadar tambah/tolak yang katalog tidak siarkan.

## Medan mana nak diubah dalam `calc-config.json`

### Harga pakej (tier)

`variants[].tiers[]` — satu baris per band pax:

```json
{"from": 3, "to": 4, "a": 957, "c": 857, "n": 757}
```

`a` = adult (11 tahun ke atas) · `c` = Child With Bed (7–10) · `n` = Child No Bed (3–6).
`variants[0]` = 3D2N Basic, `variants[1]` = 4D3N Standard.

### Single supplement

`variants[].single` — 3D2N `300`, 4D3N `450`.

### Peak season

```json
"peak": {"mode": "perNight", "value": 40, "windows": [["2026-07-15","2026-08-20"], ...]}
```

`value` = RM per pax per malam (hotel 3 bintang). Tambah/buang tetingkap dalam
`windows` sebagai `["mula","tamat"]`, format `YYYY-MM-DD`. Tarikh tamat **termasuk**.

Peak untuk hotel yang dinaik taraf lebih tinggi (3.5★ RM60, 4★ RM90). Ia tidak
diletak dalam `peak` — ia masuk melalui pilihan `up35pk` / `up4pk` dalam
`accOptions` (lihat bawah).

### Surcaj travel 2027

`extraSurcharge[0].perPax` — `100`, dikenakan bila **departure date** antara
1 Jan dan 30 Jun 2027.

### Late booking & deposit

`lateBooking` = `{"lt": 45, "amount": 50}` — RM50 per booking kalau tempahan kurang
45 hari sebelum berlepas. `deposit` = `250` per pax.

### Kadar transport (per kenderaan)

Semua dalam `ext.rates`. Setiap kunci ada band pax mengikut kelas kenderaan:
**1–4** Avanza/Innova · **5–8** Van 8 Seater · **9–16** Van 16 Seater · **17–99** tiada kadar.

| Kunci | Maksud |
|---|---|
| `day` | Full Day Tour 12 jam, ikut kawasan. `[Kudat]` 600/750/850, `[Mari-Mari]` 180/250, lain 280/380/500 |
| `dayDed` | tolak Full Day Tour dari katalog (nilai negatif) |
| `athd` / `athdDed` | Airport Transfer + Half Day Tour 6 jam, tambah / tolak |
| `atkk` / `atkkDed` | Airport Transfer ↔ KK Town |
| `atkds` / `atkdsDed` | Airport Transfer ↔ Kundasang |

`"normal": null` bermakna **kadar itu tiada dalam rate card**. Kalkulator akan papar
cip merah `kadar?` dan baris amaran, bukan mengenakan RM 0. Isi nilainya bila operasi
beri kadar — itu sahaja yang perlu.

### Kadar hotel (per pax per malam)

Juga dalam `ext.rates`, satu kunci per hotel-bilik, dengan `normal` dan `peak`:

| Awalan | Maksud |
|---|---|
| `nKpr…` `nCel…` | malam tambahan Kundasang (Kinabalu Pine Resort, Celyn Resort) |
| `nMg…` `nDt…` `nPm…` | malam tambahan Kota Kinabalu (Ming Garden, Dreamtel, Promenade) |
| `dKpr…` `dMg…` `dDt…` `dPm…` | tolak 1 malam pakej (nilai negatif) |

Celyn Resort **tiada kadar tolak** dalam rate card, jadi tiada kunci `dCel…`.

### Naik taraf kelas hotel

Dalam `accOptions`, medan `perPax`:

| `v` | Maksud | RM/pax/malam |
|---|---|---|
| `up35` | 3.5★ Kundasang (Perkasa / Dreamworld), malam normal | 80 |
| `up35pk` | sama, malam peak — 80 + beza peak (60−40) | 100 |
| `up4` | 4★ Kota Kinabalu (Promenade / Palace), malam normal | 150 |
| `up4pk` | sama, malam peak — 150 + beza peak (90−40) | 200 |

Kalau `peak.value` atau kadar peak katalog berubah, `up35pk` / `up4pk` **kena dikira
semula**: `perPax = kadar upgrade + (peak kelas itu − peak 3 bintang)`.

### Meal

`mealDelta` = `{"add": 40, "drop": 30}` — per pax **per hidangan**, bila TC menambah
atau membuang hidangan berbanding apa yang blok itinerary itu isytiharkan. Tiada
perubahan = RM 0, jadi tiada double-count dengan harga katalog.

Hidangan tertentu (Dinner Dream World, Kampung Nelayan, Candle Light Dinner, dll.)
ada dalam `addons` pada harga tersiarnya sendiri.

### Add-on

`addons[]`, setiap entri `["Nama Inggeris", hargaAdult, hargaKanak, basis, frasaEn]`:

- `basis` — `"pax"` (darab bilangan pax) · `"unit"` (satu unit) · `"share"` (kos satu
  group, dibahagi antara pax).
- Nama dipapar **terus dalam PDF quotation**, jadi tulis dalam Bahasa Inggeris.
- Harga **negatif** = tolakan (contoh buang entrance yang sudah ada dalam pakej).
  Untuk add-on negatif, elemen ke-5 wajib: nama tiket dalam Bahasa Inggeris, supaya
  kalkulator boleh membuang baris `inclusions` yang sepadan dan menambahnya ke
  `exclusions`.

## Yang masih perlu disahkan PO

1. **Mari-Mari Cultural Village Transportation, Avanza** — rate card tulis tolak
   RM 190 sedangkan tambah RM 180. Ditinggalkan sebagai `null` (`dayDed` →
   `[Mari-Mari]` band 1–4).
2. **4D3N Full Tour, Avanza** — rate card tulis tambah RM 700 = tolak RM 700, dan
   lebih murah daripada 3D2N Avanza RM 800. Baris ini hanya rujukan dalam tab
   Simple Customisation; ia tidak dipakai kalkulator.
3. **Chanteek Borneo Indigenous Museum RM 270/pax** — jauh lebih tinggi daripada
   semua entrance fee lain (≤ RM 150). Angka rate card dikekalkan.
4. **Airport Transfer untuk van** — rate card hanya beri kadar Avanza / Innova untuk
   Airport Transfer KK Town (RM 50) dan Kundasang (RM 450). Group 5 pax ke atas akan
   dapat cip `kadar?`.
5. **Caj Last Minute** (&lt;3 minggu, +RM 300 / +RM 200 per pax) ada dalam R&D Sheet
   tetapi **tiada dalam katalog v3** — sengaja tidak dimasukkan. Sahkan sebelum quote.
6. **Pakej Guesthouse dan Honeymoon** — tiada katalog v3, jadi bukan varian
   kalkulator. Quote manual.
7. **Rate card melabel Ming Garden sebagai 4 Star** sedangkan katalog meletakkannya
   dalam tier 3-Star (bersama Dreamtel). Kalkulator ikut katalog.

## Nota

Repo ini **public** dan KB mengandungi harga dalaman serta analisis pesaing.

Selepas PO mula mengedit `calc-config.json` di sini, **fail dalam repo inilah sumber
sebenar** — tarik JSON terbaharu sebelum sesiapa bina semula KB, kalau tidak suntingan
PO akan ditimpa.
