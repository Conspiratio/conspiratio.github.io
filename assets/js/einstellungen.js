// Thema und Schriftart umschalten. Die Seite funktioniert ohne diese Datei
// vollstaendig - dann gilt die Systemeinstellung und die Standardschrift.
//
// Das sichtbare Symbol der Schalter wechselt ueber CSS, nicht hier: Die Knoepfe
// enthalten beide SVG, und das Stylesheet zeigt je nach wirksamem Thema die
// passende. Dieses Skript setzt nur Attribute - wuerde es textContent setzen,
// waere die SVG weg.
(function () {
  "use strict";

  var wurzel = document.documentElement;

  function merke(schluessel, wert) {
    try {
      if (wert === null) { localStorage.removeItem(schluessel); }
      else { localStorage.setItem(schluessel, wert); }
    } catch (e) { /* privates Fenster oder gesperrter Speicher: dann nur diese Seite */ }
  }

  function beschrifte(knopf, gedrueckt, beschriftung) {
    knopf.setAttribute("aria-pressed", gedrueckt ? "true" : "false");
    knopf.setAttribute("aria-label", beschriftung);
    knopf.setAttribute("title", beschriftung);
  }

  // --- Thema -------------------------------------------------------------
  // Ohne eigene Wahl gilt die Systemeinstellung. Der Knopf muss deshalb das
  // *wirksame* Thema kennen und nicht nur das gesetzte Attribut, sonst bietet
  // er auf einem dunkel eingestellten System "dunkel" an.
  var themenKnopf = document.getElementById("schalter-thema");
  if (themenKnopf) {
    var dunkelBevorzugt = window.matchMedia("(prefers-color-scheme: dark)");

    var wirksamesThema = function () {
      return wurzel.getAttribute("data-thema") || (dunkelBevorzugt.matches ? "dunkel" : "hell");
    };

    var zeigeThema = function () {
      var dunkel = wirksamesThema() === "dunkel";
      beschrifte(themenKnopf, dunkel,
                 dunkel ? "Helles Pergament einschalten" : "Dunkles Kontor einschalten");
    };

    themenKnopf.addEventListener("click", function () {
      var neu = wirksamesThema() === "dunkel" ? "hell" : "dunkel";
      wurzel.setAttribute("data-thema", neu);
      merke("conspiratio-thema", neu);
      zeigeThema();
    });

    // Aendert der Besucher die Systemeinstellung, waehrend die Seite offen ist,
    // folgt die Beschriftung - aber nur, solange er nicht selbst gewaehlt hat.
    dunkelBevorzugt.addEventListener("change", zeigeThema);

    zeigeThema();
  }

  // --- Schriftart --------------------------------------------------------
  // Hier gibt es keine Systemvorgabe, also genuegt an/aus.
  var schriftKnopf = document.getElementById("schalter-schrift");
  if (schriftKnopf) {
    var zeigeSchrift = function () {
      var lesbar = wurzel.getAttribute("data-schrift") === "lesbar";
      beschrifte(schriftKnopf, lesbar,
                 lesbar ? "Zierschrift einschalten" : "Gut lesbare Schrift einschalten");
    };

    schriftKnopf.addEventListener("click", function () {
      if (wurzel.getAttribute("data-schrift") === "lesbar") {
        wurzel.removeAttribute("data-schrift");
        merke("conspiratio-schrift", null);
      } else {
        wurzel.setAttribute("data-schrift", "lesbar");
        merke("conspiratio-schrift", "lesbar");
      }
      zeigeSchrift();
    });

    zeigeSchrift();
  }
})();
