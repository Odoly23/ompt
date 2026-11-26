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
