# ARBA Beijing KB (TC Reference)

Interactive Travel-Consultant Knowledge Base untuk **PT Beijing 5D4N** — dua varian flight:
ketibaan pagi (Malaysia Airlines) dan ketibaan malam (AirAsia).

Disajikan sebagai `index.html` melalui GitHub Pages. Last updated: **3 September 2026**.

Sumber: katalog PT Beijing 5D4N 2026 (last updated 4 Mac 2026), Product Cheatsheet 2026 – Beijing,
rate card, trip doc, Travel Map & FAQ TL Online (China). **Katalog adalah source of truth.**

> ⚠️ **Internal data caution:** halaman ini mengandungi harga dalaman, kadar surcharge dan
> nota kos supplier. Diterbitkan secara awam atas permintaan — sesiapa yang ada URL boleh melihatnya.

---

## Tab Simple Calculator

Tab **Simple Calculator** mengira quotation dari kadar katalog, mengesan peak season dari tarikh,
dan menjana PDF quotation format rasmi ARBA dalam tab baharu.

### Cara PO ubah harga sendiri

Semua nombor kalkulator duduk dalam **[`calc-config.json`](calc-config.json)** — bukan dalam
`index.html`. Edit fail JSON itu terus di GitHub (butang ✏️), commit, dan halaman akan guna nilai
baharu pada muat semula seterusnya. **Tidak perlu bina semula halaman.**

Kalau JSON rosak (koma tertinggal, kurungan tak tutup), halaman jatuh balik kepada config terbenam
**dan** papar notis merah di atas tab kalkulator — jadi suntingan yang gagal tidak berlalu senyap.

### Medan mana nak diubah

| Nak ubah | Medan dalam `calc-config.json` |
|---|---|
| Harga tier (2–3 / 4–5 / 6–9 / 10–15 pax) | `variants[].tiers[]` — `a` adult, `c` child with bed, `n` child no bed |
| Single supplement (RM 800) | `variants[].single` |
| Panjang pakej | `variants[].days` / `nights` **dan** bilangan entri `variants[].itin[]` mesti sama |
| Itinerari default setiap hari | `variants[].itin[]` — `act` (Melayu, papar dalam KB), `eact` (Inggeris, masuk PDF) |
| Blok itinerary tambahan dalam dropdown | `library[]` |
| Dragon Boat RM 60/pax/malam | `peak.value` + `peak.windows[]` |
| Super Peak RM 300/pax (Summer, Golden Week, Christmas & NY) | `extraSurcharge[]` |
| Surcaj travel 2027 RM 100/pax | `extraSurcharge[]` (label `2027 travel surcharge`) |
| Late booking RM 50/booking | `lateBooking.amount` |
| Malam tambahan + 1 hari tour (RM 450 / RM 650 per pax) | `variants[].ext.rates.extNight` |
| Day tour per kenderaan (RM 1,500 / RM 1,700) | `variants[].ext.rates.dayTour` |
| Tolak day tour (−RM 800) | `variants[].ext.rates.dayTourCut` |
| Airport transfer tambah / tolak | `variants[].ext.rates.airT` / `airTCut` |
| Kadar tambah / tolak meal (RM 60 / RM 30 per pax per meal) | `mealDelta.add` / `mealDelta.drop` |
| Add-on (USB, Guangzhou, malam hotel per bilik, upgrade Superior) | `addons[]` — `["Nama", hargaDewasa, hargaKanak, asas]` |
| Inclusions / exclusions PDF | `variants[].inclusions` / `exclusions` / `exclusionsTail` |
| Nota terms bawah quotation | `validity` |
| Deposit per pax | `deposit` |

### ⚠️ Dua kadar yang MEMANG kosong — perlu diisi PO

Kalkulator akan papar cip merah **`kadar?`** untuk dua sel di bawah. Ini **disengajakan** —
nilainya tiada dalam Product Cheatsheet 2026, jadi ia tidak direka:

| Kadar | Lokasi dalam JSON | Kenapa kosong |
|---|---|---|
| Day tour **2–4 pax** (MPV) | `ext.rates.dayTour` → band `from:2,to:4` | Jadual *Tour transport* cheatsheet hanya ada Van 5–6 pax (RM 1,500) dan Bus 7–12 pax (RM 1,700). **Tiada baris MPV 2–4 pax.** Tab KB *Transportation & Guide* tulis RM 1,000 tetapi angka itu tiada dalam cheatsheet. |
| Tolak day tour **2–4 pax** | `ext.rates.dayTourCut` → band `from:2,to:4` | Lajur *Harga Tolak* juga hanya ada untuk 5–6 dan 7–12 pax (−RM 800). |

Untuk mengisi, tukar `"normal": null` kepada nombor yang disahkan operator, contoh:

```json
"dayTour": {"_default":[{"from":2,"to":4,"normal":1000}, ...]}
```

Sementara itu, untuk group 2–4 pax gunakan kadar **per pax** *Malam tambahan + 1 hari tour*
(RM 450/pax) yang memang tersiar.

Kadar transport untuk **13–15 pax** juga kosong — jadual katalog beri harga tier sehingga 15 pax
tetapi jadual transport hanya sehingga 12 pax.

### Peraturan penting bila mengedit

1. **`itin` mesti sama panjang dengan `days`.** Kalau tidak, notis merah muncul dan config
   terbenam digunakan.
2. **Setiap tier perlu semua lima medan** — `from`, `to`, `a`, `c`, `n`.
3. **Kalau tiada kadar tersiar, tulis `null`, jangan reka nombor.** Cip merah `kadar?` itu betul;
   mengagak tidak.
4. `act` / `eact` / `inclusions` guna `&` biasa. `t`, `name`, `validity`, `paxNotes[].text`
   guna entiti HTML (`&amp;`, `&ndash;`, `&middot;`).
5. Jangan letak aktiviti optional dalam `eact` — kalkulator sudah menambahnya sendiri ke dalam
   PDF bila add-on itu dibeli.
6. Dalam templat `incl`, **jangan tulis perkataan "daily"** dan jangan mula templat dengan
   `{n}` — kedua-duanya memecahkan padanan baris inclusions.

### Perkara yang perlu PO sedar tentang model harga

- **Super Peak RM 300/pax dikira ikut _departure date_.** Trip yang bertolak sebelum tetingkap
  peak tetapi bermalam di dalamnya (contoh bertolak 30 Jun, balik 4 Julai) **tidak** kena
  automatik — semak manual.
- **Dragon Boat RM 60/pax/malam** dikira ikut bilangan malam sebenar yang jatuh dalam
  19–21 Jun 2026 (2027: 12–14 Jun).
- **Blackout** (CNY 14–22 Feb 2026, Labor Day 1–5 Mei 2026) ditulis dalam nota & terms quotation;
  kalkulator tidak menghalang tarikh itu.
- **Malam tambahan RM 450 / RM 650 per pax** ialah kadar katalog *"Add 1 night + 1 day tour
  Beijing"*, jadi transport + guide hari itu sudah termasuk — sebab itu pilihan transport hari
  tambahan ialah *"sudah termasuk dalam malam tambahan"* (RM 0). Kadar ini **belum termasuk meals**.
- **Tolak malam hotel tersiar per BILIK** (−RM 100/bilik/malam), bukan per pax — jadi ia add-on
  `unit`, bukan pilihan hari. Buang satu hari dari itinerary **tidak** menolak apa-apa secara
  automatik; guna add-on *Less one hotel night*.
- **Upgrade 4-Star Superior RM 240/pax** ialah caj **sekali** per pax, jadi ia add-on, bukan
  pilihan per malam. (Nota: muka depan katalog tulis "Upgrade to 4 star hotel +RM240/person"
  sedangkan pakej memang sudah 4★ — maksud sebenarnya perlu disahkan operator.)
- **Universal Studios Beijing** perlu ganti satu hari itinerari, ATAU tambah 1 malam + 1 hari
  tour + USB + meals. Pilih blok *Universal Studios Beijing* dalam dropdown Itinerary, kemudian
  tambah add-on USB untuk harga.
