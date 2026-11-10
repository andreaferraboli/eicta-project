// DOM manipulation only (no server): countdown, genre filter, mobile menu.

const FESTIVAL_START = new Date("2027-05-07T16:00:00+02:00");

function updateCountdown() {
  const diff = FESTIVAL_START - new Date();
  if (diff <= 0) {
    document.querySelector(".countdown").textContent = "The festival has started: see you there!";
    return;
  }
  const minutes = Math.floor(diff / 60000);
  document.getElementById("cd-days").textContent = Math.floor(minutes / 1440);
  document.getElementById("cd-hours").textContent = Math.floor((minutes % 1440) / 60);
  document.getElementById("cd-minutes").textContent = minutes % 60;
}
updateCountdown();
setInterval(updateCountdown, 30000);

document.querySelectorAll(".chip").forEach((chip) => {
  chip.addEventListener("click", () => {
    document.querySelectorAll(".chip").forEach((c) => c.classList.toggle("is-active", c === chip));
    const genre = chip.dataset.genre;
    document.querySelectorAll(".act").forEach((act) => {
      act.hidden = genre !== "all" && act.dataset.genre !== genre;
    });
  });
});

const toggle = document.querySelector(".nav-toggle");
const nav = document.getElementById("site-nav");
toggle.addEventListener("click", () => {
  const open = nav.classList.toggle("is-open");
  toggle.setAttribute("aria-expanded", String(open));
});
nav.querySelectorAll("a").forEach((a) => a.addEventListener("click", () => {
  nav.classList.remove("is-open");
  toggle.setAttribute("aria-expanded", "false");
}));
