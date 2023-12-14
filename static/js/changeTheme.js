var root = document.querySelector(":root");
var changeTheme = document.querySelector(".changeTheme");

var theme;

if (localStorage.getItem(theme) === "dark") {
  toDark();
} else if (localStorage.getItem(theme) === "light") {
  toLight();
}

function toLight() {
  localStorage.setItem(theme, "light");
  root.style.setProperty("--themePrimary", "#fff");
  root.style.setProperty("--themeSecondary", "#064E3B");
  root.style.setProperty("--themeHelper", "#F3F4F6");
  changeTheme.innerHTML = "🌞";
  changeTheme.setAttribute("onclick", "javascript: toDark();");
}

function toDark() {
  localStorage.setItem(theme, "dark");
  root.style.setProperty("--themePrimary", "#fff");
  root.style.setProperty("--themeSecondary", "#000");
  root.style.setProperty("--themeHelper", "#C6C6C6");
  changeTheme.innerHTML = "🌚";
  changeTheme.setAttribute("onclick", "javascript: toLight();");
}
