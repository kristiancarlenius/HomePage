// Carlenius AI site behavior: mobile nav, scroll-spy, theme switch, EN/NO language switch.
// No dependencies, no build step.

(function () {
    "use strict";

    /* ---------------- translations ---------------- */
    var translations = {
        en: {
            "nav.services": "Services",
            "nav.about": "About",
            "nav.contact": "Contact",
            "nav.github": "GitHub",
            "nav.login": "Login",
            "nav.toggle": "Toggle navigation",
            "theme.toggle": "Toggle theme",
            "lang.toggle": "Switch language",
            "skip.content": "Skip to content",
            "hero.title": "Tailor-Made<br>Software Solutions",
            "hero.lead": "AI &amp; automation engineered to scale your business.",
            "hero.cta.primary": "Get in touch",
            "hero.cta.secondary": "View services",
            "services.title": "Services",
            "services.01.title": "Process Automation",
            "services.01.body": "We look at the repetitive, manual parts of your workflow and build automated solutions that just run on their own.",
            "services.02.title": "AI Integrations",
            "services.02.body": "From internal assistants to document handling and smarter analysis, we bring AI in where it actually helps people decide faster.",
            "services.03.title": "Custom Tooling",
            "services.03.body": "Internal tools built around exactly how your team works. No generic workaround, no extra layers you don't need.",
            "services.04.title": "Data Flow",
            "services.04.body": "Clean, automated data flow from source to decision, built to grow with your business instead of becoming a problem later.",
            "about.title": "About Carlenius AI",
            "about.p1": "Carlenius AI is a high-end software consultancy specializing in artificial intelligence, automation, and data-driven systems. We design and implement intelligent solutions that streamline workflows, enhance decision-making, and dramatically reduce human workload.",
            "about.p2": "From computer vision and predictive modeling to fully automated pipelines, every solution is custom-built to give your business a competitive edge.",
            "contact.title": "Contact",
            "contact.phone.label": "Phone",
            "contact.location.label": "Location",
            "contact.email.label": "Email",
            "footer.rights": "© 2026 Carlenius AI. All rights reserved."
        },
        no: {
            "nav.services": "Tjenester",
            "nav.about": "Om oss",
            "nav.contact": "Kontakt",
            "nav.github": "GitHub",
            "nav.login": "Logg inn",
            "nav.toggle": "Vis meny",
            "theme.toggle": "Bytt tema",
            "lang.toggle": "Bytt språk",
            "skip.content": "Hopp til innhold",
            "hero.title": "Skreddersydde<br>programvareløsninger",
            "hero.lead": "AI og automasjon som skalerer virksomheten din.",
            "hero.cta.primary": "Ta kontakt",
            "hero.cta.secondary": "Se tjenester",
            "services.title": "Tjenester",
            "services.01.title": "Prosessautomatisering",
            "services.01.body": "Vi finner de tunge, manuelle oppgavene i hverdagen deres og bygger løsninger som tar seg av dem helt automatisk.",
            "services.02.title": "AI-integrasjoner",
            "services.02.body": "Fra interne AI-assistenter til dokumentbehandling og smartere analyser, vi tar i bruk AI der det faktisk hjelper folk ta raskere beslutninger.",
            "services.03.title": "Skreddersydde verktøy",
            "services.03.body": "Interne verktøy bygget nøyaktig for hvordan dere jobber. Ingen generiske omveier, ingen unødvendige lag.",
            "services.04.title": "Dataflyt",
            "services.04.body": "Ryddig, automatisert dataflyt fra kilde til beslutning, bygget for å vokse med virksomheten i stedet for å bli et problem senere.",
            "about.title": "Om Carlenius AI",
            "about.p1": "Carlenius AI er et programvarekonsulentselskap som spesialiserer seg på kunstig intelligens, automasjon og datadrevne systemer. Vi designer og bygger intelligente løsninger som effektiviserer arbeidsflyt, styrker beslutningstaking og reduserer arbeidsmengden betraktelig.",
            "about.p2": "Fra computer vision og prediktiv modellering til fullautomatiserte pipelines, hver løsning er skreddersydd for å gi virksomheten din et konkurransefortrinn.",
            "contact.title": "Kontakt",
            "contact.phone.label": "Telefon",
            "contact.location.label": "Sted",
            "contact.email.label": "E-post",
            "footer.rights": "© 2026 Carlenius AI. Alle rettigheter forbeholdt."
        }
    };

    /* ---------------- theme ----------------
       The page always starts in dark mode (set inline, before paint). The
       toggle below only changes the *current* view; it is intentionally not
       persisted, so every fresh load or reload starts dark again. */
    function applyTheme(theme) {
        document.documentElement.setAttribute("data-theme", theme);
    }

    function initTheme() {
        var current = document.documentElement.getAttribute("data-theme") || "dark";
        var toggle = document.getElementById("themeToggle");
        if (!toggle) return;
        toggle.addEventListener("click", function () {
            current = current === "dark" ? "light" : "dark";
            applyTheme(current);
        });
    }

    /* ---------------- language ---------------- */
    var langLabels = { en: "EN", no: "NO" };

    function applyLanguage(lang) {
        var dict = translations[lang] || translations.en;

        document.querySelectorAll("[data-i18n]").forEach(function (el) {
            var key = el.getAttribute("data-i18n");
            if (dict[key] !== undefined) el.textContent = dict[key];
        });

        document.querySelectorAll("[data-i18n-html]").forEach(function (el) {
            var key = el.getAttribute("data-i18n-html");
            if (dict[key] !== undefined) el.innerHTML = dict[key];
        });

        document.querySelectorAll("[data-i18n-aria]").forEach(function (el) {
            var key = el.getAttribute("data-i18n-aria");
            if (dict[key] !== undefined) el.setAttribute("aria-label", dict[key]);
        });

        var langLabel = document.getElementById("langLabel");
        if (langLabel) langLabel.textContent = langLabels[lang] || "EN";

        document.querySelectorAll(".lang-option").forEach(function (opt) {
            opt.classList.toggle("active", opt.getAttribute("data-lang") === lang);
        });

        document.documentElement.setAttribute("lang", lang === "no" ? "nb" : "en");
        try { localStorage.setItem("lang", lang); } catch (e) {}
    }

    function initLanguage() {
        var current = document.documentElement.getAttribute("lang") === "nb" ? "no" : "en";
        applyLanguage(current);

        var toggle = document.getElementById("langToggle");
        var menu = document.getElementById("langMenu");
        if (!toggle || !menu) return;

        function closeMenu() {
            menu.classList.remove("open");
            toggle.setAttribute("aria-expanded", "false");
        }

        function openMenu() {
            menu.classList.add("open");
            toggle.setAttribute("aria-expanded", "true");
        }

        toggle.addEventListener("click", function (e) {
            e.stopPropagation();
            if (menu.classList.contains("open")) closeMenu(); else openMenu();
        });

        menu.querySelectorAll(".lang-option").forEach(function (option) {
            option.addEventListener("click", function () {
                current = option.getAttribute("data-lang");
                applyLanguage(current);
                closeMenu();
                toggle.focus();
            });
        });

        document.addEventListener("click", function (e) {
            if (!menu.contains(e.target) && e.target !== toggle) closeMenu();
        });

        document.addEventListener("keydown", function (e) {
            if (e.key === "Escape") closeMenu();
        });
    }

    /* ---------------- mobile nav ---------------- */
    function initMobileNav() {
        var toggle = document.querySelector(".nav-toggle");
        var nav = document.querySelector(".site-nav");
        if (!toggle || !nav) return;

        toggle.addEventListener("click", function () {
            var isOpen = nav.classList.toggle("open");
            toggle.setAttribute("aria-expanded", String(isOpen));
        });

        nav.querySelectorAll("a").forEach(function (link) {
            link.addEventListener("click", function () {
                nav.classList.remove("open");
                toggle.setAttribute("aria-expanded", "false");
            });
        });
    }

    /* ---------------- scroll-spy ---------------- */
    function initScrollSpy() {
        var sections = document.querySelectorAll("main section[id]");
        var navLinks = document.querySelectorAll(".nav-links a[href^='#']");
        if (!sections.length || !navLinks.length || !("IntersectionObserver" in window)) return;

        var observer = new IntersectionObserver(
            function (entries) {
                entries.forEach(function (entry) {
                    if (!entry.isIntersecting) return;
                    var id = entry.target.getAttribute("id");
                    navLinks.forEach(function (link) {
                        link.classList.toggle("active", link.getAttribute("href") === "#" + id);
                    });
                });
            },
            { rootMargin: "-45% 0px -50% 0px", threshold: 0 }
        );

        sections.forEach(function (section) { observer.observe(section); });
    }

    initTheme();
    initLanguage();
    initMobileNav();
    initScrollSpy();
})();
