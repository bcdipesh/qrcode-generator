"use strict";

// Buttons
const createQRBtn = document.querySelector(".create-qr-btn");
const saveQRBtn = document.querySelector(".save-qr-btn");
const updateQRBtn = document.querySelector(".update-qr-btn");
const downloadQRBtn = document.querySelector(".download-qr-btn");
let qrCodeUrl = null;
let fileFormat = null;
let qrCodeId = null;

// Form
const createQRCodeForm = document.querySelector(".qr-code-form");

const collectFormData = (form) => {
  // Collect form data
  const content = form.elements["content"].value;
  const size = form.elements["size"].value;
  const charsetSource = form.elements["charset_source"].value;
  const charsetTarget = form.elements["charset_target"].value;
  const ecc = form.elements["ecc"].value;
  const color = form.elements["color"].value;
  const bgColor = form.elements["bg_color"].value;
  const margin = form.elements["margin"].value;
  const qzone = form.elements["qzone"].value;
  qrCodeId = form.elements["qr_code_id"]?.value ?? null;
  fileFormat = form.elements["file_format"].value;

  return {
    content,
    size,
    charsetSource,
    charsetTarget,
    ecc,
    color,
    bgColor,
    margin,
    qzone,
  };
};

const createQRCodeURL = () => {
  const formData = collectFormData(createQRCodeForm);

  const url = new URL("https://api.qrserver.com/v1/create-qr-code");
  url.searchParams.set("data", formData.content);
  url.searchParams.set("size", formData.size);
  url.searchParams.set("charset-source", formData.charsetSource);
  url.searchParams.set("charset-target", formData.charsetTarget);
  url.searchParams.set("ecc", formData.ecc);
  url.searchParams.set("color", formData.color);
  url.searchParams.set("bgcolor", formData.bgColor);
  url.searchParams.set("margin", formData.margin);
  url.searchParams.set("qzone", formData.qzone);
  url.searchParams.set("format", fileFormat);

  return url.href;
};

if (createQRBtn) {
  createQRBtn.addEventListener("click", function (event) {
    qrCodeUrl = createQRCodeURL();
    document.querySelector(".qrcode-img").src = qrCodeUrl;
    document.querySelector(".container.px-0").innerHTML = "";
  });
}

if (saveQRBtn) {
  saveQRBtn.addEventListener("click", async function (event) {
    qrCodeUrl = createQRCodeURL();

    await axios.post("/user/qrcode", {
      qrCodeUrl,
    });

    const alertDiv = document.createElement("div");
    alertDiv.setAttribute("class", "alert alert-success");
    alertDiv.append("Your QR Code has been saved successfully.");
    document.querySelector(".container.px-0").appendChild(alertDiv);
  });
}

if (updateQRBtn) {
  updateQRBtn.addEventListener("click", async function (event) {
    qrCodeUrl = createQRCodeURL();

    await axios.post("/user/qrcode/update", {
      qrCodeUrl,
      qrCodeId,
    });

    const alertDiv = document.createElement("div");
    alertDiv.setAttribute("class", "alert alert-success");
    alertDiv.append("QR Code updated!");
    document.querySelector(".container.px-0").appendChild(alertDiv);
  });
}

if (downloadQRBtn) {
  downloadQRBtn.addEventListener("click", async function (event) {
    if (!qrCodeUrl) {
      createQRBtn.click();
    }

    const response = await axios.get(qrCodeUrl, {
      responseType: "blob",
    });

    const href = URL.createObjectURL(response.data);
    const link = document.createElement("a");
    link.href = href;
    link.setAttribute("download", `qrcode.${fileFormat}`);
    document.body.appendChild(link);
    link.click();

    document.body.removeChild(link);
    URL.revokeObjectURL(href);
  });
}
