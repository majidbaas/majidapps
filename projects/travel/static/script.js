const cities = {
  internal: ["تهران", "مشهد", "شیراز", "کیش", "اصفهان", "بندرعباس", "قشم", "آبادان"],
  external: ["استانبول", "دبی", "تفلیس", "وان", "ایروان", "باتومی", "آنکارا"]
};

function loadCities() {
  const type = document.getElementById("city-type").value;
  const citySelect = document.getElementById("city");

  citySelect.innerHTML = '<option value="">-- انتخاب شهر --</option>';
  if (!type) return;

  cities[type].forEach(c => {
    const opt = document.createElement("option");
    opt.value = c;
    opt.textContent = c;
    citySelect.appendChild(opt);
  });
}

// ---------- Travelers ----------
let adult = 1;
let child = 0;

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

  if (!textEl) {
    console.error("traveler-text not found");
    return;
  }

  textEl.innerText =
    adult + " بزرگسال" + (child ? "، " + child + " کودک" : "");

  document.getElementById("adultInput").value = adult;
  document.getElementById("childInput").value = child;

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

// غیرفعال‌سازی مسافران در سفر انفرادی
document.addEventListener("DOMContentLoaded", function () {
  const travelTypeSelect = document.querySelector('select[name="travel_type"]');
  const travelerInput = document.querySelector(".traveler-input");

  if (!travelTypeSelect || !travelerInput) return;

  function toggleTravelerInput() {
    if (travelTypeSelect.value === "solo") {
      travelerInput.classList.add("disabled");
      travelerInput.style.pointerEvents = "none";
      travelerInput.style.opacity = "0.5";

      document.getElementById("adultInput").value = 1;
      document.getElementById("childInput").value = 0;
      document.getElementById("adultCount").innerText = 1;
      document.getElementById("childCount").innerText = 0;

      document.querySelector(".traveler-text").innerText = "1 بزرگسال";
    } else {
      travelerInput.classList.remove("disabled");
      travelerInput.style.pointerEvents = "auto";
      travelerInput.style.opacity = "1";
    }
  }

  travelTypeSelect.addEventListener("change", toggleTravelerInput);
  toggleTravelerInput();
});




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