#!/usr/bin/env python3
# /usr/local/bin/nas-verify.py <slice 0-29>
# Keeps a checksum database of every NAS file. Each night it re-checks 1/30 of the
# files. A file whose size+mtime did NOT change but whose checksum DID change (or
# which cannot be read) is corrupted. Corrupted paths are printed, one per line.
import os, sys, hashlib, sqlite3, zlib

NAS = "/mnt/nas_6tb"
DB = "/var/lib/nas-backup/manifest.db"
SLICES = 30
day = int(sys.argv[1]) % SLICES

os.makedirs(os.path.dirname(DB), exist_ok=True)
db = sqlite3.connect(DB)
db.execute("create table if not exists f(path text primary key, size int, mtime int, sha text)")

def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()

bad = []
for root, _, files in os.walk(NAS):
    for n in files:
        p = os.path.join(root, n)
        try:
            st = os.stat(p)
        except OSError:
            continue
        row = db.execute("select size, mtime, sha from f where path=?", (p,)).fetchone()
        if row is None or (row[0], row[1]) != (st.st_size, int(st.st_mtime)):
            # new or legitimately modified file: record its checksum
            try:
                db.execute("replace into f values(?,?,?,?)", (p, st.st_size, int(st.st_mtime), sha(p)))
            except OSError:
                bad.append(p)
        elif zlib.crc32(p.encode()) % SLICES == day:
            try:
                if sha(p) != row[2]:
                    bad.append(p)
            except OSError:
                bad.append(p)
db.commit()
print("\n".join(bad))
