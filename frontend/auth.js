// Authentication Logic for AEIS

// Demo credentials (In production, this would use Supabase)
const DEMO_USERS = {
    'admin': {
        email: 'admin@aeis.gov.in',
        password: 'admin123',
        userId: 'admin'
    }
};

// Panel switching
document.getElementById('showSignup')?.addEventListener('click', (e) => {
    e.preventDefault();
    switchPanel('signupPanel');
});

document.getElementById('showLogin')?.addEventListener('click', (e) => {
    e.preventDefault();
    switchPanel('loginPanel');
});

document.getElementById('showForgotPassword')?.addEventListener('click', (e) => {
    e.preventDefault();
    switchPanel('forgotPanel');
});

document.getElementById('backToLogin')?.addEventListener('click', (e) => {
    e.preventDefault();
    switchPanel('loginPanel');
});

function switchPanel(panelId) {
    document.querySelectorAll('.auth-panel').forEach(panel => {
        panel.classList.remove('active');
    });
    document.getElementById(panelId).classList.add('active');
}

// Login Form
document.getElementById('loginForm')?.addEventListener('submit', (e) => {
    e.preventDefault();

    const userId = document.getElementById('loginUserId').value;
    const email = document.getElementById('loginEmail').value;
    const password = document.getElementById('loginPassword').value;

    // Check credentials (Demo logic)
    const user = DEMO_USERS[userId];

    if (user && user.email === email && user.password === password) {
        // Success - redirect to dashboard
        sessionStorage.setItem('authenticated', 'true');
        sessionStorage.setItem('userId', userId);
        window.location.href = 'index.html';
    } else {
        // Show warning modal
        showWarningModal();
    }
});

// Sign Up Form - OTP Flow
document.getElementById('sendSignupOtp')?.addEventListener('click', () => {
    const userId = document.getElementById('signupUserId').value;
    const email = document.getElementById('signupEmail').value;
    const password = document.getElementById('signupPassword').value;
    const confirmPassword = document.getElementById('signupConfirmPassword').value;

    if (!userId || !email || !password || !confirmPassword) {
        alert('Please fill in all fields');
        return;
    }

    if (password !== confirmPassword) {
        alert('Passwords do not match');
        return;
    }

    // Simulate sending OTP
    alert(`OTP has been sent to ${email} (Demo: use 123456)`);

    // Show OTP section
    document.getElementById('signupOtpSection').style.display = 'block';
});

document.getElementById('signupForm')?.addEventListener('submit', (e) => {
    e.preventDefault();

    const otp = document.getElementById('signupOtp').value;

    // Demo OTP validation
    if (otp === '123456') {
        alert('Account created successfully! Please login.');
        switchPanel('loginPanel');
    } else {
        alert('Invalid OTP. Please try again.');
    }
});

// Forgot Password Flow
document.getElementById('sendForgotOtp')?.addEventListener('click', () => {
    const identifier = document.getElementById('forgotIdentifier').value;

    if (!identifier) {
        alert('Please enter your User ID or Email');
        return;
    }

    // Simulate sending OTP
    alert(`OTP has been sent to your registered email (Demo: use 123456)`);

    document.getElementById('forgotOtpSection').style.display = 'block';
});

document.getElementById('verifyForgotOtp')?.addEventListener('click', () => {
    const otp = document.getElementById('forgotOtp').value;

    if (otp === '123456') {
        alert('OTP verified! Please enter your new password.');
        document.getElementById('newPasswordSection').style.display = 'block';
    } else {
        alert('Invalid OTP. Please try again.');
    }
});

document.getElementById('sendPasswordOtp')?.addEventListener('click', () => {
    const newPassword = document.getElementById('newPassword').value;
    const confirmNewPassword = document.getElementById('confirmNewPassword').value;

    if (!newPassword || !confirmNewPassword) {
        alert('Please enter and confirm your new password');
        return;
    }

    if (newPassword !== confirmNewPassword) {
        alert('Passwords do not match');
        return;
    }

    // Simulate sending confirmation OTP
    alert('Confirmation OTP sent to your email (Demo: use 123456)');
    document.getElementById('finalOtpGroup').style.display = 'block';
    document.getElementById('resetPasswordBtn').style.display = 'block';
});

document.getElementById('forgotForm')?.addEventListener('submit', (e) => {
    e.preventDefault();

    const finalOtp = document.getElementById('finalOtp').value;

    if (finalOtp === '123456') {
        alert('Password reset successfully! Please login with your new password.');
        switchPanel('loginPanel');
    } else {
        alert('Invalid OTP. Please try again.');
    }
});

// Warning Modal
function showWarningModal() {
    const modal = document.getElementById('warningModal');
    modal.classList.add('active');
}

document.getElementById('closeModal')?.addEventListener('click', () => {
    const modal = document.getElementById('warningModal');
    modal.classList.remove('active');
});

// Close modal on outside click
document.getElementById('warningModal')?.addEventListener('click', (e) => {
    if (e.target.id === 'warningModal') {
        e.target.classList.remove('active');
    }
});

// Keyboard navigation
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
        const modal = document.getElementById('warningModal');
        if (modal && modal.classList.contains('active')) {
            modal.classList.remove('active');
        }
    }
});
