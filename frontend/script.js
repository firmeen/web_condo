const API_BASE_URL = 'http://127.0.0.1:5000';

const navToggle = document.querySelector('.nav-toggle');
const navMenu = document.querySelector('.nav-menu');
const navLinks = document.querySelectorAll('.nav-menu a');
const form = document.getElementById('inquiryForm');
const feedbackEl = document.getElementById('formFeedback');
const submitBtn = form?.querySelector('.btn-submit');
const lightbox = document.getElementById('lightbox');
const lightboxImage = document.getElementById('lightboxImage');
const lightboxCaption = document.getElementById('lightboxCaption');
const lightboxClose = document.querySelector('.lightbox-close');
const galleryItems = document.querySelectorAll('.gallery-item');

let isSubmitting = false;
let lastSubmitFingerprint = '';

navToggle?.addEventListener('click', () => {
  const isExpanded = navToggle.getAttribute('aria-expanded') === 'true';
  navToggle.setAttribute('aria-expanded', String(!isExpanded));
  navMenu.classList.toggle('open');
});

navLinks.forEach((link) => {
  link.addEventListener('click', () => {
    navMenu.classList.remove('open');
    navToggle?.setAttribute('aria-expanded', 'false');
  });
});

for (const item of galleryItems) {
  item.addEventListener('click', () => {
    const image = item.querySelector('img');
    if (!image || !lightbox) return;
    lightboxImage.src = image.src;
    lightboxImage.alt = image.alt;
    lightboxCaption.textContent = item.dataset.caption || '';
    lightbox.showModal();
  });
}

lightboxClose?.addEventListener('click', () => lightbox.close());
lightbox?.addEventListener('click', (event) => {
  const rect = lightbox.getBoundingClientRect();
  const clickedOutside =
    event.clientX < rect.left ||
    event.clientX > rect.right ||
    event.clientY < rect.top ||
    event.clientY > rect.bottom;

  if (clickedOutside) lightbox.close();
});

function setFeedback(message, type = '') {
  feedbackEl.textContent = message;
  feedbackEl.className = `form-feedback ${type}`.trim();
}

function normalizePhone(phone) {
  return phone.replace(/[\s()-]/g, '');
}

function validateForm(data) {
  if (!data.full_name || data.full_name.trim().length < 2) {
    return 'กรุณากรอกชื่อ-นามสกุลให้ครบถ้วน';
  }

  const phone = normalizePhone(data.phone || '');
  if (!/^\+?[0-9]{8,15}$/.test(phone)) {
    return 'กรุณากรอกเบอร์โทรศัพท์ให้ถูกต้อง';
  }

  if (data.email && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(data.email)) {
    return 'กรุณากรอกอีเมลให้ถูกต้อง';
  }

  if (!data.consent) {
    return 'กรุณายินยอมให้ติดต่อกลับก่อนส่งข้อมูล';
  }

  return '';
}

function toPayload(formData) {
  return {
    full_name: formData.get('full_name')?.trim() || '',
    phone: normalizePhone(formData.get('phone') || ''),
    email: formData.get('email')?.trim() || '',
    preferred_building: formData.get('preferred_building') || '',
    preferred_date: formData.get('preferred_date') || '',
    preferred_time: formData.get('preferred_time') || '',
    message: formData.get('message')?.trim() || '',
    consent: formData.get('consent') === 'on',
  };
}

form?.addEventListener('submit', async (event) => {
  event.preventDefault();

  if (isSubmitting) return;

  const payload = toPayload(new FormData(form));
  const validationError = validateForm(payload);

  if (validationError) {
    setFeedback(validationError, 'error');
    return;
  }

  const fingerprint = JSON.stringify(payload);
  if (fingerprint === lastSubmitFingerprint) {
    setFeedback('คุณส่งข้อมูลชุดเดิมไปแล้ว กรุณารอสักครู่ก่อนส่งใหม่', 'error');
    return;
  }

  try {
    isSubmitting = true;
    lastSubmitFingerprint = fingerprint;
    submitBtn.disabled = true;
    submitBtn.textContent = 'กำลังส่งข้อมูล...';
    setFeedback('');

    const response = await fetch(`${API_BASE_URL}/api/inquiries`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });

    const result = await response.json();

    if (!response.ok) {
      setFeedback(result.message || 'ไม่สามารถส่งข้อมูลได้ กรุณาลองใหม่', 'error');
      return;
    }

    setFeedback('ส่งคำขอนัดดูห้องเรียบร้อยแล้ว ทีมงานจะติดต่อกลับเร็วที่สุด', 'success');
    form.reset();
  } catch (error) {
    setFeedback('เกิดข้อผิดพลาดในการเชื่อมต่อ กรุณาลองใหม่อีกครั้ง', 'error');
  } finally {
    isSubmitting = false;
    submitBtn.disabled = false;
    submitBtn.textContent = 'ส่งคำขอนัดดูห้อง';
    setTimeout(() => {
      lastSubmitFingerprint = '';
    }, 8000);
  }
});
