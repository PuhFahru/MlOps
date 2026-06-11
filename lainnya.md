## Tips

Berikut beberapa tips yang perlu Anda perhatikan.

1. Pastikan Anda menyiapkan virtual environment baru yang berbeda dengan proyek lainnya dan menggunakan TFX dengan versi yang sama seperti yang digunakan ketika latihan membuat machine learning pipeline. Hal ini dilakukan untuk menghindari adanya masalah terkait dependency tools atau library yang digunakan.

2. Anda dapat menggunakan platform Railway sebagai alternatif dari Heroku.

## Ketentuan Pengiriman Submission

Berikut merupakan beberapa poin yang perlu diperhatikan ketika mengirimkan submission.

1. Berkas submission yang dikirim merupakan folder proyek pengembangan machine learning pipeline sederhana menggunakan TFX dan dikirim dalam bentuk ZIP. Ia mengandung beberapa berkas seperti berikut.

- Sebuah direktori yang memuat seluruh komponen machine learning pipeline dengan nama fahrual_19-pipeline.
- File Jupyter Notebook (.ipynb). Pastikan file jupyter notebook sudah dijalankan ya.
- Berkas Python (.py).
- Berkas requirements.txt.
- Berkas Markdown (.md).
- Sebuah berkas Dockerfile untuk menjalankan sistem machine learning pada environment cloud.
- Screenshot bukti keberhasilan dalam menjalankan sisitem machine learning pada environment cloud dengan nama fahrual_19-deployment.
- Sebuah direktori bernama monitoring yang memuat semua kebutuhan untuk menjalankan Prometheus.
  - Sebuah berkas Dockerfile untuk menjalankan Prometheus.
  - Sebuah berkas prometheus.config.
  - Sebuah berkas prometheus.yml.
  - Screenshot dashboard monitoring dengan nama fahrual_19-monitoring.

- Jika Anda menerapkan saran kedua, lampirkan juga sebuah direktori bernama modules yang berisi seluruh modul yang digunakan untuk membuat machine learning pipeline. Selain itu, Anda juga perlu melampirkan screenshot hasil penilaian terhadap seluruh code yang terdapat pada direktori modules menggunakan pylint dengan nama fahrual_19-pylint.

- Apabila Anda menerapkan saran ketiga, lampirkan juga berkas notebook yang digunakan untuk menguji dan melakukan prediction request ke sistem machine learning yang telah dijalankan di cloud. Berkas notebook ini harus bernama fahrual_19-testing.ipynb.

- Jika Anda menerapkan saran keempat, lampirkan sebuah screenshot dashboard yang dijalankan menggunakan Grafana dengan nama fahrual_19-grafana-dashboard.

## Format Berkas Submission

Berkas submission yang dikirimkan merupakan sebuah folder yang disimpan dalam bentuk ZIP. Folder berisi beberapa berkas seperti berikut.

1. Direktori yang memuat komponen machine learning pipeline.

2. Berkas Jupyter Notebook (.ipynb), module transform (.py), module trainer (.py), dan Markdown (.md).

3. Direktori yang berisi serving model.

4. Berkas requirements.txt.

5. Direktori yang memuat seluruh kebutuhan untuk menjalaankan tahap monitoring sistem machine learning.

Pastikan Anda tidak melakukan ZIP dalam ZIP.


