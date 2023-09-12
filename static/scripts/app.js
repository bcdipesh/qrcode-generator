'use strict';

// Buttons
const createQRBtn = document.querySelector('.create-qr-btn');
const downloadQRBtn = document.querySelector('.download-qr-btn');

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
	const fileFormat = createQRCodeForm.elements['file_format'].value;

	// Update QR Code image
	document.querySelector(
		'.qrcode-img'
	).src = `https://api.qrserver.com/v1/create-qr-code/?data=${content}`;
});

downloadQRBtn.addEventListener('click', function (event) {
	console.log(this);
});
