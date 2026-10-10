# ARBA Medan – Danau Toba KB

> **Mulai 9 Okt 2026 kandungan KB dan `calc-config.json` datang dari PT R&D Costing Hub** (`prod-at22/rnd-hub`, `data/kb/medan-lake-toba.json`). Fail di sini ditulis semula oleh mirror — **jangan edit di GitHub repo ini**; edit di hub. Skema di bawah masih terpakai.

KB rujukan TC + **Simple Calculator** untuk PT Medan–Lake Toba 4D3N.

**Live:** https://prod-at22.github.io/pt-kb-house/medan-lake-toba/

| Fail | Guna |
|---|---|
| `index.html` | KB penuh + tab Simple Calculator. Jangan edit tangan. |
| `calc-config.json` | **Semua harga & kadar kalkulator.** PO edit fail ini sahaja. |

## Cara ubah harga

Klik `calc-config.json` → ikon pensel (Edit) → ubah nombor → **Commit changes**.
Perubahan naik ke halaman live dalam ~30 saat. Tekan **Muat semula kadar** dalam
tab kalkulator (atau refresh halaman) untuk nampak kesannya.

> Kalau JSON rosak (koma tertinggal, kurungan tak tutup), kalkulator akan papar
> notis merah dan jatuh balik ke harga terbenam. Betulkan JSON dan commit semula.

## Peta medan — di mana nombor duduk

### Harga pakej (tier)

`variants[].tiers[]` — satu baris per band pax. `a` = Adult, `c` = Child With Bed,
`n` = Child No Bed.

- `variants[0]` = **Option A** (laluan Parapat dahulu) — harga katalog m/s 1.
- `variants[1]` = **Option B** (laluan Samosir / Holbung) — harga yang **sama +RM 50/pax**
  (katalog m/s 3). Kalau harga katalog berubah, ingat naikkan **kedua-dua** varian.

### Surcaj

| Perkara | Medan | Nilai sekarang |
|---|---|---|
| Peak season (hotel 3★) | `peak.value` | RM 30/pax/malam |
| Tetingkap peak | `peak.windows[]` | 4 tetingkap katalog m/s 2 |
| Upgrade hotel 4★ (malam biasa) | `ext.rates.up4._default[].normal` | RM 100/pax/malam |
| Upgrade hotel 4★ (malam **peak**) | `ext.rates.up4pk._default[].normal` | RM 110/pax/malam |
| Single supplement | `variants[].single` | RM 250/pax |
| Late booking | `lateBooking.amount` / `.lt` | RM 50 kalau < 45 hari |
| Surcaj tarikh 8–15 Mac 2027 | `extraSurcharge[]` | RM 90/pax |
| Deposit | `deposit` | RM 250/pax |
| Add-on Drone Shooting | `addons[]` | RM 47/pax |

**Kenapa ada dua kadar upgrade 4★?** Katalog letak peak 3★ = RM 30/malam tetapi
peak 4★ = RM 40/malam. Enjin kira RM 30 automatik untuk setiap malam peak, jadi
pilihan *Upgrade hotel 4★ — malam PEAK* membawa RM 100 + beza RM 10 = **RM 110**,
supaya jumlah malam peak 4★ betul-betul RM 140 (RM 100 upgrade + RM 40 peak).
TC pilih *malam PEAK* hanya pada malam yang jatuh dalam tetingkap peak.

### Kadar yang MASIH KOSONG — perlu diisi PO

Katalog dan rate card **tidak menyiarkan** kadar hari tambahan / malam tambahan
untuk Medan. Jadi medan di bawah sengaja ditinggal `null`, dan kalkulator papar
cip merah **`kadar?`** dan baris amaran — bukan RM 0 senyap.

| Medan | Maksud |
|---|---|
| `ext.rates.day._default[].normal` | transport + driving guide **per kenderaan per hari tambahan**, ikut band pax (1–4 Avanza · 5 Innova · 6–19 Hiace) |
| `ext.rates.dayDed._default[].normal` | **tolakan** bila hari pakej ditukar jadi Free & Easy (nombor negatif) |
| `ext.rates.nightShort._default[].normal` | tolakan bila satu malam pakej dibuang (nombor negatif) |
| `ext.night.normal` / `.peak` | malam tambahan hotel, per pax per malam |
| `meals.lunch` / `meals.dinner` | kadar hidangan tambahan per pax |

Isi nombor (buang `null`) dan hari tambahan terus berharga betul.

## Nota operasi yang sudah terbina

- Kelas kenderaan ikut pax (Avanza / Innova / Hiace) — `paxNotes[]`.
- 20 pax ke atas melebihi tier katalog (tertinggi 10–19) — kalkulator beri amaran.
- Extra hour driver & guide 150,000 IDR/jam, tunai di Medan — dalam exclusions PDF.
- Katalog sah untuk tempoh perjalanan hingga **31 Januari 2027**. Surcaj Mac 2027
  wujud dalam rate sheet tetapi tarikh itu **di luar** tempoh sah katalog — sahkan
  dengan operator sebelum quote.

Sumber: katalog `PT MEDAN-LAKE TOBA 4D3N 2026 v3` (Last Updated 13 Mac 2026)
dan KB `PT MEDAN-LAKE TOBA KB (TC Reference) v2`.
