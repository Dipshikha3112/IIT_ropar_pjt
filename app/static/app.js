async function loadContext() {
    const res = await fetch("/context");
    const data = await res.json();

    document.getElementById("emotion").innerText = "Emotion: " + data.emotion;
    document.getElementById("time").innerText = "Time: " + data.time;
    document.getElementById("location").innerText = "Location: " + data.location;
}

async function search(domain) {
    const q = document.getElementById("search").value;
    const res = await fetch(`/recommend?query=${q}&domain=${domain}`);
    const data = await res.json();

    const box = document.getElementById("search-results");
    box.innerHTML = "";

    data.results.forEach(item => {
        const div = document.createElement("div");
        div.className = "card";
        div.innerHTML = `<h3>${item.title}</h3><p>Score: ${item.score || ""}</p>`;
        box.appendChild(div);
    });
}

async function loadRandom() {
    const movies = await fetch("/random?domain=movies").then(r => r.json());
    const news = await fetch("/random?domain=news").then(r => r.json());

    const mbox = document.getElementById("random-movies");
    const nbox = document.getElementById("random-news");

    mbox.innerHTML = "";
    nbox.innerHTML = "";

    movies.forEach(item => {
        const div = document.createElement("div");
        div.className = "card";
        div.innerHTML = `<h3>${item.title}</h3>`;
        mbox.appendChild(div);
    });

    news.forEach(item => {
        const div = document.createElement("div");
        div.className = "card";
        div.innerHTML = `<h3>${item.title}</h3><p>${item.source}</p>`;
        nbox.appendChild(div);
    });
}

setInterval(loadContext, 3000);
setInterval(loadRandom, 15000);

loadContext();
loadRandom();
