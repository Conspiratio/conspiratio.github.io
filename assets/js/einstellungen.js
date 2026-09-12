// Thema und Schriftart umschalten. Die Seite funktioniert ohne diese Datei
// vollstaendig - dann gilt die Systemeinstellung und die Standardschrift.
(function () {
  "use strict";

  var wurzel = document.documentElement;

  function merke(schluessel, wert) {
    try {
      if (wert === null) { localStorage.removeItem(schluessel); }
      else { localStorage.setItem(schluessel, wert); }
    } catch (e) { /* privates Fenster oder gesperrter Speicher: dann eben nur diese Seite */ }
  }

  // --- Thema -------------------------------------------------------------
  // Ohne eigene Wahl gilt die Systemeinstellung. Der Knopf muss deshalb das
  // *wirksame* Thema kennen und nicht nur das gesetzte Attribut, sonst bietet
  // er auf einem dunkel eingestellten System "dunkel" an.
  var themenKnopf = document.getElementById("schalter-thema");
  if (themenKnopf) {
    var dunkelBevorzugt = window.matchMedia("(prefers-color-scheme: dark)");

    function wirksamesThema() {
      return wurzel.getAttribute("data-thema") || (dunkelBevorzugt.matches ? "dunkel" : "hell");
    }

    function zeigeThema() {
      var dunkel = wirksamesThema() === "dunkel";
      themenKnopf.setAttribute("aria-pressed", dunkel ? "true" : "false");
      themenKnopf.textContent = dunkel ? "Helles Pergament" : "Dunkles Kontor";
    }

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
    function zeigeSchrift() {
      var lesbar = wurzel.getAttribute("data-schrift") === "lesbar";
      schriftKnopf.setAttribute("aria-pressed", lesbar ? "true" : "false");
      schriftKnopf.textContent = lesbar ? "Zierschrift" : "Gut lesbar";
    }

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
