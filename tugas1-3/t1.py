import tree_sitter_python as tspython
from tree_sitter import Language, Parser

parser = Parser(Language(tspython.language()))

POTONGAN = {
    "fungsi": b"def sapa(nama):\n    return 'halo ' + nama\n",
    "if_else": b"if x > 0:\n    y = 1\nelse:\n    y = 2\n",
    "kelas": b"class Hewan:\n    def bicara(self):\n        return 'suara'\n",
    "rusak_tanpa_titik_dua": b"def sapa(nama)\n    return nama\n",
    "rusak_tanpa_kurung_tutup": b"print(1 + 2\n",
}

for judul, kode in POTONGAN.items():
    tree = parser.parse(kode)
    print(f"=== {judul} (has_error={tree.root_node.has_error}) ===")
    print(tree.root_node)
    print()

# Node anonim vs bernama pada potongan fungsi
tree = parser.parse(POTONGAN["fungsi"])
fn = tree.root_node.children[0]
print("--- children dari function_definition ---")
for c in fn.children:
    print(c.type, "bernama" if c.is_named else "anonim")
print("--- children dari parameters ---")
for c in fn.child_by_field_name("parameters").children:
    print(c.type, "bernama" if c.is_named else "anonim")
print("len(children) =", len(fn.children), "| len(named_children) =", len(fn.named_children))

# Cari ERROR / MISSING
def cari(node):
    if node.type == "ERROR" or node.is_missing:
        print("ditemukan:", "MISSING" if node.is_missing else "ERROR", repr(node.type), node.start_point)
    for c in node.children:
        cari(c)

print("--- ERROR/MISSING ---")
for judul in ("rusak_tanpa_titik_dua", "rusak_tanpa_kurung_tutup"):
    print(judul)
    cari(parser.parse(POTONGAN[judul]).root_node)
