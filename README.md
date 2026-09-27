# ARBA PT Knowledge Base House

Satu tempat untuk semua KB (TC Reference) Private Tour ARBA.

- Hub: https://prod-at22.github.io/pt-kb-house/
- Setiap destinasi: `https://prod-at22.github.io/pt-kb-house/<destinasi>/` (senarai dalam `destinations.json`)

## Macam mana ia dikemas kini
Repo KB asal (contoh `arba-bali-kb`) kekal sebagai sumber. GitHub Action `sync.yml` salin
`index.html` + `calc-config.json` dari setiap repo ke folder destinasi di sini **setiap jam**
(atau tekan *Run workflow* di tab Actions untuk sync segera).

Tambah destinasi baru: tambah satu baris dalam `destinations.json`, dan tambah kad dalam `index.html`.
