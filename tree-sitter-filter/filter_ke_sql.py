"""[Pengayaan] Ubah pohon DSL filter menjadi klausa WHERE SQL berparameter.

Nilai TIDAK digabung ke string SQL, melainkan dikirim sebagai parameter (?).
Nama kolom divalidasi dengan whitelist karena tidak bisa diparameterkan.
Pemakaian: python filter_ke_sql.py 'status = "open" and priority > 2'
"""
import ctypes
import sys
from pathlib import Path
from tree_sitter import Language, Parser

lib = ctypes.cdll.LoadLibrary(str(Path(__file__).parent / "filter.dll"))
lib.tree_sitter_filter.restype = ctypes.c_void_p
import warnings; warnings.simplefilter("ignore", DeprecationWarning)
FILTER = Language(lib.tree_sitter_filter())
parser = Parser(FILTER)

KOLOM_BOLEH = {"status", "priority", "owner", "title", "archived", "customer.city", "customer.vip", "a", "b", "c"}


def nilai(node):
    teks = node.text.decode()
    if node.type == "string":
        return teks[1:-1]
    if node.type == "number":
        return float(teks) if "." in teks else int(teks)
    return teks == "true"


def kolom(node):
    nama = node.text.decode()
    if nama not in KOLOM_BOLEH:
        raise ValueError(f"kolom tidak diizinkan: {nama}")
    return nama.replace(".", "_")


def ke_sql(node, params):
    t = node.type
    if t == "query":
        return ke_sql(node.named_children[0], params)
    if t == "parenthesized":
        return "(" + ke_sql(node.named_children[0], params) + ")"
    if t in ("and_expression", "or_expression"):
        op = "AND" if t == "and_expression" else "OR"
        kiri = ke_sql(node.child_by_field_name("left"), params)
        kanan = ke_sql(node.child_by_field_name("right"), params)
        return f"({kiri} {op} {kanan})"
    if t == "not_expression":
        return "NOT " + ke_sql(node.child_by_field_name("operand"), params)
    if t == "comparison":
        op = node.child_by_field_name("operator").text.decode()
        op = "<>" if op == "!=" else op
        params.append(nilai(node.child_by_field_name("value")))
        return f"{kolom(node.child_by_field_name('field'))} {op} ?"
    if t == "in_expression":
        vals = node.child_by_field_name("values").named_children
        params.extend(nilai(v) for v in vals)
        return f"{kolom(node.child_by_field_name('field'))} IN ({', '.join('?' * len(vals))})"
    if t == "contains_expression":
        params.append("%" + nilai(node.child_by_field_name("value")) + "%")
        return f"{kolom(node.child_by_field_name('field'))} LIKE ?"
    raise ValueError(f"node tidak dikenal: {t}")


def konversi(teks):
    tree = parser.parse(teks.encode())
    if tree.root_node.has_error:
        raise ValueError("sintaks filter tidak valid")
    params = []
    return "WHERE " + ke_sql(tree.root_node, params), params


if __name__ == "__main__":
    print(konversi(sys.argv[1]))
