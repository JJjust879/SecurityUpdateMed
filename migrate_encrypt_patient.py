# migrate_encrypt_patient.py
#
# One-time script: encrypt existing address + cp_no
# values in patient_profile table.

import sqlite3
from utils.crypto import encrypt_str

DB_PATH = "db.db"  # database in project root

def main():
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()

    # Check table structure
    cur.execute("PRAGMA table_info('patient_profile')")
    cols = {c[1] for c in cur.fetchall()}
    required = {"PatientID", "address", "cp_no"}
    if not required.issubset(cols):
        raise RuntimeError(
            f"patient_profile table does not have expected columns: {required}"
        )

    # Use actual column names: PatientID, address, cp_no
    cur.execute("SELECT PatientID, address, cp_no FROM patient_profile")
    rows = cur.fetchall()

    updated = 0

    for pid, addr, phone in rows:
        new_addr = addr
        new_phone = phone

        # If value is NOT bytes, treat it as plaintext and encrypt it.
        if not isinstance(addr, (bytes, bytearray)) and addr is not None:
            new_addr = encrypt_str(addr)

        if not isinstance(phone, (bytes, bytearray)) and phone is not None:
            new_phone = encrypt_str(phone)

        # Only issue an UPDATE if something changed
        if new_addr is not addr or new_phone is not phone:
            cur.execute(
                "UPDATE patient_profile SET address = ?, cp_no = ? WHERE PatientID = ?",
                (new_addr, new_phone, pid),
            )
            updated += 1

    con.commit()
    con.close()
    print(f"Migration completed. Rows encrypted/updated: {updated}")

if __name__ == "__main__":
    main()
