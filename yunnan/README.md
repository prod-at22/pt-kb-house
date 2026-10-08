# ARBA Yunnan KB (TC Reference)

Interactive Travel-Consultant Knowledge Base untuk pakej **Private Tour Yunnan**
(3 Wilayah 6D5N · 4 Wilayah 7D6N — Kunming · Dali · Lijiang · Shangri La).

Disajikan sebagai `index.html` melalui GitHub Pages. Last updated: **3 September 2026**.

Sumber: katalog v1 (29 Jul 2026), Product Cheatsheet 2026 – Yunnan, rate card 2026/2027,
FAQs TL Online / CX Channel China, PT Travel Maps (Final).

> ⚠️ **Internal data caution:** halaman ini mengandungi harga dalaman, kadar surcharge
> dan nota kos supplier. Diterbitkan secara awam atas permintaan — sesiapa yang ada URL
> boleh melihatnya.

---

## Tab Simple Calculator

Tab **Simple Calculator** mengira quotation dari kadar katalog, mengesan peak season dari
tarikh, dan menjana PDF quotation format rasmi ARBA dalam tab baharu.

### Cara PO ubah harga sendiri

Semua nombor kalkulator duduk dalam **[`calc-config.json`](calc-config.json)** — bukan
dalam `index.html`. Edit fail JSON itu terus di GitHub (butang ✏️), commit, dan halaman
akan guna nilai baharu pada muat semula seterusnya. **Tidak perlu bina semula halaman.**

Kalau JSON rosak (koma tertinggal, kurungan tak tutup), halaman akan jatuh balik kepada
config terbenam **dan** papar notis merah di atas tab kalkulator — jadi suntingan yang
gagal tidak berlalu senyap.

### Medan mana nak diubah

| Nak ubah | Medan dalam `calc-config.json` |
|---|---|
| Harga tier (2–3 / 4–5 / 6–9 / 10–14 pax) | `variants[].tiers[]` — `a` adult, `c` child with bed, `n` child no bed |
| Single supplement | `variants[].single` (3W = 600, 4W = 700) |
| Panjang pakej | `variants[].days` / `variants[].nights` **dan** bilangan entri `variants[].itin[]` mesti sama |
| Itinerari default setiap hari | `variants[].itin[]` — `act` (Melayu, papar dalam KB), `eact` (Inggeris, masuk PDF) |
| Blok itinerary tambahan dalam dropdown | `library[]` |
| Dragon Boat Festival RM30/pax/malam | `peak.value` + `peak.windows[]` |
| Peak rata RM300/pax (Summer, Golden Week, Christmas & NY) | `extraSurcharge[]` |
| Surcaj travel 2027 RM100/pax | `extraSurcharge[]` (label `2027 travel surcharge`) |
| Late booking RM50/booking | `lateBooking.amount` |
| Malam tambahan + day tour (650 / 850 / 750 per pax) | `variants[].ext.rates.extNight` |
| Tolak 1 malam + day tour (−RM300/pax) | `variants[].ext.rates.nightShort` |
| Day tour sahaja (RM400/pax) | `variants[].ext.rates.dayTour` |
| Airport transfer tambah / tolak | `variants[].ext.rates.airT` / `airTCut` |
| Kadar tambah / tolak meal (RM60 / RM30 per pax per meal) | `mealDelta.add` / `mealDelta.drop` |
| Senarai add-on (bullet train, luggage van, malam hotel per bilik) | `addons[]` — `["Nama", hargaDewasa, hargaKanak, asas]` |
| Inclusions / exclusions PDF | `variants[].inclusions` / `exclusions` / `exclusionsTail` |
| Nota terms bawah quotation | `validity` |
| Deposit per pax | `deposit` |

### Peraturan penting bila mengedit

1. **`itin` mesti sama panjang dengan `days`.** Kalau tidak, notis merah muncul dan
   config terbenam digunakan.
2. **Setiap tier perlu semua lima medan** — `from`, `to`, `a`, `c`, `n`.
3. **Kalau tiada kadar tersiar, tulis `null`, jangan reka nombor.** Kalkulator akan papar
   cip merah `kadar?` dan baris amaran — itu memang niatnya. Contoh: kadar extension untuk
   7 pax ke atas tidak wujud dalam cheatsheet, jadi ia `null`.
4. `act` / `eact` / `inclusions` guna `&` biasa. `t`, `name`, `validity`, `paxNotes[].text`
   guna entiti HTML (`&amp;`, `&ndash;`, `&middot;`).
5. Jangan letak aktiviti optional dalam `eact` — kalkulator sudah menambahnya sendiri ke
   dalam PDF bila add-on itu dibeli.

### Perkara yang perlu PO sedar tentang model harga

- **Peak rata RM300/pax dikira ikut _departure date_.** Trip yang bertolak sebelum
  tetingkap peak tetapi bermalam di dalamnya (contoh bertolak 28 Jun, balik 3 Julai) tidak
  akan dikenakan secara automatik — semak manual.
- **Dragon Boat RM30/pax/malam** dikira ikut bilangan malam sebenar yang jatuh dalam
  19–21 Jun 2026 (2027: 12–14 Jun).
- **Blackout** (CNY 14–22 Feb 2026, Labor Day 1–5 Mei 2026) hanya ditulis dalam nota dan
  terms quotation; kalkulator tidak menghalang tarikh itu.
- **Malam tambahan = RM650/850/750 per pax** ialah kadar katalog "Extra 1 malam + 1 day
  tour", jadi transport + guide + meals hari itu sudah termasuk — sebab itu pilihan
  transport hari tambahan ialah *"sudah termasuk dalam malam tambahan"* (RM 0).
  Untuk **malam hotel sahaja** (tanpa day tour) guna add-on *Additional 4-Star hotel night
  — per room per night* (RM200 3W / RM250 4W), sebab kadar itu tersiar **per bilik**,
  bukan per pax.
- **Upgrade 4-Star RM240/pax** ialah caj **sekali** per pax, jadi ia diletak sebagai
  add-on, bukan pilihan per malam.
