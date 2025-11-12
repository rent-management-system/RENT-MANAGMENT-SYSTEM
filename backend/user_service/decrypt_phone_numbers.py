#!/usr/bin/env python3
"""
normalize_and_fill_phone_numbers.py

- Back up existing phone_number into phone_number_encrypted (if not exists)
- Normalize hex-escaped strings like "\\x2b3235313734343130" -> "+2517...."
- Fill NULL/empty or invalid phone_number with generated Ethiopian numbers:
    - Standard mobile: "+2519XXXXXXXX"  (no spaces)
    - Safaricom style: "+251 72XXXXXXX" (space optional)
- Ensure all numbers start with +251 and are 13 chars long for standard
- Optionally alter column type to VARCHAR(20) at the end.

Run:
    source Bate/bin/activate
    python backend/user_service/normalize_and_fill_phone_numbers.py
"""
import os
import re
import random
import binascii
from typing import Optional
from sqlalchemy import create_engine, Column, String, text, inspect
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import sessionmaker, declarative_base
import uuid
from dotenv import load_dotenv

load_dotenv()

AES_SECRET_KEY = os.getenv("AES_SECRET_KEY", "ZUuqSCB7UIvzs7fEmlKhoXs1PS4x8KzXXmsGLyoNhF4=")
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres.spdwbxirjclmafdwzkvu:Dagmawi/1234@aws-1-eu-west-1.pooler.supabase.com:5432/postgres",
)
if "+asyncpg" in DATABASE_URL:
    DATABASE_URL = DATABASE_URL.replace("+asyncpg", "")

# SQLAlchemy setup
Base = declarative_base()
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

class User(Base):
    __tablename__ = "users"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, index=True, nullable=False)
    phone_number = Column(String, nullable=True)
    # phone_number_encrypted might exist after backup

HEX_ESCAPE_RE = re.compile(r'^(?:\\x|\\\\x)[0-9a-fA-F]+')  # matches strings starting with \x or \\x
PLAIN_PHONE_RE = re.compile(r'^\+?[\d\s]{9,15}$')  # basic len check, spaces allowed

def decode_hex_escape(s: str, max_rounds: int = 3) -> Optional[str]:
    if not s:
        return None
    cur = s
    for _ in range(max_rounds):
        if cur.startswith('\\\\x'):
            hexpart = cur[3:]
        elif cur.startswith('\\x'):
            hexpart = cur[2:]
        else:
            idx = cur.find('\\x')
            hexpart = cur[idx+2:] if idx != -1 else None
        if hexpart:
            try:
                if len(hexpart) % 2 != 0:
                    hexpart = hexpart[:-1]
                decoded = binascii.unhexlify(hexpart).decode('utf-8', errors='ignore')
                if decoded.startswith('\\\\x') or '\\x' in decoded:
                    cur = decoded
                    continue
                return decoded.strip() if decoded.strip() else None
            except (binascii.Error, ValueError):
                break
        else:
            break
    return None

def generate_random_ethiopian_number() -> str:
    """Generate valid Ethiopian phone number (standard or Safaricom style)."""
    if random.random() < 0.2:  # 20% Safaricom style
        local_rest = ''.join(str(random.randint(0,9)) for _ in range(7))
        if random.random() < 0.5:
            return f"+251 72{local_rest}"  # Safaricom with space
        else:
            return f"+25172{local_rest}"  # Safaricom no space
    else:
        prefix = str(random.choice(range(91,100)))  # 91..99 for standard mobile
        local_rest = ''.join(str(random.randint(0,9)) for _ in range(7))
        return f"+251{prefix}{local_rest}"

def ensure_backup_column():
    inspector = inspect(engine)
    with engine.connect() as conn:
        cols = [c['name'] for c in inspector.get_columns('users')]
        if 'phone_number_encrypted' not in cols:
            print("Creating backup column phone_number_encrypted and copying current values...")
            conn.execute(text('ALTER TABLE users ADD COLUMN phone_number_encrypted TEXT;'))
            conn.execute(text('UPDATE users SET phone_number_encrypted = phone_number;'))
            conn.commit()
            print("Backup column created and populated.")
        else:
            print("Backup column already exists — skipping backup creation.")

def normalize_and_fill():
    session = SessionLocal()
    try:
        users = session.query(User).all()
        updated_count = 0
        skipped_count = 0
        filled_nulls = 0
        for u in users:
            orig = u.phone_number
            new_value = None

            # Fill null or empty
            if orig is None or not orig.strip():
                new_value = generate_random_ethiopian_number()
                u.phone_number = new_value
                filled_nulls += 1
                updated_count += 1
                print(f"[FILLED NULL] {u.email} -> {new_value}")
                continue

            # Already plain-looking phone number
            if PLAIN_PHONE_RE.match(orig.strip()):
                normalized = re.sub(r'\s+', ' ', orig.strip())  # collapse spaces
                if not normalized.startswith('+'):
                    normalized = '+' + normalized
                # Ensure valid length & prefix
                if normalized.replace(' ','').startswith('+2519') and len(normalized.replace(' ','')) == 13:
                    u.phone_number = normalized
                    updated_count += 1
                    print(f"[NORMALIZED] {u.email} {orig!r} -> {normalized!r}")
                elif normalized.replace(' ','').startswith('+2517') and len(normalized.replace(' ','')) == 13:
                    u.phone_number = normalized
                    updated_count += 1
                    print(f"[NORMALIZED Safaricom] {u.email} {orig!r} -> {normalized!r}")
                else:
                    # Invalid length/prefix -> fill
                    new_value = generate_random_ethiopian_number()
                    u.phone_number = new_value
                    updated_count += 1
                    print(f"[INVALID FORMAT -> FILLED] {u.email} {orig!r} -> {new_value!r}")
                continue

            # Hex escaped string
            if orig.startswith('\\x') or orig.startswith('\\\\x') or HEX_ESCAPE_RE.match(orig):
                decoded = decode_hex_escape(orig)
                if decoded:
                    decoded = decoded.strip()
                    if not decoded.startswith('+'):
                        decoded = '+' + decoded
                    # If still invalid length/prefix, generate new
                    if not (decoded.replace(' ','').startswith('+2519') or decoded.replace(' ','').startswith('+2517')) or len(decoded.replace(' ','')) != 13:
                        decoded = generate_random_ethiopian_number()
                    u.phone_number = decoded
                    updated_count += 1
                    print(f"[DECODED HEX] {u.email} {orig!r} -> {decoded!r}")
                else:
                    new_value = generate_random_ethiopian_number()
                    u.phone_number = new_value
                    updated_count += 1
                    print(f"[FAILED DECODE -> FILLED] {u.email} original={orig!r} -> {new_value!r}")
                continue

            # Fallback: invalid/unknown format -> fill random
            new_value = generate_random_ethiopian_number()
            u.phone_number = new_value
            updated_count += 1
            print(f"[FALLBACK FILLED] {u.email} original={orig!r} -> {new_value!r}")

        session.commit()
        print(f"\nDone. Updated: {updated_count}, Filled NULLs: {filled_nulls}, Skipped: {skipped_count}")

    except Exception as exc:
        session.rollback()
        print("Error during normalization:", exc)
    finally:
        session.close()

def alter_column_type(varchar_len: int = 20, do_alter: bool = True):
    if not do_alter:
        print("Skipping ALTER TABLE step (do_alter=False).")
        return
    print(f"Altering phone_number column type to VARCHAR({varchar_len})...")
    with engine.connect() as conn:
        conn.execute(text(f'ALTER TABLE users ALTER COLUMN phone_number TYPE VARCHAR({varchar_len}) USING phone_number::VARCHAR({varchar_len});'))
        conn.commit()
    print("Column type altered.")

if __name__ == "__main__":
    print("=== Starting normalization & fill script ===")
    ensure_backup_column()
    normalize_and_fill()
    alter_column_type(varchar_len=20, do_alter=True)
    print("=== Script finished ===")
