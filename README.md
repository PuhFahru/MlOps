# Submission 2: Pipeline dan Deployment Klasifikasi Spesies Iris
Nama: Fahru Alfarizi Hananza Putrawan

Username dicoding: fahrual_19

| | Deskripsi |
| ----------- | ----------- |
| Dataset | Iris Dataset. Dataset berisi 150 data bunga Iris dengan 4 fitur numerik: panjang sepal, lebar sepal, panjang petal, dan lebar petal. Target prediksi adalah spesies Iris dengan tiga kelas, yaitu setosa, versicolor, dan virginica. Dataset disimpan pada `data/iris.csv`. |
| Masalah | Proyek ini menyelesaikan masalah klasifikasi spesies bunga Iris berdasarkan ukuran sepal dan petal. Model diharapkan mampu mengenali pola fitur numerik dan memprediksi kelas spesies secara otomatis. |
| Solusi machine learning | Solusi dibuat sebagai sistem machine learning end-to-end menggunakan TensorFlow Extended (TFX). Pipeline membaca data CSV, menghitung statistik data, membuat schema, memvalidasi anomali, melakukan transformasi fitur, melatih model Keras, mengevaluasi performa model, dan mendorong model yang lolos evaluasi ke direktori serving. Pipeline dijalankan menggunakan Apache Beam melalui `pipeline.py`. |
| Metode pengolahan | Empat fitur numerik diproses menggunakan TensorFlow Transform dengan standardisasi z-score melalui `tft.scale_to_z_score`. Label `species` dikonversi ke integer dan digunakan sebagai target klasifikasi multi-kelas. |
| Arsitektur model | Model menggunakan neural network sederhana berbasis Keras. Empat input fitur hasil transformasi digabungkan, lalu diproses oleh dua dense layer berukuran 16 dan 8 neuron dengan aktivasi ReLU. Output layer memiliki 3 neuron dengan aktivasi softmax untuk menghasilkan probabilitas kelas. |
| Metrik evaluasi | Metrik utama adalah `SparseCategoricalAccuracy` karena target berupa label integer multi-kelas. Pipeline juga mencatat `ExampleCount` melalui TensorFlow Model Analysis. Model diberi threshold minimal akurasi 0.5 agar dapat memperoleh blessing sebelum dipush. |
| Performa model | Berdasarkan hasil `Evaluator`, model memperoleh `SparseCategoricalAccuracy` sebesar 0.85 dengan `loss` 0.4116 pada 60 data evaluasi. Model berhasil melewati threshold evaluasi dan dipush ke folder `serving_model/1781073761`. |
| Opsi deployment | Deployment menggunakan Docker dan TensorFlow Serving. File `Dockerfile` menyalin model dari `serving_model` ke image TensorFlow Serving dengan nama model `iris-model`. Image ini dapat dijalankan lokal atau dideploy ke Railway sebagai alternatif Heroku. |
| Web app | Endpoint lokal: [iris-model metadata](http://localhost:8501/v1/models/iris-model/metadata). Setelah deployment cloud berhasil, ganti bagian ini dengan URL Railway, misalnya `https://nama-project.up.railway.app/v1/models/iris-model/metadata`. |
| Monitoring | Monitoring menggunakan Prometheus. TensorFlow Serving mengaktifkan endpoint metrik `/monitoring/prometheus/metrics` melalui `monitoring/prometheus.config`, lalu Prometheus membaca endpoint tersebut menggunakan konfigurasi `monitoring/prometheus.yml`. Screenshot monitoring perlu disimpan dengan nama `fahrual_19-monitoring`. |

## Struktur Proyek

```text
.
+-- data/
|   +-- iris.csv
+-- fahrual_19-pipeline/
+-- modules/
|   +-- __init__.py
|   +-- trainer.py
|   +-- transform.py
+-- monitoring/
|   +-- Dockerfile
|   +-- prometheus.config
|   +-- prometheus.yml
+-- serving_model/
+-- Dockerfile
+-- fahrual_19-pipeline.ipynb
+-- fahrual_19-testing.ipynb
+-- pipeline.py
+-- README.md
+-- requirements.txt
```

## Komponen Pipeline

Pipeline TFX memuat komponen berikut.

1. `CsvExampleGen`
2. `StatisticsGen`
3. `SchemaGen`
4. `ExampleValidator`
5. `Transform`
6. `Trainer`
7. `Resolver`
8. `Evaluator`
9. `Pusher`

Seluruh komponen dijalankan menggunakan Apache Beam pada `pipeline.py` dengan pipeline root `fahrual_19-pipeline`.

## Cara Menjalankan Pipeline

Gunakan virtual environment Python 3.10 agar dependency TFX dan TensorFlow kompatibel.

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python pipeline.py
```

Notebook `fahrual_19-pipeline.ipynb` tetap disertakan sebagai dokumentasi tahapan pipeline dan bukti eksekusi interaktif.

Catatan: pada beberapa environment Windows, `BeamDagRunner` TFX 1.14 dapat terkena keterbatasan ML Metadata SQLite terkait filter query. Jika muncul error MLMD saat menjalankan `python pipeline.py`, jalankan pipeline pada WSL, Linux, atau Google Colab dengan dependency yang sama.

## Cara Menjalankan Serving Lokal

Build dan jalankan image TensorFlow Serving.

```bash
docker build -t fahrual-19-iris-serving .
docker run --rm -p 8501:8501 fahrual-19-iris-serving
```

Cek metadata model.

```text
http://localhost:8501/v1/models/iris-model/metadata
```

## Cara Menjalankan Monitoring Lokal

Jalankan TensorFlow Serving terlebih dahulu, lalu jalankan Prometheus.

```bash
cd monitoring
docker build -t fahrual-19-prometheus .
docker run --rm -p 9090:9090 fahrual-19-prometheus
```

Buka Prometheus pada:

```text
http://localhost:9090
```

Target dapat dicek melalui menu `Status > Targets`.

## Cara Menguji Prediction Request

Jalankan notebook:

```text
fahrual_19-testing.ipynb
```

Notebook tersebut mengirim request ke endpoint `http://localhost:8501/v1/models/iris-model:predict`. Jika model sudah dideploy ke cloud, ubah variabel `MODEL_URL` menjadi URL cloud.

## Berkas Screenshot yang Perlu Disertakan

Setelah deployment dan monitoring berhasil dijalankan, simpan screenshot berikut sebelum membuat ZIP submission.

1. `fahrual_19-deployment.png`: bukti endpoint model serving di cloud berhasil diakses.
2. `deployment/fahrual_19-deployment-lokal.png`: bukti endpoint model serving lokal berhasil diakses.
3. `monitoring/fahrual_19-monitoring.png`: bukti dashboard Prometheus berjalan dan target TensorFlow Serving terbaca.
