"use strict";
class Slider {
    constructor() {
        this.currentIndex = 0;
        this.intervalId = null;
        this.autoplayInterval = 4000;
        this.slides = document.querySelectorAll('.slide');
        this.dots = document.querySelectorAll('.dot');
        if (this.slides.length === 0)
            return;
        this.init();
    }
    init() {
        const prevBtn = document.getElementById('slider-prev');
        const nextBtn = document.getElementById('slider-next');
        if (prevBtn)
            prevBtn.addEventListener('click', () => this.prev());
        if (nextBtn)
            nextBtn.addEventListener('click', () => this.next());
        this.dots.forEach((dot) => {
            dot.addEventListener('click', (e) => {
                const target = e.target;
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
    goTo(index) {
        this.currentIndex = index;
        this.update();
    }
    next() {
        this.currentIndex = (this.currentIndex + 1) % this.slides.length;
        this.update();
    }
    prev() {
        this.currentIndex = (this.currentIndex - 1 + this.slides.length) % this.slides.length;
        this.update();
    }
    update() {
        this.slides.forEach((slide, i) => {
            slide.classList.toggle('active', i === this.currentIndex);
        });
        this.dots.forEach((dot, i) => {
            dot.classList.toggle('active', i === this.currentIndex);
        });
    }
    startAutoplay() {
        if (this.intervalId)
            return;
        this.intervalId = window.setInterval(() => this.next(), this.autoplayInterval);
    }
    stopAutoplay() {
        if (this.intervalId) {
            clearInterval(this.intervalId);
            this.intervalId = null;
        }
    }
}
document.addEventListener('DOMContentLoaded', () => {
    new Slider();
});
