
// code for saving the settings
document.addEventListener("DOMContentLoaded", function () {

    const darkMode = document.getElementById('darkMode');
    const disableNotifications = document.getElementById('disableNotifications');
    const auditiv = document.getElementById('auditiv');
    const notification = document.getElementById('notification');
    const ampel = document.getElementById('ampel');
    const balken = document.getElementById('balken');


    darkMode.checked = localStorage.getItem('darkMode') === 'true';
    disableNotifications.checked = localStorage.getItem('disableNotifications') === 'true';
    auditiv.checked = localStorage.getItem('auditiv') === 'true';
    notification.checked = localStorage.getItem('notification') === 'true';
    if (localStorage.getItem('popupView') === 'ampel') {
        ampel.checked = true;
    } else if (localStorage.getItem('popupView') === 'balken') {
        balken.checked = true;
    }


    darkMode.addEventListener('change', () => localStorage.setItem('darkMode', darkMode.checked));
    disableNotifications.addEventListener('change', () => localStorage.setItem('disableNotifications', disableNotifications.checked));
    auditiv.addEventListener('change', () => localStorage.setItem('auditiv', auditiv.checked));
    notification.addEventListener('change', () => localStorage.setItem('notification', notification.checked));
    ampel.addEventListener('change', () => localStorage.setItem('popupView', 'ampel'));
    balken.addEventListener('change', () => localStorage.setItem('popupView', 'balken'));
});