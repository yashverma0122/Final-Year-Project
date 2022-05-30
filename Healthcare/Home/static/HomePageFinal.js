const animationOptions = {
    duration: 500,
    fill: "both",
    easing: "cubic-bezier(0.42, 0.0, 0.58, 1.0)"
/*easing: "cubic-bezier(0.82, 0.04, 0.33, 0.98)"*/ };
  
  
  const showKeyframes = dir => {
    return [100 * dir, 0].map(t => ({ transform: `translateX(${t}%)` }));
  };
  
  const hideKeyframes = dir => {
    return [0, -100 * dir].map(t => ({ transform: `translateX(${t}%)` }));
  };
  
  const slideAnimation = options => keyframes => (element, callback) => {
    const animation = element.animate(keyframes, options);
    function handler() {
      callback = callback || function () {};
      callback.call(this);
      animation.removeEventListener('finish', handler);
    }
    animation.addEventListener('finish', handler, { once: true });
  };
  const actionSlide = slideAnimation(animationOptions);
  const showSlide = dir => actionSlide(showKeyframes(dir));
  const hideSlide = dir => actionSlide(hideKeyframes(dir));
  
  class Slider {
    constructor(props) {
      this.rootElement = props.element;
      this.slides = Array.from(
      this.rootElement.querySelectorAll(".slider-list__item"));
  
      this.slidesLength = this.slides.length;
      this.current = 0;
      this.isAnimating = false;
      this.direction = 1; // -1
      this.duration = 0.5;
      this.navBar = this.rootElement.querySelector(".slider__nav-bar");
      this.thumbs = Array.from(this.rootElement.querySelectorAll(".nav-control"));
      this.prevButton = this.rootElement.querySelector(".slider__arrow_prev");
      this.nextButton = this.rootElement.querySelector(".slider__arrow_next");
  
      this.slides[this.current].classList.add("slider-list__item_active");
      this.thumbs[this.current].classList.add("nav-control_active");
  
      this._bindEvents();
    }
  
    goTo(index, dir) {
      if (this.isAnimating) return;
      var self = this;
      let prevSlide = this.slides[this.current];
      let nextSlide = this.slides[index];
  
      self.isAnimating = true;
      self.current = index;
      nextSlide.classList.add("slider-list__item_active");
  
      showSlide(dir)(nextSlide, () => {});
  
      hideSlide(dir)(prevSlide, function () {
        self.isAnimating = false;
        prevSlide.classList.remove("slider-list__item_active");
        self.thumbs.forEach((item, index) => {
          var action = index === self.current ? "add" : "remove";
          item.classList[action]("nav-control_active");
        });
      });
    }
  
    goStep(dir) {
      let index = this.current + dir;
      let len = this.slidesLength;
      let currentIndex = (index + len) % len;
      this.goTo(currentIndex, dir);
    }
  
    goNext() {
      this.goStep(1);
    }
  
    goPrev() {
      this.goStep(-1);
    }
  
    _navClickHandler(e) {
      var self = this;
      if (self.isAnimating) return;
      let target = e.target.closest(".nav-control");
      if (!target) return;
      let index = self.thumbs.indexOf(target);
      if (index === self.current) return;
      let direction = index > self.current ? 1 : -1;
      self.goTo(index, direction);
    }
  
    _bindEvents() {
      var self = this;
      ["goNext", "goPrev", "_navClickHandler"].forEach(method => {
        self[method] = self[method].bind(self);
      });
      self.nextButton.addEventListener("click", self.goNext);
      self.prevButton.addEventListener("click", self.goPrev);
      self.navBar.addEventListener("click", self._navClickHandler);
    }}
  
  
  let slider = new Slider({
    element: document.querySelector(".slider") });