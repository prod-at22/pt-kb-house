# PT Maldives KB — Simple Calculator

> **Mulai 9 Okt 2026 kandungan KB dan `calc-config.json` datang dari PT R&D Costing Hub** (`prod-at22/rnd-hub`, `data/kb/maldives.json`). Fail di sini ditulis semula oleh mirror — **jangan edit di GitHub repo ini**; edit di hub. Skema di bawah masih terpakai.

Halaman live: **https://prod-at22.github.io/pt-kb-house/maldives/**

Repo ini ada dua fail yang penting:

| Fail | Apa dia | Boleh PO edit? |
|---|---|---|
| `calc-config.json` | **semua nombor dan itinerary kalkulator** — harga tier, surcaj musim, malam tambahan, add-on, upgrade | **Ya** — edit terus di sini |
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

| `id` | Pakej | Adult | CWB | CNB |
|---|---|---|---|---|
| `basic` | Basic 4D3N (3★ Maafushi) | 2,097 | 1,697 | 1,097 |
| `star4` | 4-Star 4D3N (full board) | 3,097 | 2,197 | 1,797 |
| `combo` | Combo Island 4D3N | 4,197 | 3,997 | 3,797 |
| `wv` | Water Villa 4D3N (OBLU) | 5,197 | 4,997 | 4,797 |

Semua satu tier sahaja, 2–10 pax — harga tidak turun ikut saiz group.
Infant RM100 (bukan FOC). Ubah di `variants[].tiers` / `variants[].infant`.

---

## Surcaj musim — mod `flat`

Maldives **tidak** sama dengan destinasi lain. Katalog tulis
*"Add on RM100 per person"* untuk satu tetingkap tarikh travel — iaitu **satu amaun
rata per pax untuk keseluruhan trip**, bukan per malam. Sebab itu `peak.mode` di sini
ialah `"flat"`, bukan `"perNight"`.

Setiap varian ada tetingkapnya sendiri di `variants[].peak.windows`. Bentuk satu
tetingkap:

```json
["2026-01-11", "2026-04-30", null, 100, "High Season"]
```

| Kedudukan | Maksud |
|---|---|
| 1 | tarikh mula |
| 2 | tarikh tamat |
| 3 | `null` = semua varian (biarkan `null` di sini) |
| 4 | **amaun RM per pax**, atau perkataan `"request"` |
| 5 | nama musim — muncul dalam nota KB dan baris **Season** pada PDF quotation |

**Tetingkap bertindih:** yang paling tinggi menang. Sebab itu 24 Disember dikira
RM600 (Christmas Eve) dan bukan RM200 (Peak Season) + RM600 — katalog menyenaraikan
Christmas eve / New year eve sebagai **baris berasingan** dalam jadual yang sama,
jadi ia dibaca sebagai kadar ganti. Kalau operator sahkan ia sepatutnya **bertimbun**,
beritahu team product — itu perlu tukar cara enjin mengira, bukan sekadar JSON.

**`"request"` = price upon request.** Combo (1 Sep – 31 Dis 2026) dan Water Villa
(25 – 31 Dis 2026) ialah Super Peak tanpa harga tersiar. Kalkulator sengaja
**tidak mengira apa-apa** untuk tarikh itu dan papar amaran merah; PDF quotation
tulis `Super Peak Season - price upon request`. Bila operator dah bagi harga, tukar
`"request"` kepada nombor, contoh `500`.

> Katalog Combo bercanggah dengan dirinya sendiri: Shoulder Season 1–31 Okt 2026
> (+RM100) berada **dalam** Super Peak 1 Sep – 31 Dis 2026 (price on request).
> Kalkulator memilih `request` (lebih selamat). Sahkan dengan operator yang mana betul.

### Surcaj travel 2027

`extraSurcharge[]` — RM200/pax untuk departure **11 Jan – 30 Jun 2027**, semua varian.

```json
{"label": "Travel date 2027", "dateIn": ["2027-01-11", "2027-06-30"], "perPax": 200}
```

Ia bermula 11 Jan (bukan 1 Jan) supaya **tidak bertindih** dengan Peak Season
21 Dis 2026 – 10 Jan 2027 pada varian Basic & 4-Star. Kalau nak ia bertimbun,
tukar tarikh mula kepada `2027-01-01`.

Beza dengan `peak`: `extraSurcharge` diuji pada **departure date** sahaja, `peak`
diuji pada **setiap malam** trip.

---

## Late booking & last minute

| Perkara | Di mana | Kadar |
|---|---|---|
| Late booking (<45 hari) | `lateBooking` | RM50 **satu booking** |
| Last minute (<3 minggu) | `variants[].lastMinute` | Basic 2 pax RM300 / 3–10 pax RM200 · 4-Star, Combo, WV 2 pax RM400 / 3+ RM300 |

Kedua-duanya dicaj **sekali satu booking**, bukan per pax — itulah maksud
`"perGroup": true` dalam `lastMinute`. Jangan buang medan itu, kalau tidak kadar akan
didarab dengan bilangan pax.

Last minute untuk **Combo & Water Villa datang dari rate card 2026/2027, bukan
katalog** — sahkan sebelum quote group besar.

---

## Malam tambahan & upgrade hotel

Kadar malam tambahan datang dari **rate card ARBA, tiada dalam katalog**:

| Pilihan hari | `ext.rates` | Kadar |
|---|---|---|
| Malam tambahan — hotel 3★ Maafushi | `n3` | RM550 /pax /malam |
| Malam tambahan — hotel 4★ Maafushi | `n4` | RM800 /pax /malam |
| Malam tambahan — water villa | `nwv` | RM1,600 /pax /malam |

Bila TC tekan **+ Tambah Hari**, hari baharu guna pilihan *kelas hotel pakej*
(`variants[].ext.night`) — 550 untuk Basic & Combo, 800 untuk 4-Star, 1,600 untuk
Water Villa. TC boleh tukar kepada mana-mana kelas di atas pada baris hari itu.

> **Combo:** hari tambahan default kepada RM550 (local island 3★). Tiada kadar malam
> tambahan tersiar untuk Adaaran Select Hudhuran Fushi — kalau customer nak tambah
> malam water villa Adaaran, minta operator quote, jangan guna kadar OBLU RM1,600.

> **Buang hari:** tiada kadar tolakan tersiar untuk trip yang lebih pendek daripada
> pakej. Kalkulator tidak akan menolak apa-apa — minta operator quote semula.

### Upgrade 3★ → 4★ (Basic sahaja)

Katalog Basic **bercanggah dengan dirinya sendiri**: muka depan tulis RM240/pax,
Important Notes (m/s 7) tulis RM400/pax. Kedua-duanya disediakan sebagai pilihan
Accommodation:

| Pilihan | `perPax` dalam JSON | Jumlah 3 malam |
|---|---|---|
| kadar muka depan katalog | 80 | RM240/pax |
| kadar Important Notes katalog | 133.33333333333334 | RM400/pax |

Pilihan Accommodation dicaj **per malam**, jadi amaun katalog dibahagi 3 malam.
Letak pilihan itu pada **ketiga-tiga malam pakej** (Day 1, 2, 3) supaya jumlahnya
tepat dan lajur Accommodation dalam PDF betul-betul tulis 4-Star pada setiap malam.
Bila operator sahkan satu kadar muktamad, buang pilihan yang tidak dipakai.

---

## Transport

Semua pergerakan Maldives guna speedboat sharing yang sudah termasuk pakej — tiada
kadar transport per hari. Satu-satunya kadar transport tersiar ialah:

**Speedboat ketibaan lewat (selepas 8 malam) — RM150 per hala per pax**
(rate card ARBA; katalog hanya sebut *extra charges apply*). Pilih
*Airport transfer by speedboat – ketibaan selepas 8 malam* pada hari ketibaan
dan/atau hari balik. Kadar di `trpOptions[v=airlate].perPax`.

---

## Add-on / optional activity

`addons[]` — `["Nama", hargaAdult, hargaChild, "pax"|"unit"]`.

- `"pax"` = kuantiti diisi automatik ikut bilangan pax.
- `"unit"` = sekali sahaja (bedroom decoration, candle-light dinner, couple spa).
- Nama masuk PDF quotation, jadi **tulis dalam Bahasa Inggeris**.

Excursion ditag ikut hotel (Kaani / Arena / ICOM / Velana) sebab **aktiviti mesti
ditempah dengan hotel yang sama**. Minimum pax: 6 (Kaani) · 10 (Arena) — kalkulator
papar nota ini sendiri bila pax kurang (`paxNotes[]`).

Travel essentials (pocket WiFi, eSIM, Takaful, luggage tracker) **sengaja tidak
dimasukkan** — itu jualan after-sales, bukan sebahagian quotation PT.

Extra halal lunch RM50 dan extra dinner RM65 ada sebagai add-on. Menukar dropdown
**Meal** pada baris hari tidak menambah atau menolak apa-apa — katalog tidak beri
kadar tolakan meal, jadi guna add-on untuk meal tambahan.

---

## Lain-lain

| Nak ubah | Di mana |
|---|---|
| Single supplement (RM700; Basic quoted on request) | `variants[].single` |
| Harga infant | `variants[].infant` |
| Deposit per pax (RM500) | `deposit` |
| Late booking surcharge | `lateBooking` |
| Inclusions / exclusions PDF | `variants[].inclusions`, `exclusions`, `exclusionsTail` |
| Teks bawah PDF quotation | `validity` |
| Nota ikut saiz group | `paxNotes[]` |
| Itinerary default setiap varian | `variants[].itin[]` |

`variants[].itin[]` — `t` / `act` Bahasa Melayu (dipapar dalam KB), `en` / `eact`
Bahasa Inggeris (masuk PDF quotation). Bilangan hari **mesti** sama dengan `days`.
Penanda `"{auto}"` dalam `inclusions` diganti dengan baris yang dijana daripada
itinerary sebenar, supaya inclusions tidak jadi basi bila TC ubah hari.

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

*Sumber nombor: katalog `MALDIVES BASIC 4D3N 2026 v4`, `PT MALDIVES 4D3N 2026 v3`
(4-Star), `PT MALDIVES 4D3N COMBO 2026`, `PT MALDIVES 4D3N WATER VILLA`, dan rate
card ARBA 2026/2027 untuk malam tambahan, speedboat ketibaan lewat serta last minute
Combo & Water Villa. Repo ini public — ia mengandungi harga dalaman.*
