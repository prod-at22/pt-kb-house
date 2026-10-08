# PT Jakarta-Bandung KB — Simple Calculator

Halaman live: **https://prod-at22.github.io/pt-kb-house/jakarta-bandung/**

Repo ini ada dua fail yang penting:

| Fail | Apa dia | Boleh PO edit? |
|---|---|---|
| `calc-config.json` | **semua nombor dan itinerary kalkulator** — harga tier, kadar peak, kadar transport ikut kawasan, malam tambahan, add-on, surcaj | **Ya** — edit terus di sini |
| `index.html` | halaman KB penuh (termasuk tab Simple Customisation) + enjin kalkulator | Tidak — perlu bina semula |

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

| Sumber | Apa yang datang dari situ |
|---|---|
| Katalog `PT JKT-BANDUNG 4D3N 2026` (8 Ogos 2026) | tier per pax, peak season RM30/RM35, upgrade 4★ RM90, single supplement RM350, late booking RM50, deposit RM250, itinerari 4 hari Option A / Option B |
| Rate Card Operasi Bandung (3 Sept 2026) | kadar transport ikut jenis tour × kelas kenderaan, lajur Harga Tolak, malam tambahan Bandung/Jakarta 3★/4★, meal tambah/tolak, entrance, Whoosh / Panoramic / Argo |
| 2026/2027 Date Surcharge ARBA | surcaj travel date 2027 RM50/pax |

Bila rate card dan R&D Sheet bercanggah, **rate card menang** (keputusan PO, 3 Sept 2026).

---

## Di mana benda yang biasa diubah

### Harga katalog (tier per pax)

`variants[].tiers` — `a` = adult, `c` = Child With Bed, `n` = Child No Bed.
Kedua-dua varian (`optA`, `optB`) guna tier yang sama.

```json
{"from": 4, "to": 5, "a": 1227, "c": 1127, "n": 927}
```

### Kadar peak season

`peak.value` = RM per pax per malam peak (sekarang **30**, ikut 3★ katalog).
`peak.windows` = senarai tetingkap tarikh.

```json
"peak": {"mode": "perNight", "value": 30,
         "windows": [["2026-03-19","2026-03-28"], ["2026-05-14","2026-05-16"]]}
```

Nak tambah tetingkap baharu: tambah satu baris `["2027-03-15","2027-03-25"]`.

**Hotel 4★ pada malam peak** ialah RM35, bukan RM30. Beza RM5 itu ada dalam pilihan
accommodation `up4pk` (RM95 = RM90 upgrade + RM5 beza peak). TC pilih
*Naik taraf hotel 4 bintang – malam peak season* pada baris hari yang peak.

### Kadar transport ikut kawasan

`ext.rates.day` — kunci = tag kawasan, nilai = band pax (ikut kelas kenderaan).

```json
"[Bandung]": [{"from":2,"to":4,"normal":260,"peak":260},
              {"from":5,"to":6,"normal":300,"peak":300},
              {"from":7,"to":12,"normal":400,"peak":400},
              {"from":13,"to":19,"normal":null,"peak":null}]
```

- `[Bandung]` = Bandung Tour · `[Jakarta]` = Jakarta Tour
- `_default` sengaja `null` — hari tanpa tag kawasan mesti papar cip merah `kadar?`,
  bukan diam-diam guna kadar Bandung.
- Band `13–19` `null` kerana rate card tidak menyiarkan kadar untuk lebih satu Hiace.
  Isi nombornya di sini bila operasi dah bagi.

### Kadar lain dalam `ext.rates`

| Kunci | Maksud | Sekarang |
|---|---|---|
| `dayDed` | Harga Tolak transport (free & easy) | −100 / −150 / −200 |
| `transfer` | Transfer to Jakarta/Bandung | 400 / 450 / 550 |
| `xferDed` | Harga Tolak transfer | −150 rata |
| `hBdg4` | malam tambahan Bandung 4★ | 150 |
| `hJkt3` | malam tambahan Jakarta 3★ | 110 |
| `hJkt4` | malam tambahan Jakarta 4★ | 200 |
| `nightShort` | tolak 1 malam pakej 3★ | −50 |
| `nightShort4` | tolak 1 malam pakej 4★ | −100 |

Malam tambahan Bandung 3★ (RM90) ada dalam `ext.night`, bukan `ext.rates`.

### Pindah bandar

Nota rate card: transfer Jakarta↔Bandung = **full day tour + transfer**, dua baris.
Itu dibuat oleh pilihan transport `xfer`, yang mengenakan kadar hari (`ext.rates.day`
ikut kawasan) **dan** `ext.rates.transfer` sekali. Blok itinerary `xferjb` dan `xferbj`
sudah tetapkan pilihan itu.

### Meal tambah / tolak

`mealDelta` — `add` 30, `drop` 20 (RM per pax per hidangan). Enjin bandingkan pilihan
meal pada baris hari dengan apa yang blok itinerary itu sendiri isytiharkan, jadi
tiada perubahan = RM 0.

### Add-on (entrance, train, upgrade)

`addons` — `["Nama", hargaDewasa, hargaKanak, "pax"]`. **Nama add-on muncul dalam PDF
quotation customer**, jadi tulis dalam Bahasa Inggeris.

### Surcaj tarikh 2027

`extraSurcharge` — RM50/pax untuk berlepas 1 Jan – 30 Jun 2027.

---

## Apa yang kalkulator tidak buat

- Tiket penerbangan antarabangsa, travel insurance, Blue Ribbon luggage, TripCare 360 —
  itu after-sales yang jual, bukan sebahagian quotation ground.
- Zip Bike dan Rainbow Slide — bayar terus di lokasi, tidak masuk quotation.
- Group 13 pax ke atas — perlu lebih satu Hiace dan rate card tiada kadarnya;
  kalkulator akan papar `kadar?` dan minta sebut harga operasi.
