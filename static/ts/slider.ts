class Slider {
    private slides: NodeListOf<HTMLElement>;
    private dots: NodeListOf<HTMLElement>;
    private currentIndex: number = 0;
    private intervalId: number | null = null;
    private autoplayInterval: number = 4000;

    constructor() {
        this.slides = document.querySelectorAll('.slide');
        this.dots = document.querySelectorAll('.dot');
        
        if (this.slides.length === 0) return;
        this.init();
    }

    private init(): void {
        const prevBtn = document.getElementById('slider-prev');
        const nextBtn = document.getElementById('slider-next');

        if (prevBtn) prevBtn.addEventListener('click', () => this.prev());
        if (nextBtn) nextBtn.addEventListener('click', () => this.next());

        this.dots.forEach((dot) => {
            dot.addEventListener('click', (e) => {
                const target = e.target as HTMLElement;
                const index = Number(target.dataset.index);
                this.goTo(index);
            });
        });

        this.startAutoplay();

        const container = document.getElementById('silant-slider');
        if (container) {
            container.addEventListener('mouseenter', () => this.stopAutoplay());
            container.addEventListener('mouseleave', () => this.startAutoplay());
        }
    }

    private goTo(index: number): void {
        this.currentIndex = index;
        this.update();
    }

    private next(): void {
        this.currentIndex = (this.currentIndex + 1) % this.slides.length;
        this.update();
    }

    private prev(): void {
        this.currentIndex = (this.currentIndex - 1 + this.slides.length) % this.slides.length;
        this.update();
    }

    private update(): void {
        this.slides.forEach((slide, i) => {
            slide.classList.toggle('active', i === this.currentIndex);
        });
        this.dots.forEach((dot, i) => {
            dot.classList.toggle('active', i === this.currentIndex);
        });
    }

    private startAutoplay(): void {
        if (this.intervalId) return;
        this.intervalId = window.setInterval(() => this.next(), this.autoplayInterval);
    }

    private stopAutoplay(): void {
        if (this.intervalId) {
            clearInterval(this.intervalId);
            this.intervalId = null;
        }
    }
}

document.addEventListener('DOMContentLoaded', () => {
    new Slider();
});