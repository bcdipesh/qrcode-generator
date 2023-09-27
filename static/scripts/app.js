'use strict';

// Buttons
const createQRBtn = document.querySelector('.create-qr-btn');
const downloadQRBtn = document.querySelector('.download-qr-btn');
let qrCodeUrl = null;
let fileFormat = null;

// Form
const createQRCodeForm = document.querySelector('.qr-code-form');

createQRBtn.addEventListener('click', async function (event) {
	// Collect form data
	const content = createQRCodeForm.elements['content'].value;
	const size = createQRCodeForm.elements['size'].value;
	const charsetSource = createQRCodeForm.elements['charset_source'].value;
	const charsetTarget = createQRCodeForm.elements['charset_target'].value;
	const ecc = createQRCodeForm.elements['ecc'].value;
	const color = createQRCodeForm.elements['color'].value;
	const bgColor = createQRCodeForm.elements['bg_color'].value;
	const margin = createQRCodeForm.elements['margin'].value;
	const qzone = createQRCodeForm.elements['qzone'].value;
	fileFormat = createQRCodeForm.elements['file_format'].value;

	qrCodeUrl = `https://api.qrserver.com/v1/create-qr-code/?data=${content}`;

	// Update QR Code image
	document.querySelector('.qrcode-img').src = qrCodeUrl;
});

downloadQRBtn.addEventListener('click', async function (event) {
	if (!qrCodeUrl) {
		createQRBtn.click();
	}

	const response = await axios.get(qrCodeUrl, {
		responseType: 'blob',
	});

	const href = URL.createObjectURL(response.data);
	console.log(response);
	const link = document.createElement('a');
	link.href = href;
	link.setAttribute('download', `qrcode.${fileFormat}`);
	document.body.appendChild(link);
	link.click();

	document.body.removeChild(link);
	URL.revokeObjectURL(href);
});
