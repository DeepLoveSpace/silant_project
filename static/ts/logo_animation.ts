document.addEventListener('DOMContentLoaded', () => {
    const container = document.getElementById('logo-animation');
    const logo = container?.querySelector('.flying-logo') as HTMLImageElement | null;

    if (!container || !logo) return;

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
