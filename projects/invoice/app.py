from flask import Flask, render_template, request, make_response
from weasyprint import HTML
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, 'templates'),
    static_folder=os.path.join(BASE_DIR, 'static')
)
app.secret_key = "invoice_secret"

def fa_num(text):
    en = "0123456789"
    fa = "۰۱۲۳۴۵۶۷۸۹"

    text = str(text)

    for e, f in zip(en, fa):
        text = text.replace(e, f)

    return text

app.jinja_env.filters["fa"] = fa_num


@app.route("/", methods=["GET"])
def form():
    return render_template("form.html")


@app.route("/invoice", methods=["POST"])
def invoice():

    buyer = request.form.get("buyer")
    buyer_phone = request.form.get("buyer_phone")
    
    seller = request.form.get("seller")
    seller_phone = request.form.get("seller_phone")

    invoice_number = request.form.get("invoice_number")
    invoice_date = request.form.get("date")
    description = request.form.get("notes")
    discount = request.form.get("discount", "0")
    discount = float(discount.replace(",", ""))
    card_number_name = request.form.get("card_number_name")
    seller_address = request.form.get("seller_address")
    buyer_address = request.form.get("buyer_address")
    
    card_number = request.form.get("card_number")
    vat_percent = float(
        request.form.get("vat_percent", 0) or 0
    )
    vat_enabled = request.form.get("vat_enabled") is not None

    titles = request.form.getlist("item[]")
    quantities = request.form.getlist("qty[]")
    prices = request.form.getlist("price[]")

    items = []
    total_before_discount = 0

    for t, q, p in zip(titles, quantities, prices):

        
        q = float(str(q).replace(",",""))
        p = float(str(p).replace(",",""))
         
        subtotal = q * p

        total_before_discount += subtotal

        items.append({
            "title": t,
            "quantity": q,
            "price": p,
            "subtotal": subtotal,
           
        })

    total_discount = discount

    if vat_enabled:
        vat_amount = (
            (total_before_discount - total_discount)
            * vat_percent / 100
        )
    else:
         vat_amount = 0

    total_after_discount = (
        total_before_discount
        - total_discount
        + vat_amount
    )
    html = render_template(
        "invoice.html",
        buyer=buyer,
        buyer_phone=buyer_phone,
        buyer_address = buyer_address,

        seller=seller,
        seller_phone=seller_phone,
        seller_address = seller_address,
        
        invoice_number=invoice_number,
        invoice_date=invoice_date,
        description=description,
        card_number = card_number,
        card_number_name = card_number_name,
        items=items,

        total_before_discount=total_before_discount,
        total_discount=total_discount,
        total_after_discount=total_after_discount,

        vat_percent=vat_percent,
        vat_amount=vat_amount
    )

    pdf = HTML(string=html).write_pdf()

    response = make_response(pdf)
    response.headers["Content-Type"] = "application/pdf"
    response.headers["Content-Disposition"] = "inline; filename=invoice.pdf"

    return response


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port, debug=True)