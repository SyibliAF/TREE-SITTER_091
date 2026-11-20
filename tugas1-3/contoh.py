"""Modul contoh untuk Tugas 3."""
import os
import sys as system
from pathlib import Path
from collections import OrderedDict, defaultdict


def tambah(a, b):
    """Menjumlahkan dua angka."""
    return a + b


def kali(a, b, c=1):
    print(a, b)
    return a * b * c


def tanpa_param():
    print("halo")
    print()


class Kalkulator:
    def bagi(self, x, y):
        return x / y

    @staticmethod
    def pangkat(x, n):
        return x ** n
