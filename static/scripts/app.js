"use strict";

// Buttons
const createQRBtn = document.querySelector(".create-qr-btn");
const saveQRBtn = document.querySelector(".save-qr-btn");
const downloadQRBtn = document.querySelector(".download-qr-btn");
let qrCodeUrl = null;
let fileFormat = null;

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
  });
}

if (saveQRBtn) {
  saveQRBtn.addEventListener("click", async function (event) {
    qrCodeUrl = createQRCodeURL();

    await axios.post("/user/qrcode", {
      qrCodeUrl,
    });
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
