console.log("script loaded");

// =========================
// Cities
// =========================
const cities = {
  internal: ["تهران", "مشهد", "شیراز", "کیش", "اصفهان", "بندرعباس", "قشم", "آبادان"],
  external: ["استانبول", "دبی", "تفلیس", "وان", "ایروان", "باتومی", "آنکارا"]
};

function loadCities(selectedCity = "") {

    const type = document.getElementById("city-type").value;
    const citySelect = document.getElementById("city");

    citySelect.innerHTML = '<option value="">-- انتخاب شهر --</option>';

    if (!type || !cities[type]) return;

    cities[type].forEach(city => {

        const option = document.createElement("option");

        option.value = city;
        option.textContent = city;

        if (city === selectedCity) {
            option.selected = true;
        }

        citySelect.appendChild(option);

    });

}

// ---------- Travelers ----------
let adult = 1;
let child = 0;

const adultInput = document.getElementById("adultInput");
const childInput = document.getElementById("childInput");

if (adultInput) {
    adult = parseInt(adultInput.value) || 1;
}

if (childInput) {
    child = parseInt(childInput.value) || 0;
}
function openTravelerModal() {
  document.getElementById("travelerModal").classList.add("active");
}

function closeTravelerModal() {
  document.getElementById("travelerModal").classList.remove("active");
}

function changeCount(type, value) {
  if (type === "adult") {
    adult = Math.max(1, adult + value);
    document.getElementById("adultCount").innerText = adult;
  } else {
    child = Math.max(0, child + value);
    document.getElementById("childCount").innerText = child;
  }
}
function applyTravelers() {
  const textEl = document.querySelector(".traveler-text");

  
   if (!textEl) return;
  

  textEl.innerText =
    adult + " بزرگسال" + (child ? "، " + child + " کودک" : "");

	const adultInput = document.getElementById("adultInput");
	const childInput = document.getElementById("childInput");

	if(adultInput) adultInput.value = adult;
	if(childInput) childInput.value = child;
  closeTravelerModal();
}

function generateChecklist(formData) {
  let checklist = [];

  // عمومی
  checklist.push("کارت ملی / شناسنامه");
  checklist.push("شارژر موبایل");
  checklist.push("لباس مناسب");

  // نوع سفر
  if (formData.travel_type === "family") {
    checklist.push("داروهای ضروری خانواده");
    checklist.push("وسایل کودک");
  }

  // وسیله سفر
  if (formData.transport === "plane") {
    checklist.push("بلیط هواپیما");
    checklist.push("کارت ملی");
	checklist.push("شناسنامه");
  }

  if (formData.transport === "car") {
    checklist.push("مدارک خودرو");
    checklist.push("بررسی فنی خودرو");
  }

  // محل اقامت
  if (formData.hotel_type === "camp") {
    checklist.push("چادر");
    checklist.push("چراغ قوه");
    checklist.push("پاوربانک");
  }
if (formData.hotel_type === "familyHome") {
  checklist.push("هماهنگی با میزبان");
  checklist.push("گرفتن آدرس دقیق");
  checklist.push("تهیه هدیه کوچک");
  checklist.push("بررسی ساعت ورود");
}


  // بودجه
  if (formData.budget === "economic") {
    checklist.push("بطری آب");
    checklist.push("خوراکی سبک");
  }

  if (formData.budget === "luxury") {
    checklist.push("لباس رسمی");
    checklist.push("عطر و لوازم شخصی کامل");
  }

  return checklist;
}
// =========================
// Travelers
// =========================
// غیرفعال‌سازی مسافران در سفر انفرادی
document.addEventListener("DOMContentLoaded", function () {
  const travelTypeSelect = document.querySelector('select[name="travel_type"]');
  const travelerInput = document.querySelector(".traveler-input");

  if (!travelTypeSelect || !travelerInput) return;

  function toggleTravelerInput() {
    if (travelTypeSelect.value === "solo") {
      travelerInput.classList.add("disabled");
	  
     

      const adultInput = document.getElementById("adultInput");
		const childInput = document.getElementById("childInput");
		const adultCount = document.getElementById("adultCount");
		const childCount = document.getElementById("childCount");
		const travelerText = document.querySelector(".traveler-text");

		if (adultInput) adultInput.value = 1;
		if (childInput) childInput.value = 0;

		if (adultCount) adultCount.innerText = 1;
		if (childCount) childCount.innerText = 0;

		if (travelerText) travelerText.innerText = "1 بزرگسال";
    } else {
      travelerInput.classList.remove("disabled");
   
    }
  }

  travelTypeSelect.addEventListener("change", toggleTravelerInput);
  toggleTravelerInput();
});


// Stepper

function setStep(stepNumber) {
  const steps = document.querySelectorAll('.step');
  const connectors = document.querySelectorAll('.connector');

  steps.forEach((step, index) => {
    step.classList.remove('active', 'completed');

    if (index + 1 < stepNumber) {
      step.classList.add('completed');
    } else if (index + 1 === stepNumber) {
      step.classList.add('active');
    }
  });

  connectors.forEach((connector, index) => {
    connector.classList.toggle('completed', index + 2 <= stepNumber);
  });
}

document.addEventListener("DOMContentLoaded", () => {



    console.log("DOMContentLoaded");



    const bar = document.getElementById("progressFill");
    const percent = document.getElementById("progressPercent");
    const status = document.getElementById("progressStatus");
    const btn = document.getElementById("confirmBtn");

    // اگر این صفحه صفحه پیش‌نمایش نبود، هیچ کاری نکن
    if (!bar || !percent || !status || !btn) {
        return;
    }

    let progress = 0;

    btn.disabled = true;

    const steps = [
        { percent:10, text:"🔍 در حال بررسی اطلاعات سفر..." },
        { percent:25, text:"📍 بررسی مقصد سفر..." },
        { percent:40, text:"🏨 انتخاب وسایل متناسب با محل اقامت..." },
        { percent:55, text:"👕 آماده‌سازی لباس‌های مناسب فصل..." },
        { percent:70, text:"💊 بررسی وسایل بهداشتی..." },
        { percent:82, text:"🔌 اضافه کردن وسایل الکترونیکی..." },
        { percent:92, text:"📋 تولید چک لیست اختصاصی..." },
        { percent:100, text:"✅ همه چیز آماده است." }
    ];

    function updateStatus() {

        for(let i=steps.length-1;i>=0;i--){

            if(progress>=steps[i].percent){

                status.innerText=steps[i].text;
                break;

            }

        }

    }

    function next(){

        progress++;

        bar.style.width = progress + "%";

        percent.innerText = progress + "%";

        updateStatus();

        if(progress<30){

            setTimeout(next,15);

        }

        else if(progress<70){

            setTimeout(next,20);

        }

        else if(progress<90){

            setTimeout(next,60);

        }

        else if(progress<100){

            setTimeout(next,120);

        }

        else{

            status.innerHTML =
            "✅ اطلاعات سفر با موفقیت بررسی شد.<br>اکنون می‌توانید چک لیست را ایجاد کنید.";

            btn.disabled = false;

            btn.classList.add("ready");

        }

    }

    next();

});

console.log("END OF SCRIPT");