# ARBA New Zealand KB (TC Reference)

> **Mulai 9 Okt 2026 kandungan KB dan `calc-config.json` datang dari PT R&D Costing Hub** (`prod-at22/pt-rnd-hub`, `data/kb/new-zealand.json`). Fail di sini ditulis semula oleh mirror — **jangan edit di GitHub repo ini**; edit di hub. Skema di bawah masih terpakai.

Knowledge Base destinasi New Zealand untuk Travel Consultant ARBA — Private Tour (PT)
dan Self Tour (ST). Disajikan sebagai `index.html`.

**Live:** https://prod-at22.github.io/pt-kb-house/new-zealand/

> Nota data dalaman: ini KB PENUH — mengandungi harga dalaman, surcharge rate card
> 2026/2027 dan kod promo Free Gift. Repo public: sesiapa yang ada URL boleh lihat.

---

## Fail dalam repo ini

| Fail | Apa dia |
|---|---|
| `index.html` | KB penuh + tab **Simple Calculator** |
| `calc-config.json` | **semua harga & kadar kalkulator** — PO edit fail ini |

## Cara PO ubah harga sendiri

Kalkulator membaca `calc-config.json` setiap kali halaman dibuka. Jadi untuk tukar
harga, **jangan** minta bina semula KB — cukup edit JSON di sini:

1. Buka `calc-config.json` → tekan ikon pensel (Edit this file).
2. Ubah nombor yang perlu.
3. Tekan **Commit changes** (terus ke `main`).
4. Tunggu ~30 saat, refresh KB. Selesai.

Kalau JSON rosak (koma tertinggal, kurungan tak tutup), KB **tidak** senyap — ia
papar notis merah di atas kalkulator dan guna salinan lama yang terbenam dalam
`index.html`. Betulkan JSON dan commit semula.

### Medan mana nak diubah

| Nak ubah | Cari medan |
|---|---|
| Harga pakej ikut bilangan pax | `variants[].tiers` — `from`/`to` = julat pax, `a` = adult, `c` = child with bed, `n` = child no bed |
| Tarikh & kadar peak season | `peak.windows` — `["mula","tamat"]`; elemen ke-4 = % khusus tetingkap itu (contoh 20% Krismas) |
| Add-on tempoh perjalanan 2027 | `extraSurcharge` |
| Last-minute surcharge | `variants[].lastMinute` — `lt` = hari, `rate2` = 2 pax, `rate3` = 3 pax ke atas |
| Single supplement | `variants[].single` |
| Harga infant | `variants[].infant` |
| Deposit | `deposit` |
| Harga optional activity | `addons` — `["Nama", hargaDewasa, hargaKanak, "pax"]` |
| Kadar transport hari tambahan | `variants[].ext.rates.day` |
| Kadar tolak transport dari katalog | `variants[].ext.rates.dayDed` |
| Kadar malam tambahan ikut kelas hotel | `variants[].ext.rates.nAirbnb` / `nMotel` / `n3air` / `n3cbd` / `n4cbd` / `n5cbd` |
| Kadar tolak malam | `variants[].ext.rates.dedNight` / `dedNightCbd` / `nightShort` |
| Sektor flight domestik | `variants[].ext.rates.fltaklchc` dan seterusnya |
| Airport shuttle ST | `variants[].ext.rates.shuttle` (sehala) / `shuttle2` (pergi balik) |
| Blok itinerary dalam dropdown | `library` |
| Nota ikut saiz group | `paxNotes` |

### Bentuk kadar

```json
{"from": 2, "to": 3, "normal": 2300, "peak": 2300}
```

`from`–`to` = **kapasiti kenderaan**, bukan bilangan pax tepat. Padanan ambil julat
**pertama** yang muat, jadi rate sheet yang bertindih (2–3, 3–4, 4–5, 5–6) berkelakuan
betul: 3 pax → band 2–3, 4 pax → band 3–4, 5 pax → band 4–5, 6 pax → band 5–6.

`"normal": null` bermaksud **kadar belum diisi** — kalkulator akan papar cip merah
`kadar?` dan baris amaran, bukan RM 0. Ia sengaja begitu untuk kadar yang memang
tiada dalam rate sheet. Isi nombor sebenar bila PO dah dapat dari operator.

### Kawasan (region) &mdash; berlabuh pada BANDAR

New Zealand **tiada ProdReq**, jadi kadar ikut kawasan diambil dari rate sheet
*Simple Customisation New Zealand* (lihat tab Simple Customisation dalam KB).
Rate sheet itu menyenaraikan accommodation ikut **bandar**, dikumpulkan dalam tiga
kumpulan harga. Jadi `region` setiap hari ialah **bandar tempat customer bermalam**,
bukan label pulau &mdash; kos berlabuh pada itinerary sebenar dan cip pada baris hari
membaca "[Queenstown]", bukan "[South Island]".

| Kumpulan harga | Bandar dalam kumpulan itu |
|---|---|
| North Island | Auckland &middot; Rotorua &middot; Hamilton &middot; Taupo &middot; Wellington |
| South Island | Christchurch &middot; Dunedin &middot; Wanaka &middot; Cromwell &middot; Omarama &middot; Franz Josef &middot; Timaru |
| Twizel / Te Anau / Queenstown | Twizel &middot; Te Anau &middot; Queenstown (rate sheet: "harga **hanya** untuk 3 lokasi ini") |

Contoh kesannya &mdash; malam tambahan hotel 4&#9733; CBD, musim peak:
Auckland RM450 &middot; Christchurch RM500 &middot; Queenstown RM800 per pax per malam.

Dalam `calc-config.json`, setiap kunci kadar ada satu entri bagi **setiap bandar**
(nilai sama untuk bandar dalam kumpulan yang sama), campur tiga kunci kumpulan
(`[North Island]`, `[South Island]`, `[Twizel/Te Anau/Queenstown]`) yang dipakai oleh
blok "Hari tambahan" generik. Nak tukar harga satu kumpulan: tukar nilai pada
**semua bandar** dalam kumpulan itu.

- **PT** transport + driving guide: **satu kadar kebangsaan** (rate sheet tidak
  bezakan pulau) &mdash; jadi ia duduk bawah `_default`.
- **ST** kereta sewa: **berbeza North vs South** &mdash; diselesaikan dari bandar hari itu.

### Makan

Katalog NZ **tidak** termasuk sebarang breakfast (katalog ST: "Exclude Breakfast,
lunch and dinner"). Jadi setiap hari default `meal: "none"`, kecuali dua lunch yang
memang tersiar dalam katalog PT: Welcome Lunch (Hari 1) dan lunch High Country
Salmon Farm. `Breakfast` disenaraikan dalam Exclusions.

## Yang PO kena tahu

- Kadar malam tambahan ikut kelas hotel: rate sheet **hanya** siarkan lajur *peak*.
  Untuk normal season kadarnya `null` (papar "kadar belum diisi"). Pilihan
  *Malam tambahan (kadar pakej)* tetap guna kadar rata `variants[].ext.night`.
- Lajur *Tolak 1 Night (Peak)* juga kosong dalam rate sheet — kalkulator guna kadar
  normal untuk peak. Sahkan dengan operator kalau berbeza.
- Kadar transport ST rate sheet setakat 5–6 pax. Untuk 7 pax ke atas kalkulator
  darab dengan bilangan kereta dan papar nota supaya PO sahkan dahulu.


## Bagaimana quotation PDF dibina

Bahagian **PROPOSED ITINERARY** dan **PACKAGE INCLUSIONS** dijana daripada itinerary
yang TC bina, bukan teks tetap. Ini yang perlu PO tahu bila mengedit `calc-config.json`:

| Medan | Kesan dalam PDF |
|---|---|
| `variants[].itin[].eact` | senarai butiran hari (Inggeris). **Jangan** letak aktiviti optional di sini &mdash; add-on yang customer benar-benar beli ditambah sendiri oleh enjin sebagai "... (optional activity)". Aktiviti optional untuk rujukan TC duduk dalam `act` (Melayu). |
| `trpOptions[].lbl` &middot; `accOptions[].hotel` | teks lajur Transport / Accommodation |
| `trpOptions[].incl` &middot; `accOptions[].incl` | baris **Inclusions** yang dijana; `{days}` diganti dengan hari yang benar-benar guna pilihan itu |
| `"{auto}"` dalam `variants[].inclusions` | tempat baris dijana itu disisipkan |
| `line` | label baris dalam jadual harga & baris "Price per pax already includes" |

Sebab ia dijana: bila TC tolak driving guide pada satu hari, baris inclusions
turut gugurkan hari itu sendiri &mdash; PDF tidak lagi menjanjikan sesuatu yang
sudah ditolak daripada harga. Hari flight domestik berlabel **Domestic Flight**
(bukan Airport Transfer), dan malam tambahan memaparkan kelas hotel sebenar
(contoh "5-Star Hotel (CBD)"), bukan kelas hotel pakej.

**Had yang masih ada:** enjin menjana inclusions daripada pilihan **Transport**
dan **Accommodation** sahaja, belum daripada **Meal**. Jadi bila TC guna
*tolak Welcome Meal* atau *tolak lunch Salmon Farm*, baris
"Welcome Lunch 1x & lunch at High Country Salmon Farm" masih kekal dalam
Inclusions &mdash; tolakan itu tetap kelihatan dalam baris
"Price per pax already includes", tetapi sahkan dengan customer secara manual
sehingga ini diperbaiki.

---

**Kalau minta Claude bina semula KB ini, sebut yang `calc-config.json` sudah diedit
di GitHub** — supaya suntingan PO ditarik dahulu dan tidak ditimpa.

Dibina dengan skill `kb-calculator` (baseline penuh Korea). Untuk kemas kini
`index.html`: ganti fail, commit, push — GitHub Pages deploy sendiri.
