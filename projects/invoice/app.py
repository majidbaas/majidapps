from flask import Flask, render_template, request, make_response, redirect, url_for, session
import os

import tempfile
from weasyprint import HTML   
from werkzeug.utils import secure_filename
from utils import to_persian_number, to_persian_text
from db import (
    create_database,
    get_settings,
    save_settings,
    save_invoice,
    get_all_invoices,
    get_invoice_by_id,
    get_invoice_items_by_invoice_id,
    delete_invoice_by_id   
)

app = Flask(__name__)
UPLOAD_FOLDER = "static/uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.secret_key = "supersecretkey"

create_database()

def fa_num(text):
    en = "0123456789"
    fa = "۰۱۲۳۴۵۶۷۸۹"
    text = str(text)
    for e, f in zip(en, fa):
        text = text.replace(e, f)
    return text
app.jinja_env.filters["fa"] = fa_num

def build_invoice_data(form):
    data = {}
    data["buyer"] = form.get("buyer")
    data["buyer_phone"] = form.get("buyer_phone")
    data["buyer_address"] = form.get("buyer_address")
    data["invoice_number"] = form.get("invoice_number")
    data["invoice_date"] = form.get("date")
    data["description"] = form.get("notes")
    settings = get_settings()
    data["settings"] = settings
    data["seller"] = settings["shop_name"] or ""
    data["seller_phone"] = settings["phone"] or ""
    data["seller_address"] = settings["address"] or ""
    data["card_number"] = settings["card_number"] or ""
    data["card_number_name"] = settings["card_holder"] or ""
    data["vat_percent"] = float(form.get("vat_percent", settings["vat_percent"] or 0))
    vat_enabled = form.get("vat_enabled") is not None
    titles = form.getlist("item[]")
    quantities = form.getlist("qty[]")
    prices = form.getlist("price[]")
    item_discounts = form.getlist("item_discount[]")
    item_discount_types = form.getlist("item_discount_type[]")
    items = []
    total_before_discount = 0
    total_item_discount = 0
    for i in range(len(titles)):
        title = titles[i]
        qty = float(str(quantities[i]).replace(",", "") or 0)
        price = float(str(prices[i]).replace(",", "") or 0)
        discount = 0
        if i < len(item_discounts):
           discount = float(str(item_discounts[i] if i < len(item_discounts) else 0).replace(",", "") or 0)
        discount_type = "none"
        if i < len(item_discount_types):
            discount_type = item_discount_types[i]
        subtotal = qty * price
        if discount_type == "amount":
            discount_amount = discount
        elif discount_type == "percent":
            discount_amount = subtotal * discount / 100
        else:
            discount_amount = 0
        discount_amount = min(discount_amount, subtotal)
        final_price = subtotal - discount_amount
        total_before_discount += subtotal
        total_item_discount += discount_amount
        items.append({
            "title": title,
            "quantity": int(qty) if qty.is_integer() else qty,
            "price": price,
            "subtotal": subtotal,
            "discount": discount_amount,
            "discount_type": discount_type,
            "final_price": final_price
        })
    items_total = sum(item["final_price"] for item in items)
    total_discount = total_item_discount
    after_discount = items_total
    if vat_enabled:
        vat_amount = (items_total * data["vat_percent"] / 100)
    else:
        vat_amount = 0
    total_after_discount = items_total + vat_amount
    data["items"] = items
    data["total_before_discount"] = total_before_discount
    data["items_total"] = items_total
    data["total_item_discount"] = total_item_discount
    data["total_discount"] = total_discount
    data["after_discount"] = after_discount
    data["vat_amount"] = vat_amount
    data["total_after_discount"] = total_after_discount
    data["save_data"] = {
        "invoice_number": data["invoice_number"],
        "invoice_date": data["invoice_date"],
        "buyer": data["buyer"],
        "buyer_phone": data["buyer_phone"],
        "buyer_address": data["buyer_address"],
        "description": data["description"],
        "subtotal": data["total_before_discount"],
        "discount": data["total_discount"],
        "vat_percent": data["vat_percent"],
        "vat_amount": data["vat_amount"],
        "total": data["total_after_discount"],
        "items": data["items"]
    }
    return data

@app.route("/settings/save", methods=["POST"])
def save_settings_route():
    settings = get_settings()
    logo_name = settings["logo"]
    logo = request.files.get("logo")
    if logo and logo.filename != "":
        filename = secure_filename(logo.filename)
        os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
        logo.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
        logo_name = filename
    data = {
        "shop_name": request.form["shop_name"],
        "phone": request.form["phone"],
        "address": request.form["address"],
        "card_number": request.form["card_number"],
        "card_holder": request.form["card_holder"],
        "vat_percent": request.form["vat_percent"],
        "logo": logo_name,
        "header": "",
        "stamp": "",
        "signature": ""
    }
    save_settings(data)
    return redirect("/settings")
@app.route("/invoice/edit/<int:invoice_id>", methods=["GET"])
def edit_invoice(invoice_id):
    invoice = get_invoice_by_id(invoice_id)
    items_tuple = get_invoice_items_by_invoice_id(invoice_id)
    settings = get_settings()
    
    if not invoice:
        return redirect("/invoices")

   
    items_list = []
    if items_tuple:
        for item in items_tuple:
            if len(item) >= 9:
                items_list.append({
                    "title": item[2],
                    "quantity": item[4],
                    "price": item[5],
                    "discount": item[6] if item[7] != "none" else "",
                    "discount_type": item[7],
                    "final_price": item[8]
                })

    invoice_data = {
        "invoice_number": invoice[1],
        "invoice_date": invoice[2],
        "buyer": invoice[3],
        "buyer_phone": invoice[4],
        "buyer_address": invoice[5],
        "description": invoice[6],
        "items_list": items_list,   
        "vat_percent": invoice[9] if invoice else 10,
        "vat_enabled": invoice[9] and invoice[9] > 0 if invoice else False    }

    return render_template(
        "pages/form.html",
        edit_mode=True,
        invoice_data=invoice_data,
         
        settings=settings
    )
# ============================================================
# مسیر تنظیمات (با دکمه برگشت به خانه)
# ============================================================
@app.route("/settings")
def settings():
    settings = get_settings()
    # به صفحه خانه برمی‌گردد
    back_url = "/" 
    return render_template("pages/settings.html", settings=settings, back_url=back_url)

# ============================================================
# مسیر حذف فاکتور (تکمیل شده)
# ============================================================
@app.route("/invoice/delete/<int:invoice_id>", methods=["POST"])
def delete_invoice(invoice_id):
    delete_invoice_by_id(invoice_id)  
    return redirect("/invoices")
@app.route("/", methods=["GET"])
def home():
    return render_template("pages/home.html")
    
@app.route("/invoice/new")
def new_invoice():
    settings = get_settings()
    return render_template("pages/form.html", settings=settings)
 
@app.route("/preview", methods=["POST"])
def preview():
    data = build_invoice_data(request.form)

    # اطلاعات فاکتور فعلاً در Session نگهداری می‌شود
    # تا کاربر در صفحه پیش‌نمایش روی «ثبت نهایی» بزند.
    session["preview_invoice"] = data["save_data"]

    return render_template(
        "invoice.html",
        preview=True,
        source="new",
        invoice_id=None,
        **data,
        to_persian_number=to_persian_number,
        to_persian_text=to_persian_text
    )
    
@app.route("/invoice/final-save", methods=["POST"])
def final_save_invoice():

    data = session.get("preview_invoice")

    if not data:
        return redirect("/invoice/new")

    # ذخیره نهایی در دیتابیس
    save_invoice(data)

    # بعد از ذخیره، اطلاعات موقت را پاک می‌کنیم
    session.pop("preview_invoice", None)

    return redirect("/invoices")

@app.route("/invoice/save", methods=["POST"])
def save_invoice_only():
    data = build_invoice_data(request.form)
    save_invoice(data["save_data"])
    return redirect("/invoices")

@app.route("/invoices")
def invoices_list():
    all_invoices = get_all_invoices()
    return render_template("pages/invoices_list.html", invoices=all_invoices)

# ============================================================
# مسیرهای تولید PDF با WeasyPrint (نسخه نهایی و تضمینی)
# ============================================================
def generate_pdf_from_invoice_id(invoice_id, download=True):
    invoice = get_invoice_by_id(invoice_id)
    items_tuple = get_invoice_items_by_invoice_id(invoice_id)
    settings = get_settings()
    
    items = []
    for item in items_tuple:
        items.append({
            "title": item[2],
            "quantity": item[4],
            "price": item[5],
            "discount": item[6],
            "discount_type": item[7],
            "final_price": item[8]
        })

    if hasattr(settings, 'keys'):
        settings = dict(settings)

    data = {
        "invoice_number": invoice[1],
        "invoice_date": invoice[2],
        "buyer": invoice[3],
        "buyer_phone": invoice[4],
        "buyer_address": invoice[5],
        "description": invoice[6],
        "settings": settings,
        "seller": settings["shop_name"] or "",
        "seller_phone": settings["phone"] or "",
        "seller_address": settings["address"] or "",
        "card_number": settings["card_number"] or "",
        "card_number_name": settings["card_holder"] or "",
        "vat_percent": invoice[9] if invoice else 10,
        "items": items,
        "total_before_discount": invoice[7],
        "total_discount": invoice[8],
        "vat_amount": invoice[10],
        "total_after_discount": invoice[11]
    }

    rendered_html = render_template(
        "invoice.html", 
        **data, 
        to_persian_number=to_persian_number, 
        to_persian_text=to_persian_text
    )

    # استفاده از WeasyPrint برای تبدیل مستقیم
    pdf_bytes = HTML(string=rendered_html, base_url=request.url_root).write_pdf()

    response = make_response(pdf_bytes)
    response.headers["Content-Type"] = "application/pdf"
    if download:
        response.headers["Content-Disposition"] = f"attachment; filename=invoice_{invoice_id}.pdf"
    else:
        response.headers["Content-Disposition"] = f"inline; filename=invoice_{invoice_id}.pdf"
    return response

@app.route("/invoice/download_pdf/<int:invoice_id>", methods=["GET"])
def download_pdf(invoice_id):
    return generate_pdf_from_invoice_id(invoice_id, download=True)


# ============================================================
# مسیر پیش‌نمایش فاکتورهای ثبت شده (از روی دیتابیس)
# ============================================================
@app.route("/invoice/preview/<int:invoice_id>", methods=["GET"])
def preview_saved_invoice(invoice_id):
    source = "list"
    invoice = get_invoice_by_id(invoice_id)
    items_tuple = get_invoice_items_by_invoice_id(invoice_id)
    settings = get_settings()
    
    items = []
    for item in items_tuple:
        items.append({
            "title": item[2],
            "quantity": item[4],
            "price": item[5],
            "discount": item[6],
            "discount_type": item[7],
            "final_price": item[8]
        })

    if hasattr(settings, 'keys'):
        settings = dict(settings)

    data = {
        "invoice_number": invoice[1],
        "invoice_date": invoice[2],
        "buyer": invoice[3],
        "buyer_phone": invoice[4],
        "buyer_address": invoice[5],
        "description": invoice[6],
        "settings": settings,
        "seller": settings["shop_name"] or "",
        "seller_phone": settings["phone"] or "",
        "seller_address": settings["address"] or "",
        "card_number": settings["card_number"] or "",
        "card_number_name": settings["card_holder"] or "",
        "vat_percent": invoice[9],
        "items": items,
        "total_before_discount": invoice[7],
        "total_discount": invoice[8],
        "vat_amount": invoice[10],
        "total_after_discount": invoice[11]
    }

    return render_template(
        "invoice.html",
        preview=False,
        source="list",
        invoice_id=invoice_id,
        **data,
        to_persian_number=to_persian_number,
        to_persian_text=to_persian_text
    )
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003, debug=False)