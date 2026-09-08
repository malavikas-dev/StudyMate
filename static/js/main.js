// ==========================================
// STUDYMATE JAVASCRIPT
// ==========================================

document.addEventListener("DOMContentLoaded", function () {

    // ==========================================
    // LOAD SAVED THEME
    // ==========================================

    const savedTheme = localStorage.getItem("theme");

    if (savedTheme === "dark") {
        document.body.classList.add("dark-mode");
    }


    // ==========================================
    // PROGRESS BARS
    // ==========================================

    const progressBars = document.querySelectorAll("[data-width]");

    progressBars.forEach(function (bar) {

        const width = bar.getAttribute("data-width");

        if (width !== null) {
            bar.style.width = Math.min(Math.max(parseFloat(width) || 0, 0), 100) + "%";
        }

    });


    // ==========================================
    // EXAM COUNTDOWN
    // ==========================================

    const countdowns = document.querySelectorAll(".countdown");

    countdowns.forEach(function (element) {

        const examDate = element.getAttribute("data-exam-date");

        if (!examDate) {
            element.textContent = "No exam date";
            return;
        }

        const exam = new Date(examDate + "T00:00:00");

        const today = new Date();
        today.setHours(0, 0, 0, 0);

        const difference = exam - today;

        const days = Math.ceil(
            difference / (1000 * 60 * 60 * 24)
        );

        if (days < 0) {
            element.textContent = "Exam completed";
        }
        else if (days === 0) {
            element.textContent = "Today";
        }
        else if (days === 1) {
            element.textContent = "1 day left";
        }
        else {
            element.textContent = days + " days left";
        }

    });


    // ==========================================
    // AUTO HIDE ALERTS
    // ==========================================

    const alerts = document.querySelectorAll(".alert");

    alerts.forEach(function (alert) {

        setTimeout(function () {

            alert.style.opacity = "0";

            setTimeout(function () {
                alert.remove();
            }, 300);

        }, 4000);

    });

});


// ==========================================
// THEME TOGGLE
// ==========================================

function toggleTheme() {

    document.body.classList.toggle("dark-mode");

    if (document.body.classList.contains("dark-mode")) {

        localStorage.setItem("theme", "dark");

    } else {

        localStorage.setItem("theme", "light");

    }

}


// ==========================================
// SIDEBAR MOBILE TOGGLE
// ==========================================

function toggleSidebar() {

    const sidebar = document.querySelector(".sidebar");

    if (sidebar) {
        sidebar.classList.toggle("sidebar-open");
    }

}


// ==========================================
// CONFIRM DELETE
// ==========================================

function confirmDelete(message) {

    return confirm(
        message || "Are you sure you want to delete this?"
    );

}

function toggleNotifications() {

    const panel = document.getElementById("notificationPanel");

    if (!panel) return;

    panel.classList.toggle("show");
}


// Close notification panel when clicking outside

document.addEventListener("click", function(event) {

    const wrapper = document.querySelector(".notification-wrapper");
    const panel = document.getElementById("notificationPanel");

    if (!wrapper || !panel) return;

    if (!wrapper.contains(event.target)) {
        panel.classList.remove("show");
    }

});