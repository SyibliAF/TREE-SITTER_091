# cek.py: pemeriksa kode Python berbasis tree-sitter

Melaporkan tiga hal pada semua file `*.py` dalam sebuah folder:

1. komentar `TODO` / `FIXME` (query `(comment)` + `#match?`, jadi `TODO` di dalam string tidak ikut),
2. fungsi/method lebih dari 30 baris (semua fungsi dihitung, termasuk method kelas dan fungsi bersarang),
3. file yang pohonnya mengandung `ERROR`/`MISSING`, beserta baris pertama yang bermasalah.

Folder `venv/`, `.venv/`, `.git/`, `node_modules/`, `__pycache__/` dilewati.

## Pasang dan jalankan

```bash
pip install tree-sitter tree-sitter-python
python cek.py uji/
```

## Contoh output (folder `uji/`)

```
cek\uji\ada_todo.py:1: TODO: # TODO: tambahkan validasi
cek\uji\ada_todo.py:2: TODO: # FIXME: angka ajaib
cek\uji\panjang.py:5: FUNGSI PANJANG: panjang (37 baris)
cek\uji\rusak.py:1: SINTAKS RUSAK (ERROR)
```

Contoh pada repo nyata (`pallets/itsdangerous`): lihat `output_itsdangerous.txt`.
Hasil dicocokkan manual pada `timed.py` (`unsign` baris 72-158 = 87 baris; satu-satunya TODO di baris 182)
dan `signer.py` (`derive_key` baris 182-213 = 32 baris).
