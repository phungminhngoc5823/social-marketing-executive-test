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

  /* ---------- Active section highlight in the top nav ---------- */
  var navLinks = Array.prototype.slice.call(document.querySelectorAll('.nav__menu a[href^="#"]'));
  var sections = navLinks
    .map(function (a) { return document.querySelector(a.getAttribute("href")); })
    .filter(Boolean);

  function setActive(id) {
    navLinks.forEach(function (a) {
      var on = a.getAttribute("href") === id;
      a.classList.toggle("is-active", on);
      if (on) a.setAttribute("aria-current", "true"); else a.removeAttribute("aria-current");
    });
  }

  if ("IntersectionObserver" in window && sections.length) {
    var spy = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) setActive("#" + entry.target.id);
      });
    }, { rootMargin: "-35% 0px -60% 0px" });
    sections.forEach(function (s) { spy.observe(s); });
    // Clear the highlight while the hero is on screen.
    var hero = document.getElementById("top");
    if (hero) {
      new IntersectionObserver(function (entries) {
        if (entries[0].isIntersecting && entries[0].intersectionRatio > 0.4) setActive(null);
      }, { threshold: [0.4] }).observe(hero);
    }
  }

  /* ---------- Script tables: current row + sticky progress ---------- */
  Array.prototype.forEach.call(document.querySelectorAll("[data-script]"), function (script) {
    var rows = Array.prototype.slice.call(script.querySelectorAll(".srow"));
    var segs = Array.prototype.slice.call(script.querySelectorAll(".sprog__seg"));
    if (!rows.length || !("IntersectionObserver" in window)) return;

    function mark(idx) {
      rows.forEach(function (r, i) { r.classList.toggle("is-current", i === idx); });
      segs.forEach(function (s, i) {
        s.classList.toggle("is-active", i === idx);
        s.classList.toggle("is-done", i < idx);
      });
    }
    var ro = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) mark(parseInt(entry.target.getAttribute("data-row"), 10));
      });
    }, { rootMargin: "-40% 0px -55% 0px" });
    rows.forEach(function (r) { ro.observe(r); });
  });

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
