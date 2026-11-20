"""cek.py <folder>: lapor TODO/FIXME, fungsi > 30 baris, dan file Python dengan error sintaks."""
import sys
from pathlib import Path
import tree_sitter_python as tspython
from tree_sitter import Language, Parser, Query, QueryCursor

PY = Language(tspython.language())
parser = Parser(PY)

BATAS_BARIS = 30
ABAIKAN = {"venv", ".venv", ".git", "node_modules", "__pycache__"}

Q_TODO = Query(PY, '((comment) @c (#match? @c "TODO|FIXME"))')
Q_FUNGSI = Query(PY, "(function_definition name: (identifier) @nama) @fungsi")


def node_error_pertama(node):
    """Node ERROR/MISSING pertama (urutan dokumen), atau None."""
    if node.type == "ERROR" or node.is_missing:
        return node
    for child in node.children:
        if child.has_error or child.is_missing:
            hasil = node_error_pertama(child)
            if hasil is not None:
                return hasil
    return None


def cek_file(path):
    tree = parser.parse(path.read_bytes())
    root = tree.root_node

    # Fitur 1: komentar TODO/FIXME
    for node in QueryCursor(Q_TODO).captures(root).get("c", []):
        print(f"{path}:{node.start_point[0] + 1}: TODO: {node.text.decode(errors='replace').strip()}")

    # Fitur 2: fungsi lebih dari BATAS_BARIS baris (termasuk method dan fungsi bersarang)
    for _, cap in QueryCursor(Q_FUNGSI).matches(root):
        fungsi = cap["fungsi"][0]
        jumlah = fungsi.end_point[0] - fungsi.start_point[0] + 1
        if jumlah > BATAS_BARIS:
            nama = cap["nama"][0].text.decode(errors="replace")
            print(f"{path}:{fungsi.start_point[0] + 1}: FUNGSI PANJANG: {nama} ({jumlah} baris)")

    # Fitur 3: file dengan error sintaks
    if root.has_error:
        err = node_error_pertama(root)
        baris = err.start_point[0] + 1 if err else "?"
        jenis = "MISSING " + err.type if err is not None and err.is_missing else "ERROR"
        print(f"{path}:{baris}: SINTAKS RUSAK ({jenis})")


def main():
    if len(sys.argv) != 2:
        sys.exit("pemakaian: python cek.py <folder>")
    for path in sorted(Path(sys.argv[1]).rglob("*.py")):
        if ABAIKAN.intersection(path.parts):
            continue
        cek_file(path)


if __name__ == "__main__":
    main()
