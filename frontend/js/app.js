let allMatches = [];
let autoRefreshInterval = null;
const AUTO_REFRESH_INTERVAL = 1000;
let currentTeamFilter = "";

async function loadMatch() {
    try {
        const res = await fetch("/api/matches");

        if (res.status !== 200) {
            console.error("Errore nel caricamento delle partite:", res.status);
            const errorText = await res.text();
            console.error("Dettagli errore:", errorText);
            return;
        }

        const data = await res.json();
        console.log("Dati ricevuti:", data);
        const newMatches = data.items || [];
        const list = document.getElementById("matchList");
        const emptyMessage = document.getElementById("emptyMessage");

        if (newMatches.length === 0) {
            list.innerHTML = "";
            emptyMessage.style.display = "block";
            console.log("Nessun match trovato");
            return;
        }

        emptyMessage.style.display = "none";

        // Salva il filtro corrente
        const filter = document.getElementById("teamFilter");
        currentTeamFilter = filter.value;

        // Aggiorna solo i match modificati/nuovi
        const newMatchIds = new Set(newMatches.map(m => m.id));
        const oldMatchIds = new Set(allMatches.map(m => m.id));

        // Rimuovi match eliminati
        allMatches.forEach(match => {
            if (!newMatchIds.has(match.id)) {
                const element = document.getElementById("match-" + match.id);
                if (element) element.remove();
            }
        });

        // Aggiorna o aggiungi match
        newMatches.forEach(match => {
            const existingItem = document.getElementById("match-" + match.id);
            if (existingItem) {
                updateMatchElement(existingItem, match);
            } else {
                // Nuovo match
                addMatchToList(match);
            }
        });

        allMatches = newMatches;
        renderLeagueTable();

        // Aggiorna il filtro squadre (mantieni il valore corrente)
        populateTeamFilter();
        
        // Ripristina il filtro
        filter.value = currentTeamFilter;
        filterByTeam();
    } catch (error) {
        console.error("Errore nel caricamento:", error);
    }
}

function parseScore(scoreData, teamName) {
    let currentScore = 0;
    let events = [];

    if (Array.isArray(scoreData)) {
        scoreData.forEach(item => {
            if (typeof item === 'object') {
                const key = Object.keys(item)[0];
                const time = item[key];
                const score = parseInt(key);
                if (score > currentScore) {
                    events.push({
                        type: 'goal',
                        team: teamName,
                        time: time,
                        details: `Gol ${teamName} (${score})`
                    });
                    currentScore = score;
                }
            } else if (typeof item === 'number') {
                currentScore = item;
            }
        });
    } else {
        currentScore = scoreData;
    }
    return { value: currentScore, events: events };
}

function getMatchEvents(match) {
    const s1 = parseScore(match.scoreT1, match.team1_name);
    const s2 = parseScore(match.scoreT2, match.team2_name);
    
    let events = [...s1.events, ...s2.events];
    
    if (match.breaks && Array.isArray(match.breaks)) {
        match.breaks.forEach(b => {
            const type = Object.keys(b)[0];
            const time = b[type];
            let details = type;
            if (type === 'fallo') details = 'Fallo';
            if (type === 'pausa') details = 'Pausa';
            
            events.push({
                type: type,
                time: time,
                details: details
            });
        });
    }
    
    return events.sort((a, b) => a.time - b.time);
}

function updateMatchElement(element, match) {
    const s1 = parseScore(match.scoreT1, match.team1_name);
    const s2 = parseScore(match.scoreT2, match.team2_name);
    
    const details = element.querySelector(".match-details");
    if (details) {
        details.innerHTML = `<strong>Score:</strong> ${s1.value} - ${s2.value} | 
                            <strong>Tempo:</strong> ${match.time}' | 
                            <strong>Campionato:</strong> ${match.championship}`;
    }
    
    // Update events
    let eventsContainer = element.querySelector(".match-events");
    if (!eventsContainer) {
        eventsContainer = document.createElement("div");
        eventsContainer.className = "match-events";
        element.querySelector(".match-info").appendChild(eventsContainer);
    }
    
    const events = getMatchEvents(match);
    if (events.length > 0) {
        eventsContainer.innerHTML = events.map(e => `
            <div class="event-item">
                <span class="event-time">${e.time}'</span>
                <span class="event-desc">
                    ${e.type === 'goal' ? '<i class="fa-solid fa-futbol"></i>' : ''}
                    ${e.type === 'fallo' ? '<i class="fa-solid fa-circle-exclamation" style="color:orange"></i>' : ''}
                    ${e.type === 'pausa' ? '<i class="fa-solid fa-pause"></i>' : ''}
                    ${e.details}
                </span>
            </div>
        `).join("");
        eventsContainer.style.display = "block";
    } else {
        eventsContainer.style.display = "none";
    }
    
    element.className = "match-item " + (match.done ? "done" : "");
    
    // Update button state
    const toggleBtn = element.querySelector(".icon-btn:not(.delete)");
    if (toggleBtn) {
        toggleBtn.innerHTML = '<i class="fa-solid fa-circle-info" title="Dettagli partita"></i>';
        toggleBtn.onclick = () => {
            window.location.href = `match_page.html?id=${match.id}`;
    };
}


    }

function addMatchToList(match) {
    const list = document.getElementById("matchList");
    const emptyMessage = document.getElementById("emptyMessage");
    
    // Controlla se il match esiste già e aggiornalo
    const existingItem = document.getElementById("match-" + match.id);
    if (existingItem) {
        existingItem.remove();
    } else {
        // Se è un nuovo match, aggiungilo a allMatches
        allMatches.push(match);
        emptyMessage.style.display = "none";
    }
    
    const li = document.createElement("li");
    li.className = "match-item " + (match.done ? "done" : "");
    li.id = "match-" + match.id;

    // Info partita
    const info = document.createElement("div");
    info.className = "match-info";

    const title = document.createElement("div");
    title.className = "match-title";
    title.textContent = `${match.team1_name} vs ${match.team2_name}`;

    const details = document.createElement("div");
    details.className = "match-details";
    
    info.appendChild(title);
    info.appendChild(details);

    // Azioni
    const actions = document.createElement("div");
    actions.className = "match-actions";

    // Bottone toggle done/active
    const moreinfo = document.createElement("button");
    moreinfo.className = "icon-btn";
    actions.appendChild(moreinfo);

    li.appendChild(info);
    li.appendChild(actions);
    list.appendChild(li);
    
    // Use updateMatchElement to populate details and events
    updateMatchElement(li, match);
}

function populateTeamFilter() {
    const filter = document.getElementById("teamFilter");
    const teams = new Set();
    
    allMatches.forEach(match => {
        teams.add(match.team1_name);
        teams.add(match.team2_name);
    });

    // Mantieni l'opzione "Tutte"
    const currentValue = filter.value;
    filter.innerHTML = '<option value="">Tutte le squadre</option>';
    
    Array.from(teams).sort().forEach(team => {
        const option = document.createElement("option");
        option.value = team;
        option.textContent = team;
        filter.appendChild(option);
    });

    filter.value = currentValue;
}

function filterByTeam() {
    const filter = document.getElementById("teamFilter").value;
    currentTeamFilter = filter; // Salva il filtro corrente
    const items = document.querySelectorAll(".match-item");

    items.forEach(item => {
        const title = item.querySelector(".match-title").textContent;
        if (filter === "" || title.includes(filter)) {
            item.style.display = "flex";
        } else {
            item.style.display = "none";
        }
    });
}

function startAutoRefresh() {
    if (autoRefreshInterval) {
        clearInterval(autoRefreshInterval);
    }
    
    autoRefreshInterval = setInterval(() => {
        loadMatch();
    }, AUTO_REFRESH_INTERVAL);
    
    console.log("Auto-refresh abilitato ogni " + AUTO_REFRESH_INTERVAL + "ms");
}

function buildLeagueTable(matches) {
    const table = {};
    matches.forEach(match => {
        const s1 = parseScore(match.scoreT1, match.team1_name).value;
        const s2 = parseScore(match.scoreT2, match.team2_name).value;

        if (!table[match.team1_name]) table[match.team1_name] = { team: match.team1_name, pt: 0, gf: 0, gs: 0 };
        if (!table[match.team2_name]) table[match.team2_name] = { team: match.team2_name, pt: 0, gf: 0, gs: 0 };

        table[match.team1_name].gf += s1;
        table[match.team1_name].gs += s2;
        table[match.team2_name].gf += s2;
        table[match.team2_name].gs += s1;

        if (match.done) {
            if (s1 > s2) table[match.team1_name].pt += 3;
            else if (s2 > s1) table[match.team2_name].pt += 3;
            else { table[match.team1_name].pt += 1; table[match.team2_name].pt += 1; }
        }
    });

    return Object.values(table).sort((a,b) => b.pt - a.pt || (b.gf-b.gs) - (a.gf-a.gs) || b.gf - a.gf);
}

function renderLeagueTable() {
    const body = document.getElementById("leagueBody");
    if (!body) return;
    const standings = buildLeagueTable(allMatches);
    body.innerHTML = "";
    standings.forEach((t, index) => {
        body.innerHTML += `
            <tr>
                <td>${index+1}</td>
                <td style="text-align:left; padding-left:10px;"><strong>${t.team}</strong></td>
                <td>${t.pt}</td>
                <td>${t.gf}</td>
                <td>${t.gs}</td>
                <td>${t.gf - t.gs}</td>
            </tr>
        `;
    });
}


if (location.pathname.endsWith("main_page.html") || location.pathname === "/")
    loadMatch();
