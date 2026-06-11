# Submission 2: Pipeline dan Deployment Klasifikasi Spesies Iris
Nama: Fahru Alfarizi Hananza Putrawan

Username dicoding: fahrual_19

| | Deskripsi |
| ----------- | ----------- |
| Dataset | Iris Dataset. Dataset ini berisi 150 data bunga Iris dengan 4 fitur numerik, yaitu `sepal_length`, `sepal_width`, `petal_length`, dan `petal_width`. Target prediksi adalah `species` dengan tiga kelas: setosa, versicolor, dan virginica. Dataset disimpan pada `data/iris.csv`. |
| Masalah | Proyek ini menyelesaikan masalah klasifikasi spesies bunga Iris berdasarkan ukuran sepal dan petal. Sistem diharapkan dapat memprediksi spesies Iris secara otomatis dari data fitur numerik. |
| Solusi machine learning | Solusi dibuat sebagai pipeline machine learning end-to-end menggunakan TensorFlow Extended (TFX). Pipeline menjalankan tahap ingestion data, validasi data, transformasi fitur, training model, evaluasi model, dan push model ke direktori serving. |
| Metode pengolahan | Fitur numerik diproses menggunakan TensorFlow Transform dengan standardisasi z-score melalui `tft.scale_to_z_score`. Label `species` digunakan sebagai target klasifikasi multi-kelas. |
| Arsitektur model | Model menggunakan neural network sederhana berbasis Keras. Empat fitur hasil transformasi digabungkan, lalu diproses oleh dense layer 16 neuron dan 8 neuron dengan aktivasi ReLU. Output layer terdiri dari 3 neuron dengan aktivasi softmax. |
| Metrik evaluasi | Metrik utama yang digunakan adalah `SparseCategoricalAccuracy`. Pipeline juga mencatat `ExampleCount` melalui TensorFlow Model Analysis. Model diberi threshold minimal akurasi 0.5 sebelum dipush. |
| Performa model | Berdasarkan hasil `Evaluator`, model memperoleh `SparseCategoricalAccuracy` sebesar 0.85 dengan `loss` 0.4116 pada 60 data evaluasi. Model berhasil memperoleh blessing dan dipush ke `serving_model/1781073761`. |
| Opsi deployment | Deployment menggunakan Docker dan TensorFlow Serving. Model disajikan sebagai service bernama `iris-model` dan dideploy ke Railway. |
| Web app | [iris-model Railway metadata](https://mlops-production-cf92.up.railway.app/v1/models/iris-model/metadata) |
| Monitoring | Monitoring menggunakan Prometheus. TensorFlow Serving menyediakan endpoint metrik `/monitoring/prometheus/metrics`, dan Prometheus berhasil membaca target `tensorflow-serving` dengan status `UP`. |
