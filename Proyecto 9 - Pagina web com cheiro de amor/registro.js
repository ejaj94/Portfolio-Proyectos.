document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('register-form');
  const password = document.getElementById('password');
  const confirmPassword = document.getElementById('confirmPassword');
  const passwordError = document.getElementById('password-error');
  const phoneInput = document.getElementById('phone');
  const phoneError = document.getElementById('phone-error');
  const btnSubmit = document.getElementById('btn-submit');
  const verificationStep = document.getElementById('verification-step');
  const btnVerify = document.getElementById('btn-verify');

  // Initialize intl-tel-input
  const iti = window.intlTelInput(phoneInput, {
    initialCountry: "auto",
    geoIpLookup: function(success, failure) {
      fetch("https://ipapi.co/json")
        .then(res => res.json())
        .then(data => success(data.country_code))
        .catch(() => success("pt"));
    },
    utilsScript: "https://cdnjs.cloudflare.com/ajax/libs/intl-tel-input/17.0.8/js/utils.js",
  });

  // Handle form submission
  form.addEventListener('submit', (e) => {
    e.preventDefault();
    let isValid = true;

    // Check passwords
    if (password.value !== confirmPassword.value) {
      passwordError.textContent = "Las contraseñas no coinciden.";
      isValid = false;
    } else {
      passwordError.textContent = "";
    }

    // Check phone
    if (!iti.isValidNumber()) {
      phoneError.textContent = "Número de celular inválido para este país.";
      isValid = false;
    } else {
      phoneError.textContent = "";
    }

    if (isValid) {
      // Simulate API call to Firebase
      btnSubmit.textContent = "Registrando...";
      btnSubmit.disabled = true;

      setTimeout(() => {
        // Hide form, show verification
        form.classList.add('hidden');
        verificationStep.classList.remove('hidden');
      }, 1500);
    }
  });

  // Handle Mock Verification
  btnVerify.addEventListener('click', () => {
    btnVerify.textContent = "Verificando...";
    btnVerify.disabled = true;

    setTimeout(() => {
      alert("¡Cuenta verificada y creada con éxito! Bienvenid@ a los Workshops.");
      window.location.href = "index.html";
    }, 1500);
  });
});
