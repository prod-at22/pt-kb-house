# PT Perhentian &mdash; KB (TC Reference) + Simple Calculator

> **Mulai 9 Okt 2026 kandungan KB dan `calc-config.json` datang dari PT R&D Costing Hub** (`prod-at22/pt-rnd-hub`, `data/kb/perhentian.json`). Fail di sini ditulis semula oleh mirror — **jangan edit di GitHub repo ini**; edit di hub. Skema di bawah masih terpakai.

Halaman live: **https://prod-at22.github.io/pt-kb-house/perhentian/**

Repo ini menyajikan `index.html` sebagai GitHub Pages. Dua fail sahaja yang penting:

| Fail | Guna |
|---|---|
| `index.html` | KB penuh + tab **Simple Calculator**. Jangan edit tangan. |
| `calc-config.json` | **Semua harga kalkulator.** Edit fail ini terus di GitHub. |

## Cara ubah harga

Klik `calc-config.json` &rarr; ikon pensel &rarr; ubah nombor &rarr; **Commit changes**.
Tunggu ~30 saat, refresh halaman live. Tiada rebuild diperlukan.

Kalau JSON rosak (koma tertinggal, petik tak tutup), kalkulator jatuh balik ke config
terbenam dan papar **notis merah** di atas tab. Betulkan JSON, commit lagi.

## Peta medan &mdash; mana nak ubah apa

Ada **4 varian** dalam `variants[]`, ikut susunan dropdown pakej:

| index | `id` | Pakej | Sumber harga |
|---|---|---|---|
| 0 | `basic` | Shari-la (BASIC) | katalog V3 2026 |
| 1 | `standard` | Mimpi (STANDARD) | katalog V3 2026 |
| 2 | `ombak` | Ombak | rate card ARBA |
| 3 | `florabay` | Flora Bay | rate card ARBA |

### Harga tier per pax
`variants[N].tiers[]` &mdash; satu baris per band pax:

```json
{"from": 2, "to": 3, "a": 1097, "c": 997, "n": 897}
```

`a` = dewasa &middot; `c` = CWB (6&ndash;11 thn) &middot; `n` = CNB (2&ndash;5 thn).
Band dipadan ikut **jumlah pax berbayar**, julat pertama yang muat.

Kalau satu band memang **tiada harga tersiar**, tulis `"a": "request"` (bukan `0`) &mdash;
kalkulator akan papar amaran *price on request* dan bukan RM 0 secara senyap.
Itulah yang dipakai untuk Flora Bay 1 pax sekarang.

### Single supplement
`variants[N].single` &mdash; kadar rata per pax: BASIC 500, STANDARD 600, Ombak/Flora Bay 400.

### Peak season
`variants[N].peak` &mdash; `mode` kekal `"perNight"` (RM per pax per **malam peak**):

```json
{"mode":"perNight","value":50,"windows":[["2025-03-21","2026-09-30"],["2027-02-15","2027-03-31"]]}
```

- `value` = RM per pax per malam.
- `windows` = senarai `[mula, tamat]` dalam format `YYYY-MM-DD`.
- **Ombak dan Flora Bay ada `"windows": []` (kosong)** &mdash; amaunnya tersiar
  (+RM150 dan +RM50) tetapi tarikhnya tidak pernah disiarkan dalam rate card.
  Bila PO dapat tarikh sebenar, masukkan ke dalam `windows` dan surcaj mula dikira.

### Tambah / kurang malam
`variants[N].ext.rates` &mdash; dua kunci:

| Kunci | Maksud | Nilai sekarang |
|---|---|---|
| `addnight` | RM per pax untuk setiap malam **tambahan** | Mimpi 550 &middot; Ombak 475 &middot; BASIC 0 &middot; Flora Bay 0 |
| `nightShort` | RM per pax untuk setiap malam yang **dibuang** (nombor negatif) | Ombak &minus;400 &middot; lain-lain 0 |

`0` bermakna **kadar belum tersiar** &mdash; kalkulator papar cip merah `kadar?` pada
baris hari itu, bukan RM 0 diam-diam. Isi nombor bila kadar diperoleh.

### Add-on
`addons[]` &mdash; `["Nama", hargaDewasa, hargaKanak, asas]`.
`asas` = `"pax"` (kuantiti auto ikut bilangan pax) atau `"unit"` (satu unit, contoh
per boat atau per couple). `hargaKanak` `0` = tiada harga kanak-kanak.

### Late booking & deposit
`lateBooking` = `{"lt":45,"amount":50}` &middot; `deposit` = `250` (per pax).

### Teks bawah quotation
`validity` &mdash; **dicetak terus ke PDF customer**, jadi kekalkan Bahasa Inggeris.
Nota dalaman untuk TC letak dalam `paxNotes[]` (itu muncul dalam KB sahaja, tidak
masuk PDF).

## Perkara yang masih perlu disahkan dengan operator

1. **Peak BASIC menelan hampir seluruh musim.** Katalog V3 tulis window
   21 Mac 2025 &ndash; 30 Sep 2026, dan pulau tutup monsun 15 Okt &ndash; 15 Feb, jadi
   satu-satunya tarikh bukan-peak dalam 2026 ialah 1&ndash;15 Okt. Dikodkan ikut katalog
   atas arahan PO.
2. **Tarikh peak Ombak / Flora Bay** &mdash; belum tersiar (lihat `windows: []` di atas).
3. **Kadar tambah-malam** BASIC &amp; Flora Bay, dan **kredit kurang-malam** BASIC,
   STANDARD &amp; Flora Bay &mdash; belum tersiar.
4. **Airport transfer:** katalog tulis "Return Airport Transfer RM65/pax" tetapi R&D
   sheet tulis RM65 = **sehala** dan return = RM130. Kedua-dua versi ada dalam senarai
   add-on; pilih yang betul.
5. **Marine Park Fee:** katalog V3 RM5 dewasa / RM2 kanak; RAW DATA PHT 2026 RM12/pax.
   Dikecualikan dari harga pakej, jadi ia tidak menjejaskan pengiraan.
6. **Halfboard:** rate card tulis &minus;RM150/dewasa untuk buang lunch+dinner
   (2 malam). Kalkulator guna kadar per hidangan RM35, jadi buang 4 hidangan =
   &minus;RM140. Beza RM10.
7. **CWB tambah-malam RM375** tidak dapat dimodelkan &mdash; kadar malam tambahan
   dikenakan sama rata untuk semua pax.
8. **Lebih 10 pax** &mdash; tier katalog berhenti di 10; kalkulator guna tier 8&ndash;10
   dan papar amaran. Quote manual.
