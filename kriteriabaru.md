## Kriteria 1: Menggunakan TensorFlow Extended (TFX) untuk Membuat Machine Learning Pipeline

Mirip seperti materi latihan sebelumnya, Anda harus membuat machine learning pipeline sederhana menggunakan TensorFlow Extended (TFX). Machine learning pipeline yang Anda buat harus memuat seluruh komponen yang dibutuhkan seperti berikut.

1. ExampleGen
2. StatisticGen
3. SchemaGen
4. ExampleValidator
5. Transform
6. Trainer
7. Resolver
8. Evaluator
9. Pusher

Seluruh komponen di atas harus dijalankan menggunakan Pipeline Orchestrator bernama Apache Beam dan disimpan dalam sebuah folder bernama fahrual_19-pipeline.

## Kriteria 2: Melampirkan Dokumentasi Proyek

Pada proyek ini, Anda menggunakan text cell pada notebook (.ipynb) untuk menjelaskan setiap tahapan proyek dan berkas Markdown untuk menjelaskan proyek secara keseluruhan. Berikut merupakan beberapa informasi yang harus ada dalam dokumentasi yang Anda buat.

1. Informasi terkait dataset yang digunakan.
2. Informasi tentang persoalan yang ingin diselesaikan.
3. Penjelasan terkait solusi machine learning yang akan dibuat beserta target yang ingin dicapai.
4. Penjelasan tentang metode pengolahan data, arsitektur model yang digunakan, dan metrik untuk mengevaluasi performa model.
5. Informasi terkait performa model machine learning yang telah dibuat.
6. Penjelasan singkat tentang opsi model deployment beserta platform yang digunakan.
7. Tautan web app yang digunakan untuk mengakses model serving.
8. Penjelasan singkat tentang hasil monitoring yang diperoleh.

Berikut merupakan template dokumentasi yang dapat Anda gunakan: format-dokumentasi.md yang ada di file folder ini.

## Kriteria 3: Menjalankan Sistem Machine Learning Menggunakan Komputasi Cloud

Pada proyek ini, Anda harus mampu menjalankan sistem machine learning pada environment cloud. Anda telah berhasil menjalankan tahapan ini pada salah satu latihan di kelas ini. Pada latihan tersebut kita menggunakan Heroku sebagai platform cloud untuk menjalankan sistem machine learning. Kini saatnya Anda menerapkan pengetahuan tersebut ke dalam sebuah proyek submission ini.

## Kriteria 4: Memantau Sistem Machine Learning Menggunakan Prometheus

Setelah menjalankan sistem machine learning di cloud, selanjutnya Anda wajib memonitor sistem tersebut dengan menjalankan Prometheus. Sebelumnya, Anda telah berhasil menjalankan proses ini pada salah satu latihan di kelas ini. Jadi, cobalah untuk menerapkannya pada proyek submission.

![alt text](image.png)
![alt text](image.png)