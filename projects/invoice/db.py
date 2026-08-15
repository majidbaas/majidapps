import sqlite3

from .config import DATABASE_PATH
 
def get_all_invoices():
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM invoices ORDER BY id DESC")
    rows = c.fetchall()
    conn.close()
    return rows

def get_invoice_by_id(invoice_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM invoices WHERE id = ?", (invoice_id,))
    row = c.fetchone()
    conn.close()
    return row

def get_invoice_items_by_invoice_id(invoice_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM invoice_items WHERE invoice_id = ?", (invoice_id,))
    rows = c.fetchall()
    conn.close()
    return rows
def get_connection():

    conn = sqlite3.connect(DATABASE_PATH)

    conn.row_factory = sqlite3.Row

    return conn


def create_database():

    conn = get_connection()

    cursor = conn.cursor()

    # ==========================
    # جدول تنظیمات
    # ==========================

    cursor.execute("""

    CREATE TABLE IF NOT EXISTS settings(

        id INTEGER PRIMARY KEY,

        shop_name TEXT,

        phone TEXT,

        address TEXT,

        card_number TEXT,

        card_holder TEXT,

        vat_percent REAL,

        logo TEXT,

        header TEXT,

        stamp TEXT,

        signature TEXT

    )

    """)

    # ==========================
    # جدول فاکتورها
    # ==========================

    cursor.execute("""

    CREATE TABLE IF NOT EXISTS invoices(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        invoice_number TEXT,

        invoice_date TEXT,

        buyer TEXT,

        buyer_phone TEXT,

        buyer_address TEXT,

        description TEXT,

        subtotal REAL,

        discount REAL,

        vat_percent REAL,

        vat_amount REAL,

        total REAL,

        pdf_name TEXT,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

    )

    """)

    # ==========================
    # جدول ردیف های فاکتور
    # ==========================

    cursor.execute("""

    CREATE TABLE IF NOT EXISTS invoice_items(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        invoice_id INTEGER,

        title TEXT,

        description TEXT,

        quantity REAL,

        price REAL,

        discount REAL,

        discount_type TEXT,

        total REAL,

        FOREIGN KEY(invoice_id)
        REFERENCES invoices(id)

    )

    """)

    # ==========================
    # اگر تنظیمات وجود نداشت
    # ==========================

    cursor.execute(

        "SELECT COUNT(*) FROM settings"

    )

    count = cursor.fetchone()[0]

    if count == 0:

        cursor.execute("""

        INSERT INTO settings(

            id,

            shop_name,

            phone,

            address,

            card_number,

            card_holder,

            vat_percent,

            logo,

            header,

            stamp,

            signature

        )

        VALUES(

            1,

            'کافی نت آپادانا',

            '',

            '',

            '',

            '',

            10,

            '',

            '',

            '',

            ''

        )

        """)

    conn.commit()

    conn.close()

def get_settings():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(

        "SELECT * FROM settings WHERE id=1"

    )

    row = cursor.fetchone()

    conn.close()

    return row


def save_settings(data):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""

        UPDATE settings

        SET

            shop_name=?,

            phone=?,

            address=?,

            card_number=?,

            card_holder=?,

            vat_percent=?,

            logo=?,

            header=?,

            stamp=?,

            signature=?

        WHERE id=1

    """,

    (

        data["shop_name"],

        data["phone"],

        data["address"],

        data["card_number"],

        data["card_holder"],

        data["vat_percent"],

        data["logo"],

        data["header"],

        data["stamp"],

        data["signature"]

    )

    )

    conn.commit()

    conn.close()
    
    
    
    # ============================================================
#تابع شماره فاکتور
# ============================================================
def get_next_invoice_number():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT MAX(CAST(invoice_number AS INTEGER))
        FROM invoices
        WHERE invoice_number IS NOT NULL
          AND invoice_number != ''
          AND invoice_number GLOB '[0-9]*'
    """)

    row = cursor.fetchone()
    conn.close()

    last_number = row[0] if row and row[0] is not None else 1000

    return str(last_number + 1)
# ============================================================
# تابع حذف فاکتور (همه‌ی ردیف‌های مربوطه حذف می‌شوند)
# ============================================================
def delete_invoice_by_id(invoice_id):
    conn = get_connection()
    cursor = conn.cursor()
    
    # 1. ابتدا ردیف‌های جدول invoice_items حذف می‌شوند (چون کلید خارجی دارند)
    cursor.execute("DELETE FROM invoice_items WHERE invoice_id = ?", (invoice_id,))
    
    # 2. سپس خود فاکتور حذف می‌شود
    cursor.execute("DELETE FROM invoices WHERE id = ?", (invoice_id,))
    
    conn.commit()
    conn.close()
def save_invoice(data):
    conn = get_connection()
    cursor = conn.cursor()
    # تولید خودکار شماره فاکتور
    if not data.get("invoice_number"):
        cursor.execute("""
            SELECT MAX(CAST(invoice_number AS INTEGER))
            FROM invoices
            WHERE invoice_number IS NOT NULL
              AND invoice_number != ''
              AND invoice_number GLOB '[0-9]*'
        """)

        row = cursor.fetchone()

        last_number = row[0] if row and row[0] is not None else 1000

        data["invoice_number"] = str(last_number + 1)
    # 1. ذخیره اطلاعات هدر فاکتور در جدول invoices
    cursor.execute("""
        INSERT INTO invoices(
            invoice_number,
            invoice_date,
            buyer,
            buyer_phone,
            buyer_address,
            description,
            subtotal,
            discount,
            vat_percent,
            vat_amount,
            total,
            pdf_name
        )
        VALUES(
            ?,?,?,?,?,?,?,?,?,?,?,?
        )
    """,
    (
        data["invoice_number"],
        data["invoice_date"],
        data["buyer"],
        data["buyer_phone"],
        data["buyer_address"],
        data["description"],
        data["subtotal"],
        data["discount"],
        data["vat_percent"],
        data["vat_amount"],
        data["total"],
        data.get("pdf_name", "")
    )
    )

    # دریافت ID فاکتور تازه ثبت شده
    invoice_id = cursor.lastrowid

    # ============================================================
    # 2. تغییر مهم: ذخیره لیست کالاها (items) در جدول invoice_items
    # ============================================================
    if "items" in data:
        for item in data["items"]:
            cursor.execute("""
                INSERT INTO invoice_items(
                    invoice_id,
                    title,
                    description,
                    quantity,
                    price,
                    discount,
                    discount_type,
                    total
                )
                VALUES(?,?,?,?,?,?,?,?)
            """,
            (
                invoice_id,
                item["title"],
                "", # توضیحات فعلاً خالی است
                item["quantity"],
                item["price"],
                item["discount"],
                item["discount_type"],
                item["final_price"]
            )
            )

    conn.commit()
    conn.close()

    return invoice_id
    
    
