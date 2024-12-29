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
                    console.log("Dark mode enabled"); // Konsola mesaj yaz
                } else {
                    localStorage.setItem("darkMode", "disabled");
                    document.body.classList.remove("dark-mode");
                    console.log("Dark mode disabled"); // Konsola mesaj yaz
                }
            });
        });