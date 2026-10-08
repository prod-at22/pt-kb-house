# PT Lombok KB — Simple Calculator

Halaman live: **https://prod-at22.github.io/pt-kb-house/lombok/**

Repo ini ada dua fail yang penting:

| Fail | Apa dia | Boleh PO edit? |
|---|---|---|
| `calc-config.json` | **semua nombor dan itinerary kalkulator** — harga tier, kadar peak, kadar transport, kadar malam, blok itinerary, add-on | **Ya** — edit terus di sini |
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

## Empat varian

Kelas hotel dijadikan varian berasingan sebab **kadar peak, kadar malam tambahan dan
kadar tolak malam semuanya berbeza antara 3★ dan 4★**.

| id | Pakej | Harga asas (2 pax) |
|---|---|---|
| `std3` | PT Lombok 4D3N · Hotel 3 bintang | RM 1,257/pax |
| `std4` | PT Lombok 4D3N · Hotel 4 bintang | RM 1,497/pax (= 3★ + RM80/pax/malam × 3) |
| `hny3` | PT Honeymoon 4D3N · Hotel 3 bintang | RM 2,697/couple |
| `hny4` | PT Honeymoon 4D3N · Hotel 4 bintang | RM 3,177/couple (= 2,697 + RM160/couple/malam × 3) |

> Honeymoon disimpan sebagai **harga per pax** (separuh harga per couple), sebab enjin
> mengira ikut pax. `hny3` = 2697 ÷ 2 = 1348.5. Kalau harga per couple berubah, bahagi
> dua dahulu sebelum masuk `tiers`.

---

## Di mana benda yang biasa diubah

### Harga katalog (tier per pax)

`variants[].tiers` — `a` = adult, `c` = CWB, `n` = CNB.

```json
{"from": 4, "to": 6, "a": 1197, "c": 1097, "n": 997}
```

Kalau harga 3★ berubah, ingat **`std4` juga perlu diubah** (3★ + RM240/pax untuk 3 malam).

### Kadar peak season

`variants[].peak` — `value` = kadar peak biasa (RM per pax per malam). Elemen
**keempat** dalam satu tetingkap = kadar khas tetingkap itu (dipakai untuk event
9–11 Okt 2026), elemen **kelima** = nama musim.

```json
"peak": {"mode": "perNight", "value": 60,
         "windows": [["2026-03-15","2026-03-31", null, 60],
                     ["2026-10-09","2026-10-11", null, 150, "Event Peak Season"]]}
```

Kadar semasa: `std3` 60 / event 150 · `std4` 70 / event 250 · `hny3` 60 / event 150 ·
`hny4` 70 / event 250. **Honeymoon dalam unit per pax** — RM120/couple/malam = 60.

### Kadar transport (rate card operasi)

`variants[].ext.rates.day` — kunci = jenis hari, nilai = band ikut **kapasiti kenderaan**.

```json
"[Full Day]": [{"from":1,"to":4,"normal":250,"peak":250},
               {"from":5,"to":6,"normal":320,"peak":320},
               {"from":7,"to":12,"normal":420,"peak":420},
               {"from":13,"to":99,"normal":null,"peak":null}]
```

- `[Full Day]` 250 / 320 / 420 · `[Half Day]` 200 / 250 / 320 · `[Airport Transfer]` 150 / 180 / 210
- `ext.rates.dayDed` = lajur **Harga Tolak** (nombor negatif): −200/−270/−370, −150/−200/−270, −100/−130/−160
- Band 13–99 sengaja `null` — rate card tiada kadar bas. Halaman papar cip merah
  `kadar?`, bukan RM 0. Isi nombornya di sini bila operator dah bagi.

Kadar ini **per kenderaan** dan dibahagi sama rata antara pax berbayar
(`ext.shareVehicle: true`).

### Kadar malam tambahan / tolak malam

```json
"ext": {"night": {"normal": 85, "peak": 145}}
"ext": {"rates": {"nightShort": {"_default":[{"from":1,"to":99,"normal":-50,"peak":0}]}}}
```

3★ tambah 85 / peak 145, tolak −50 · 4★ tambah 120 / peak 190, tolak −90.
`nightShort.peak` = **0** sebab rate card tiada tolakan malam semasa peak.

### Kadar meal

`mealDelta` — `add` 30, `drop` 20 (per pax per hidangan). **Breakfast neutral**:
ia dikawal oleh `variants[].breakfast` dan tiada kadar tambah/tolak, sama seperti
rate card ("Suggest at Hotel" / "–").

### Add-on

`addons` — `["Nama", hargaDewasa, hargaKanak, basis]`.
Basis: `"pax"` (default, kuantiti auto ikut pax) · `"unit"` (per carriage/couple) ·
`"share"` (kos satu group, dibahagi antara pax — dipakai untuk boat Pink Beach).
Nilai **negatif** = lajur Harga Tolak rate card.

### Blok itinerary

`library[]` — blok yang TC boleh pilih pada mana-mana hari. `region` menentukan kadar
transport hari itu (`[Full Day]` / `[Half Day]` / `[Airport Transfer]`). Blok
`ext` dan `exth` khas untuk **hari tambahan** (ia sudah berkos); blok tour lain
(`gili`, `sembalun`, `d3b`, `sasak`, `gumuk`) ialah blok **dalam pakej** — tukar
antaranya pada hari pakej = RM 0.

---

## Nota kadar (bukan tetapan)

- **Upgrade 4★ Honeymoon RM160/couple/malam.** Katalog v3 bercanggah dengan dirinya
  sendiri (jadual RM160, kotak callout RM120). PO pilih RM160 pada 3 Sep 2026 — ia
  konsisten dengan katalog Standard RM80/pax × 2 pax.
- **13–15 pax:** katalog beri tier harga sehingga 15 pax, tetapi rate card transport
  setakat Hiace 12 pax sahaja. Kalkulator akan tanda gap; sahkan kadar bas dengan
  operator sebelum quote.
- **Buang baris hari** menolak malam pakej sahaja. Kalau hidangan juga perlu ditolak,
  jangan buang barisnya — set Accommodation ke *Tolak 1 malam dari pakej* dan Meal ke
  *Breakfast sahaja*.
