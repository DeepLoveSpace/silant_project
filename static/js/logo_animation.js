"use strict";
document.addEventListener('DOMContentLoaded', () => {
    const container = document.getElementById('logo-animation');
    const logo = container === null || container === void 0 ? void 0 : container.querySelector('.flying-logo');
    if (!container || !logo)
        return;
    void container.offsetWidth;
    requestAnimationFrame(() => {
        requestAnimationFrame(() => {
            setTimeout(() => {
                container.classList.add('active');
            }, 200);
        });
    });
    setTimeout(() => {
        logo.classList.add('spinning');
    }, 2200);
    setTimeout(() => {
        container.classList.add('finished');
    }, 7200);
    setTimeout(() => {
        container.remove();
    }, 9200);
});