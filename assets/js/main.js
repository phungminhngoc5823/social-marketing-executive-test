(function () {
  "use strict";

  var doc = document.documentElement;
  var reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ---------- Load-in choreography ---------- */
  function markLoaded() {
    requestAnimationFrame(function () { doc.classList.add("is-loaded"); });
  }
  if (document.readyState === "complete") markLoaded();
  else window.addEventListener("load", markLoaded);
  // Safety net in case fonts/images stall the load event.
  setTimeout(markLoaded, 1200);

  /* ---------- Nav: scrolled state + progress bar ---------- */
  var nav = document.querySelector("[data-nav]");
  var bar = document.querySelector("[data-progress]");
  var ticking = false;

  function onScroll() {
    var y = window.scrollY || window.pageYOffset;
    var max = document.body.scrollHeight - window.innerHeight;
    if (nav) nav.classList.toggle("is-scrolled", y > 8);
    if (bar) bar.style.transform = "scaleX(" + (max > 0 ? Math.min(y / max, 1) : 0) + ")";
    ticking = false;
  }
  window.addEventListener("scroll", function () {
    if (!ticking) { requestAnimationFrame(onScroll); ticking = true; }
  }, { passive: true });
  onScroll();

  /* ---------- Mobile menu ---------- */
  var toggle = document.querySelector("[data-nav-toggle]");
  var menu = document.getElementById("nav-menu");
  function setMenu(open) {
    if (!toggle || !menu) return;
    toggle.setAttribute("aria-expanded", String(open));
    toggle.setAttribute("aria-label", open ? "Close menu" : "Open menu");
    menu.classList.toggle("is-open", open);
  }
  if (toggle && menu) {
    toggle.addEventListener("click", function () {
      setMenu(toggle.getAttribute("aria-expanded") !== "true");
    });
    menu.addEventListener("click", function (e) {
      if (e.target.closest("a")) setMenu(false);
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape") setMenu(false);
    });
  }

  /* ---------- Active section highlight (top nav + sidebar) ---------- */
  var navLinks = Array.prototype.slice.call(document.querySelectorAll('.nav__menu a[href^="#"]'));
  var sideLinks = Array.prototype.slice.call(document.querySelectorAll('.sidebar__link[href^="#"]'));
  var sectionIds = sideLinks.map(function (a) { return a.getAttribute("href"); });
  var sections = sectionIds
    .map(function (id) { return document.querySelector(id); })
    .filter(Boolean);

  function setActive(id) {
    navLinks.forEach(function (a) { a.classList.toggle("is-active", a.getAttribute("href") === id); });
    var idx = sectionIds.indexOf(id);
    sideLinks.forEach(function (a, i) {
      a.classList.toggle("is-active", i === idx);
      a.classList.toggle("is-done", idx > -1 && i < idx);
      if (i === idx) {
        a.setAttribute("aria-current", "true");
        // Keep the active chip visible in the mobile horizontal stepper.
        var list = a.closest(".sidebar__list");
        if (list && list.scrollWidth > list.clientWidth) {
          list.scrollTo({ left: a.parentNode.offsetLeft - 16, behavior: reduceMotion ? "auto" : "smooth" });
        }
      } else {
        a.removeAttribute("aria-current");
      }
    });
  }

  if ("IntersectionObserver" in window && sections.length) {
    var spy = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) setActive("#" + entry.target.id);
      });
    }, { rootMargin: "-35% 0px -60% 0px" });
    sections.forEach(function (s) { spy.observe(s); });
  }

  /* ---------- At a glance: column highlight (desktop hover) / tabs (mobile) ---------- */
  var glance = document.querySelector("[data-glance]");
  if (glance) {
    var cells = glance.querySelectorAll("[data-col]");
    var tabs = glance.querySelectorAll("[data-glance-tab]");
    var mobile = window.matchMedia("(max-width: 720px)");
    var selected = "a";

    function paint(col) {
      cells.forEach(function (c) {
        var on = col && c.getAttribute("data-col") === col;
        c.classList.toggle("is-hl", !!on);
        c.classList.toggle("is-dim", !!col && !on);
      });
    }
    function selectTab(col) {
      selected = col;
      tabs.forEach(function (t) { t.setAttribute("aria-selected", String(t.getAttribute("data-glance-tab") === col)); });
      if (mobile.matches) paint(col);
    }
    function sync() { paint(mobile.matches ? selected : null); }

    tabs.forEach(function (t) {
      t.addEventListener("click", function () { selectTab(t.getAttribute("data-glance-tab")); });
    });
    cells.forEach(function (c) {
      c.addEventListener("mouseenter", function () { if (!mobile.matches) paint(c.getAttribute("data-col")); });
    });
    glance.addEventListener("mouseleave", function () { if (!mobile.matches) paint(null); });
    if (mobile.addEventListener) mobile.addEventListener("change", sync);
    else if (mobile.addListener) mobile.addListener(sync);
    sync();
  }

  /* ---------- Reveal on scroll (outside the hero) ---------- */
  var reveals = document.querySelectorAll(".reveal:not(.hero .reveal)");
  if ("IntersectionObserver" in window && !reduceMotion) {
    var io = new IntersectionObserver(function (entries, obs) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add("is-in");
          obs.unobserve(entry.target);
        }
      });
    }, { threshold: 0.15 });
    reveals.forEach(function (el) { io.observe(el); });
  } else {
    reveals.forEach(function (el) { el.classList.add("is-in"); });
  }

  /* ---------- Count-up numbers ---------- */
  function countUp(el) {
    var target = parseInt(el.getAttribute("data-count"), 10);
    if (isNaN(target) || reduceMotion) return;
    var start = null;
    var duration = target > 10 ? 1400 : 700;
    function step(ts) {
      if (!start) start = ts;
      var p = Math.min((ts - start) / duration, 1);
      var eased = 1 - Math.pow(1 - p, 3);
      el.textContent = Math.round(target * eased);
      if (p < 1) requestAnimationFrame(step);
    }
    el.textContent = "0";
    requestAnimationFrame(step);
  }

  var counters = document.querySelectorAll("[data-count]");
  if ("IntersectionObserver" in window) {
    var co = new IntersectionObserver(function (entries, obs) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          // Small delay so the count starts as the facts row fades in.
          setTimeout(function () { countUp(entry.target); }, 650);
          obs.unobserve(entry.target);
        }
      });
    }, { threshold: 0.6 });
    counters.forEach(function (el) { co.observe(el); });
  }
})();
