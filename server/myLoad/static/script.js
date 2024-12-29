 document.addEventListener("DOMContentLoaded", function () {
            const isDarkModeEnabled = localStorage.getItem("darkMode") === "enabled";
            const darkModeCheckbox = document.getElementById("darkModeToggle");

            if (isDarkModeEnabled) {
                document.body.classList.add("dark-mode");
                darkModeCheckbox.checked = true;
            }


            darkModeCheckbox.addEventListener("change", function () {
                if (this.checked) {
                    localStorage.setItem("darkMode", "enabled");
                    document.body.classList.add("dark-mode");
                } else {
                    localStorage.setItem("darkMode", "disabled");
                    document.body.classList.remove("dark-mode");
                }
            });
        });