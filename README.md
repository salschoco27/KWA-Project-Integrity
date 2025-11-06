# KWA Integrity Detection
Kelas Keamanan Web dan Aplikasi Kelas A

 Anggota Kelompok:
 - Revalina Fairuzy Azhari Putri (5027231001)
 - Chelsea Vania Hariyono (5027231003)
 - Salsabila Rahmah (5027231005)
 - Farida Qurrotu A'yuna (5027231015)
 - Nayyara Ashila (5027231083)

 ## Cara Menjalankan Program
 1. Buat struktur folder sebagai berikut
 ```
 project_integrity/
│
├── secure_files/
│   ├── data.txt
│   └── config.json
│
├── hash_db.json
├── security.log
├── monitor.py
└── app.py

 ```
 **Notes!** <br>
 - hash_db.json dan security.log akan ter-generate setelah menjalankan monitor.py <br>
 - Isi semua file dalam folder secure_files bebas
 2. Jalankan monitor.py
 ```
 python monitor.py
 ```
 3. Buka terminal baru dan jalankan app.py
 ```
 python app.py
 ```
 4. Lakukan percobaan dengan mengubah, menambahkan, maupun menghapus isi atau file itu sendiri dalam folder secure_files dan jalankan kembali monitor.py.

 5. Refresh pada website untuk menampilkan versi terbaru.

 # Dokumentasi Pengerjaan

 Sistem ini diimplementasikan melalui script `monitor.py` yang bertugas sebagai *File Integrity Monitor*. Mekanisme pemantauan mencakup deteksi terhadap tiga jenis anomali utama sesuai dengan perintah soal:
 
 | Anomali | Mekanisme Deteksi | Level Log |
| :--- | :--- | :--- |
| **File Diubah (Modified)** | Membandingkan Hash SHA-256 saat ini dengan Hash Baseline di `hash_db.json`. | **WARNING** |
| **File Dihapus (Deleted)** | File yang ada di `hash_db.json` tidak ditemukan di direktori. | **ALERT** |
| **File Ditambahkan (Added)** | File baru ditemukan di direktori yang tidak ada di `hash_db.json`. | **ALERT** |

Setiap kasus deteksi anomali telah berhasil diuji dan dicatat dalam bagian **Dokumentasi Pengerjaan** di bawah.

# Case 1: Mengubah salah satu isi file
 Salah satu file yang sudah ada dalam baseline hash, misalnya `data.txt`, diubah isinya.

 ## Hasil Deteksi:
- Deteksi Integritas: Ketika `monitor.p`y dijalankan kembali, sistem menghitung ulang hash `data.txt` dan menemukan bahwa hash baru berbeda dengan baseline yang tersimpan di hash_db.json.
- Logging: Perbedaan hash ini dicatat ke dalam `security.log` dengan level WARNING, yang secara spesifik menunjukkan bahwa integritas file telah gagal diverifikasi (File "data.txt" integrity failed!).
- Antarmuka Web: Antarmuka web yang dijalankan oleh ``app.py memperbarui metriknya. Terlihat adanya peningkatan pada "Jumlah File Rusak/Terganggu" dan pembaruan pada "Waktu Terakhir Ada Anomali" sesuai dengan timestamp log WARNING yang baru.
  
 ![alt text](image.png)
 ![alt text](image-1.png)
Output: Sistem berhasil mendeteksi perubahan konten file secara granular melalui perbandingan hash dan mencatatnya sebagai WARNING (Pelanggaran Integritas).

# Case 2: Menghapus salah satu file
File yang sebelumnya ada dan tercatat dalam baseline hash (hash_db.json), seperti `test.txt` dalam contoh ini, dihapus dari folder secure_files/.

## Hasil Deteksi:
- Deteksi Integritas: Saat `monitor.py` dieksekusi, sistem memeriksa setiap entri dalam hash_db.json. Ketika mencoba menemukan `test.txt` di direktori dan gagal, sistem menginterpretasikannya sebagai penghapusan yang tidak sah.
- Logging: Kejadian ini dicatat ke dalam security.log dengan level keamanan yang lebih tinggi, yaitu ALERT, karena penghapusan adalah aktivitas yang sangat mencurigakan (ALERT: Baseline file "test.txt" is missing.).
- Antarmuka Web: Antarmuka monitoring menampilkan hasil ini dengan jelas. Metrik "Jumlah File Rusak/Terganggu" diperbarui, dan "Waktu Terakhir Ada Anomali" mencerminkan timestamp log ALERT yang baru.
  
Dalam kasus ini, file yang dihapus adalah test.txt
 ![alt text](image-2.png)
 ![alt text](image-3.png)

Output: Sistem berhasil mendeteksi penghilangan file yang menjadi bagian dari baseline dan mencatatnya sebagai ALERT (Aktivitas Mencurigakan: File Hilang).

# Case 3: Menambahkan file baru (File Addition/Unknown File) "new.txt"
Sebuah file baru, misalnya `new.txt`, ditambahkan ke dalam folder secure_files/ tanpa terdaftar sebelumnya di hash_db.json.

# Hasil Deteksi:
- Deteksi Integritas: Ketika `monitor.py` berjalan, sistem memindai folder secure_files/. File `new.txt` ditemukan, namun tidak ada entry yang sesuai di dalam hash_db.json. Ini diidentifikasi sebagai penambahan file yang tidak diketahui (Unknown File).
- Logging: Penemuan file asing ini dicatat ke dalam security.log dengan level ALERT (ALERT: Unknown file "new.txt" detected.), menandakan potensi malware atau file yang disuntikkan.
- Antarmuka Web: Sama seperti kasus sebelumnya, metrik "Jumlah File Rusak/Terganggu" dan "Waktu Terakhir Ada Anomali" diperbarui untuk mencerminkan insiden ALERT penambahan file baru ini.

 ![alt text](image-4.png)
 ![alt text](image-5.png)

Output: Sistem berhasil mengidentifikasi adanya file baru yang tidak termasuk dalam baseline yang sah dan mencatatnya sebagai ALERT (Aktivitas Mencurigakan: File Asing Terdeteksi).

 ### Isi dari security.log
 ![alt text](image-6.png)
