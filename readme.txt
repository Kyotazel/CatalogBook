Cara Menggunakan Database dan Environtment
    1. Buat database catalogbook
    2. Import CatalogBook.sql pada phpmyadmin
    3. Install virtualenv dengan pip install vitualenv
    4. buat virtualenv dengan virtualenv namaenv
    5. aktivasi Environtment dengan "nama/Scripts/activate" pada terminal
    6. Install flask dan flask_mysqldb dengan pip install flask flask_mysqldb
    7. Ubah database pada app.config sesuai database yang digunakan
    8. Ketikkan perintah python app.py untuk menjalankan
    9. Cek localhost:5000 pada browser

Cara Menggunakan Login:
    1. Register terlebih dahulu
    2. Login menggunakan akun yang telah di Register
    3. Logout apabila tidak digunakan

Cara Menggunakan CRUD (login terlebih dahulu)
    1. Tambahkan data (create)
    2. Setelah ditambahkan akan redirect ke list (read)
    3. Edit dan Hapus sesuai keinginan

Akses Guest:
    1. List-Buku (Tanpa Create Update Delete)
    2. Halaman Login
    3. Halaman Signup

Akses Login:
    1. List Buku (Dengan CRUD)
    2. Tambahkan data
    3. Edit data
    4. Hapus Data