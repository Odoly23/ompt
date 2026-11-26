# Website OPMT — Organização Popular da Mulher Timor

Website resmi OPMT (organisasi perempuan FRETILIN, berdiri 28 Agustus 1975), dalam empat bahasa: **Tetun (default), Português, Bahasa Indonesia, English**.

| Bagian | Teknologi | Folder |
|---|---|---|
| API | Django 5 + Django REST Framework + JWT (SimpleJWT) | `backend/` |
| Panel admin | Template Django HTML + CSS + Bootstrap 4 | `backend/panel/` → `/panel/` |
| Website publik | Vue 3 + Vite + Vue Router + Pinia + vue-i18n | `frontend/` |

## Isi website

- **Istória**: linha tempu 1975–2025, figura/eroína, dan daftar 7 Sekretária-Jeral
- **Lideransa**: órgaun nasionál menurut Estatutu (Art. 19–25) dan pengurus saat ini
- **Atividade & programa**: kegiatan dan sub-programa yang sedang berjalan
- **Notísia, galeri, dokumentu** (Estatutu OPMT 2016/2021, poster pameran "Buibere Hamrik")
- **Estrutura**: peta 13 munisípiu + RAEOA beserta postu administrativu
- **Sai membru**: pendaftaran online (umur ≥16 dan setuju Estatutu, Art. 6), login JWT, dashboard anggota, kartu anggota digital
- **Kontaktu**: formulir pesan yang masuk ke panel
- **Slider beranda**: slide pertama adalah desain poster "Buibere Hamrik"; slide berikutnya dikelola di **Panel → Slide sira** (judul, teks, tombol, link, gambar, warna tema, urutan, aktif/nonaktif — 4 bahasa). Autoplay 7 detik, berhenti saat disentuh/di-hover/fokus, tombol jeda, panah, titik, swipe, dan keyboard
- **Animasi scrolling**: konten muncul bertahap saat di-scroll (`v-reveal`), progress bar di atas layar, efek parallax pada ilustrasi poster, garis linimasa Istória yang tergambar mengikuti scroll, serta slider horizontal "Momentu boot". Semua animasi otomatis mati jika pengguna memilih *reduce motion* di perangkatnya

Data awal diambil dari dokumen yang dikirim Filomena de Almeida (OPMT, 17 Okt 2025): *Perfil OPMT no atividades*, *Estatutos da OPMT*, dan poster pameran. Data yang belum dikonfirmasi (pengurus saat ini, koordinator munisípiu, jumlah anggota) ditandai **dadus ezemplu** dan ditampilkan di dashboard panel sampai diganti.

## Fitur organisasi (v3)

| Fitur | Untuk siapa | Di mana |
|---|---|---|
| **Kartu anggota QR** | Anggota aktif mendapat kartu digital ber-QR (bisa diunduh sebagai PNG). Siapa pun yang memindai QR dengan kamera HP melihat halaman verifikasi `/verifika/<token>` (nama, nomor, munisípiu, status, kuota lunas/belum) | Website → Ha'u-nia konta |
| **Agenda & pendaftaran acara** | Publik/anggota daftar ikut acara (tamu cukup nama + telepon/email), batal daftar, unduh `.ics` ke kalender. Acara bisa dibatasi kapasitas atau khusus anggota | Website → Agenda; Panel → Agenda |
| **Check-in QR** | Petugas membuka **Panel → Scan QR**, pilih acara, scan kartu dengan kamera HP/laptop (BarcodeDetector atau jsQR) atau ketik nomor anggota. Anggota yang datang tanpa daftar otomatis ditambahkan | Panel → Scan QR / check-in |
| **Memória Buibere** | Arsip kisah perempuan pejuang: teks, foto, audio, video YouTube. Publik bisa mengirim kisah (wajib izin pencerita); kisah tampil setelah status diubah ke *Publika ona* di panel | Website → Memória Buibere; Panel → Memória Buibere |
| **Admin per munisípiu** | Akun koordinator munisípiu hanya melihat dan mengelola anggota, kegiatan, acara, pendaftaran, kuota, pengumuman, kisah, dan pos administratif di wilayahnya. Halaman sejarah, konfigurasi, dan Ekipa hanya untuk tim nasional | Panel → Ekipa panel |
| **Dashboard statistik** | Anggota per munisípiu, umur, pertumbuhan 13 bulan, kegiatan per kategori, partisipasi acara, penerimaan kuota. Ekspor Excel (anggota, kuota, peserta acara) dan versi cetak/PDF | Panel → Estatístika |
| **Iuran (kuota)** | Tarif per tahun (Estatutu Art. 22 j), catat pembayaran, laporan tunggakan dengan input cepat, riwayat kuota di akun anggota | Panel → Relatóriu kuota |
| **Pengumuman email/SMS** | Tulis pengumuman → pilih kanal (website, email, SMS, email+SMS), sasaran (anggota aktif/semua, nasional/per munisípiu) → pratinjau jumlah penerima → kirim. Pengumuman juga tampil di akun anggota | Panel → Anúnsiu sira |

### Email dan SMS

Atur di `backend/.env`:

- **Email**: `EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend` + `EMAIL_HOST`, `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`, `DEFAULT_FROM_EMAIL`. Default: dicetak di log (console).
- **SMS**: `SMS_BACKEND=console` (default, hanya log) atau `SMS_BACKEND=http` untuk gateway bulk SMS (Telkomcel, Timor Telecom, Telemor, atau penyedia lain) dengan `SMS_HTTP_URL`, `SMS_HTTP_TOKEN`, dan nama field `SMS_HTTP_TO_FIELD` / `SMS_HTTP_TEXT_FIELD` / `SMS_HTTP_SENDER_FIELD` sesuai API penyedia. Nomor otomatis dinormalisasi ke format `+670…`.
- **SITE_URL**: alamat website publik; dipakai di QR kartu anggota. Wajib diisi dengan domain asli sebelum kartu dibagikan.

Pengiriman berjalan langsung saat tombol *Haruka* ditekan; cocok untuk ratusan penerima. Untuk ribuan penerima, pindahkan `send_announcement` ke antrean (Celery/RQ).

## Menjalankan backend

```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env          # ubah DJANGO_SECRET_KEY
python manage.py migrate
python manage.py seed_opmt --admin admin@opmt.tl   # isi data awal + buat akun admin
python manage.py runserver
```

- API: `http://localhost:8000/api/v1/`
- Panel admin (Bootstrap 4): `http://localhost:8000/panel/`
- Django admin bawaan (cadangan): `http://localhost:8000/django-admin/`

## Menjalankan frontend

```bash
cd frontend
npm install
npm run dev        # http://localhost:5173 (proxy /api dan /media ke :8000)
npm run build      # hasil di frontend/dist/
```

Untuk produksi, atur `VITE_API_URL` jika API berada di domain lain.

## API

Semua endpoint ada di `/api/v1/`. Bahasa dipilih dengan `?lang=tet|pt|id|en` atau header `Accept-Language` (default Tetun). Pengguna publik menerima field terjemahan (`title`, `body`, …) dalam bahasa yang diminta; staf juga menerima dan bisa menulis kolom mentah (`title_tet`, `title_pt`, …).

| Endpoint | Keterangan |
|---|---|
| `GET site/`, `GET stats/` | Info organisasi dan angka ringkas |
| `slides/` | Slide beranda (yang aktif) |
| `events/{slug}` · `POST events/{slug}/register/` · `POST …/cancel/` · `GET …/ics/` | Agenda (`?when=upcoming|past`) |
| `stories/{slug}` · `POST stories/submit/` · `GET stories/choices/` | Memória Buibere (kirim kisah dibatasi 5/jam) |
| `GET verify/{token}/` | Verifikasi kartu anggota dari QR (publik, dibatasi 60/menit) |
| `GET auth/overview/` | Kartu QR, kuota, acara saya, pengumuman (anggota) |
| `history/`, `figures/{slug}`, `secretaries-general/`, `objectives/` | Sejarah |
| `organs/{code}`, `leaders/` | Struktur dan pengurus |
| `activities/{slug}`, `programs/` | Kegiatan (`?category=&status=&municipality__code=&search=`) |
| `news/{slug}`, `albums/{slug}`, `documents/` | Komunikasi (dokumen non-publik hanya untuk anggota aktif) |
| `municipalities/{code}` | Peta struktur + postu administrativu |
| `POST contact/` | Pesan kontak (dibatasi 10/jam) |
| `POST auth/register/` | Daftar anggota → token JWT |
| `POST auth/login/` | Email + password → `access` + `refresh` |
| `POST auth/refresh/`, `auth/verify/`, `auth/logout/` | Rotasi refresh token + blacklist |
| `GET/PATCH auth/me/`, `POST auth/change-password/`, `GET auth/member-card/` | Akun anggota |

Endpoint tulis (POST/PUT/PATCH/DELETE) pada konten hanya untuk staf (`is_staff`).

## Alur anggota

1. Anggota mendaftar di website, status awal *Hein aprovasaun*.
2. Staf membuka **Panel → Membru** lalu klik **Aprova**; nomor anggota dibuat otomatis (mis. `OPMT-DIL-00001`).
3. Anggota aktif bisa melihat kartu anggota digital dan dokumen internal.

## Struktur folder

```
backend/
  config/        settings, urls
  content/       model konten 4 bahasa, API, seed_opmt, seed_files/
  accounts/      MemberProfile, register/login/me (JWT)
  panel/         panel admin Bootstrap 4
frontend/
  src/views/     halaman publik
  src/i18n/      teks antarmuka tet/pt/id/en
```
