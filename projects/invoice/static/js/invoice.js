document.addEventListener("DOMContentLoaded", function () {

function calc() {

    let subtotal = 0;
    let totalItemDiscount = 0;
	
    document.querySelectorAll("#items tr").forEach(function (row) {

        // ======================
        // تعداد
        // ======================

        let qty =
            Number(
                (row.querySelector(".qty")?.value || "0")
                .replace(/,/g, "")
            ) || 0;

        // ======================
        // قیمت
        // ======================

        let price =
            Number(
                (row.querySelector(".price")?.value || "0")
                .replace(/,/g, "")
            ) || 0;

        // ======================
        // مبلغ قبل از تخفیف
        // ======================

        let amount = qty * price;

        let subtotalCell = row.querySelector(".subtotal");

		if(subtotalCell){
			subtotalCell.innerText = amount.toLocaleString("en-US");
		}
		// ======================
		// تخفیف
		// ======================

		let input = row.querySelector(".item-discount");

		if(!input) return;
        let discountSelect = row.querySelector(".discount-type");

		let discountType = discountSelect ? discountSelect.value : "none";
        let discount = 0;

        // اگر نوع تخفیف "none" است، مقدار داخل فیلد را نادیده بگیر
        if (discountType === "none") {
            discount = 0;
        } else {
            discount = Number((input?.value || "0").replace(/,/g, "")) || 0;
        }

        let discountAmount = 0;

        if (discountType === "none") {
            discountAmount = 0;
        }
        else if (discountType === "amount") {
            discountAmount = discount;
        }
        else if (discountType === "percent") {
            if (discount > 99) {
                discount = 99;
                input.value = "99";
            }
            discountAmount = amount * discount / 100;
        }

        if (discountAmount > amount) {
            discountAmount = amount;
        }

        // ======================
        // مبلغ قابل پرداخت
        // ======================

        let finalAmount =
            amount - discountAmount;

        row.querySelector(".amount").innerText =
            finalAmount.toLocaleString("en-US");

        subtotal += finalAmount;
        totalItemDiscount += discountAmount;

    });

    // ======================
    // جمع کالاها
    // ======================

    document.getElementById("subtotal").innerText =
        subtotal.toLocaleString("en-US");

    document.getElementById("discount").innerText =
        totalItemDiscount.toLocaleString("en-US");

    // ======================
    // مالیات
    // ======================

    let vat = 0;

    let vatEnabled =
        document.getElementById("vat_enabled");

    let vatPercent =
        document.getElementById("vat_percent");

    if (
        vatEnabled &&
        vatEnabled.checked
    ) {

        vat =
            subtotal *
            (Number(vatPercent.value) || 0) / 100;

    }

    document.getElementById("vatAmount").innerText =
        vat.toLocaleString("en-US");

    document.getElementById("total").innerText =
        (subtotal + vat).toLocaleString("en-US");

}

// ======================
// فرمت اعداد
// ======================

document.addEventListener("input", function (e) {

    if (e.target.classList.contains("number-format")) {

        let raw = e.target.value.replace(/,/g, "");

        if (raw !== "" && !isNaN(raw)) {

            e.target.value =
                Number(raw).toLocaleString("en-US");

        }

    }

    calc();

});

// ==========================================================
// مدیریت فعال/غیرفعال کردن فیلد تخفیف بر اساس انتخاب منو
// ==========================================================
 
// ==========================================================
// مدیریت تخفیف
// ==========================================================

function updateDiscountState(select) {

    const row = select.closest("tr");
    const input = row.querySelector(".discount-input");

    if (!input) return;

    if (select.value === "none") {

        input.disabled = true;
        input.value = "";
        input.placeholder = "غیرفعال";
        input.classList.add("bg-secondary-subtle");

    } else {

        input.disabled = false;
        input.placeholder = "0";
        input.classList.remove("bg-secondary-subtle");

    }
}


// ردیف‌های موجود
document.querySelectorAll(".discount-type").forEach(function(select) {

    updateDiscountState(select);

    select.addEventListener("change", function() {

        updateDiscountState(this);
        calc();

    });

});
// ======================
// افزودن ردیف
// ======================

// ======================
// افزودن ردیف
// ======================

const addRowButton = document.getElementById("addRow");

console.log("Add Row Button:", addRowButton);

if (addRowButton) {

    addRowButton.onclick = function () {

        let firstRow = document.querySelector("#items tr");

        if (!firstRow) return;

        let row = firstRow.cloneNode(true);

        // ======================
        // ریست فیلدها
        // ======================

        row.querySelectorAll("input").forEach(function(input) {

            if (input.classList.contains("qty")) {

                input.value = "1";

            }
            else if (input.classList.contains("price")) {

                input.value = "0";

            }
            else if (input.classList.contains("item-discount")) {

                input.value = "";
                input.placeholder = "غیرفعال";

            }
            else {

                input.value = "";

            }

        });

        // ======================
        // ریست تخفیف
        // ======================

        const discountSelect =
            row.querySelector(".discount-type");

        const discountInput =
            row.querySelector(".discount-input");

        if (discountSelect) {
            discountSelect.value = "none";
        }

        if (discountInput) {

            discountInput.disabled = true;
            discountInput.value = "";
            discountInput.placeholder = "غیرفعال";
            discountInput.classList.add("bg-secondary-subtle");

        }

        // ======================
        // ریست مبالغ
        // ======================

        const subtotalCell =
            row.querySelector(".subtotal");

        const amountCell =
            row.querySelector(".amount");

        if (subtotalCell) {
            subtotalCell.innerText = "0";
        }

        if (amountCell) {
            amountCell.innerText = "0";
        }

        // ======================
        // اضافه کردن ردیف
        // ======================

        document
            .getElementById("items")
            .appendChild(row);
		const newSelect = row.querySelector(".discount-type");

		if (newSelect) {

			updateDiscountState(newSelect);

			newSelect.addEventListener("change", function() {

				updateDiscountState(this);
				calc();

			});

		}
        // ======================
        // تغییر نوع تخفیف
        // ======================

        if (discountSelect && discountInput) {

            discountSelect.addEventListener("change", function() {

                if (this.value === "none") {

                    discountInput.disabled = true;
                    discountInput.value = "";
                    discountInput.placeholder = "غیرفعال";
                    discountInput.classList.add("bg-secondary-subtle");

                }
                else {

                    discountInput.disabled = false;
                    discountInput.placeholder = "0";
                    discountInput.classList.remove("bg-secondary-subtle");

                }

                calc();

            });

        }

        calc();

    };

}

// ======================
// حذف ردیف
// ======================

document.addEventListener("click", function (e) {

    if (!e.target.classList.contains("removeRow")) return;

    if (
        document.querySelectorAll("#items tr").length > 1
    ) {

        e.target.closest("tr").remove();

        calc();

    }

});

// ======================
// روشن / خاموش مالیات
// ======================

const vatEnabled =
    document.getElementById("vat_enabled");

const vatPercent =
    document.getElementById("vat_percent");

if (vatEnabled) {

    vatEnabled.addEventListener("change", function () {

        vatPercent.disabled = !this.checked;

        if (this.checked) {

            vatPercent.classList.remove("bg-secondary-subtle");

        } else {

            vatPercent.classList.add("bg-secondary-subtle");

        }

        calc();

    });

}

if (vatPercent) {

    vatPercent.addEventListener("input", calc);

}


// ======================
// تاریخ
// ======================

const invoiceDate =
    document.getElementById("invoice_date");

if (invoiceDate) {

    invoiceDate.addEventListener("input", function (e) {

        let value =
            e.target.value.replace(/\D/g, "");

        if (value.length > 8)
            value = value.substring(0, 8);

        if (value.length > 4)
            value =
                value.substring(0, 4) +
                "/" +
                value.substring(4);

        if (value.length > 7)
            value =
                value.substring(0, 7) +
                "/" +
                value.substring(7);

        e.target.value = value;

    });

}


// ======================
// شماره کارت
// ======================

const cardNumber =
    document.getElementById("card_number");

if (cardNumber) {

    cardNumber.addEventListener("input", function (e) {

        let value =
            e.target.value.replace(/\D/g, "");

        value = value.substring(0, 16);

        value =
            value.match(/.{1,4}/g)?.join("-") || "";

        e.target.value = value;

    });

}

// ======================
// اولین محاسبه
// ======================

document.querySelectorAll(".discount-type").forEach(function(select){

    const input = select.parentElement.querySelector(".discount-input");

    if(select.value === "none"){

        input.disabled = true;
        input.value = "";
        input.placeholder = "غیرفعال";
        input.classList.add("bg-secondary-subtle");

    } else {

        input.disabled = false;
        input.placeholder = "0";
        input.classList.remove("bg-secondary-subtle");

    }

});


calc();

});