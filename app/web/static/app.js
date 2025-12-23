const token = new URLSearchParams(window.location.search).get("token");

const api = async (path, options = {}) => {
  const headers = options.headers || {};
  headers["X-Admin-Token"] = token;
  if (options.body && !headers["Content-Type"]) {
    headers["Content-Type"] = "application/json";
  }
  const response = await fetch(path, { ...options, headers });
  if (!response.ok) {
    const text = await response.text();
    throw new Error(text || "Request failed");
  }
  return response.json();
};

const renderValue = (value) => (value === null || value === undefined || value === "" ? "—" : value);

const renderStats = (stats) => {
  const container = document.getElementById("dashboard-stats");
  container.innerHTML = "";
  const items = [
    ["Online", renderValue(stats.online)],
    ["Economy", renderValue(stats.economy_gold)],
    ["New Players", renderValue(stats.new_players)],
    ["Server Load", renderValue(stats.server_load)],
    ["Кап", renderValue(stats.level_cap)],
    [
      "Лидер",
      stats.leader_name && stats.leader_level
        ? `${stats.leader_name} (${stats.leader_level})`
        : "—",
    ],
  ];
  items.forEach(([label, value]) => {
    const div = document.createElement("div");
    div.className = "stat";
    div.innerHTML = `<strong>${label}</strong><span>${value}</span>`;
    container.appendChild(div);
  });
};

const renderTrades = (trades) => {
  const container = document.getElementById("trade-list");
  container.innerHTML = "";
  if (!trades.length) {
    container.innerHTML = "<div class='empty-state'>Подозрительных сделок нет.</div>";
    return;
  }
  trades.forEach((trade) => {
    const row = document.createElement("div");
    row.className = "row";
    row.innerHTML = `
      <div>${trade.seller} ➜ ${trade.buyer}</div>
      <div>${trade.item}</div>
      <div>${trade.price} (+${trade.deviation}%)</div>
      <div class="actions">
        <button data-action="approved" data-id="${trade.id}">✅ Одобрить</button>
        <button data-action="cancelled" data-id="${trade.id}">❌ Отменить</button>
        <button data-action="ban" data-id="${trade.id}">⛔️ Бан за RMT</button>
      </div>
    `;
    container.appendChild(row);
  });
};

const renderGuildReports = (reports) => {
  const container = document.getElementById("guild-list");
  container.innerHTML = "";
  if (!reports.length) {
    container.innerHTML = "<div class='empty-state'>Жалоб пока нет.</div>";
    return;
  }
  reports.forEach((report) => {
    const row = document.createElement("div");
    row.className = "row";
    row.innerHTML = `
      <div>${report.player}</div>
      <div>${report.reason}</div>
      <div>${report.status}</div>
      <div class="actions">
        <button data-report="resolved" data-id="${report.id}">Удалить из книги</button>
        <button data-report="banned" data-id="${report.id}">Добавить мошенника</button>
      </div>
    `;
    container.appendChild(row);
  });
};

const renderWorldState = (state) => {
  const container = document.getElementById("world-state");
  if (!state.season && !state.time_of_day && !state.weather) {
    container.innerHTML = "Данные мира пока не заполнены.";
    return;
  }
  container.innerHTML = `Текущий сезон: ${renderValue(state.season)} | Время: ${renderValue(
    state.time_of_day
  )} | Погода: ${renderValue(state.weather)}`;
  const form = document.getElementById("world-form");
  if (state.time_mode) form.time_mode.value = state.time_mode;
  if (state.time_of_day) form.time_of_day.value = state.time_of_day;
  if (state.weather) form.weather.value = state.weather;
  if (state.season) form.season.value = state.season;
};

const renderEvents = (events) => {
  const container = document.getElementById("event-list");
  container.innerHTML = "";
  if (!events.length) {
    container.innerHTML = "<div class='empty-state'>Ивенты не заданы.</div>";
    return;
  }
  events.forEach((event) => {
    const row = document.createElement("div");
    row.className = "row";
    row.innerHTML = `
      <div>${event.name}</div>
      <div>${event.status}</div>
      <button data-event="${event.id}">Запустить</button>
    `;
    container.appendChild(row);
  });
};

const renderPlayer = (player) => {
  const container = document.getElementById("player-profile");
  container.innerHTML = `
    <h3>${player.nickname} (#${player.player_id})</h3>
    <p>Уровень: <input type="number" name="level" value="${player.level}" /></p>
    <p>Золото: <input type="number" name="gold" value="${player.gold}" /></p>
    <p>Опыт: <input type="number" name="experience" value="${player.experience}" /></p>
    <div class="toggle-group">
      <label><input type="checkbox" name="is_pk" ${player.is_pk ? "checked" : ""}/> ПК</label>
      <label><input type="checkbox" name="is_vip" ${player.is_vip ? "checked" : ""}/> VIP</label>
      <label><input type="checkbox" name="in_jail" ${player.in_jail ? "checked" : ""}/> Тюрьма</label>
    </div>
    <button id="player-save" data-player="${player.player_id}">Сохранить</button>
    <h4>Инвентарь</h4>
    <ul>${
      player.inventory.length
        ? player.inventory.map((item) => `<li>${item}</li>`).join("")
        : "<li>Инвентарь пуст.</li>"
    }</ul>
  `;
};

const renderClans = (clans) => {
  const container = document.getElementById("clan-list");
  container.innerHTML = "";
  if (!clans.length) {
    container.innerHTML = "<div class='empty-state'>Кланы не найдены.</div>";
    return;
  }
  clans.forEach((clan) => {
    const row = document.createElement("div");
    row.className = "row";
    row.innerHTML = `
      <div>${clan.name}</div>
      <div>Лидер: <input type="text" value="${clan.leader}" data-clan="${clan.id}" /></div>
      <div>Казна: ${clan.treasury}</div>
      <div>Постройки: ${clan.building_level}</div>
    `;
    container.appendChild(row);
  });
};

const renderTerritories = (territories) => {
  const container = document.getElementById("territory-list");
  container.innerHTML = "";
  if (!territories.length) {
    container.innerHTML = "<div class='empty-state'>Территории не назначены.</div>";
    return;
  }
  territories.forEach((territory) => {
    const row = document.createElement("div");
    row.className = "row";
    row.textContent = `${territory.mine}: ${territory.owner}`;
    container.appendChild(row);
  });
};

const renderQuests = (quests) => {
  const container = document.getElementById("quest-list");
  container.innerHTML = "";
  if (!quests.length) {
    container.innerHTML = "<div class='empty-state'>Квесты не заданы.</div>";
    return;
  }
  quests.forEach((quest) => {
    const row = document.createElement("div");
    row.className = "row";
    row.innerHTML = `
      <div>${quest.name}</div>
      <div>${quest.status}</div>
      <button data-quest="${quest.id}">Reset Legend</button>
    `;
    container.appendChild(row);
  });
};

const renderLogs = (entries, containerId) => {
  const container = document.getElementById(containerId);
  container.innerHTML = "";
  if (!entries.length) {
    container.innerHTML = "<div class='empty-state'>Записей пока нет.</div>";
    return;
  }
  entries.forEach((entry) => {
    const row = document.createElement("div");
    row.className = "row";
    row.textContent = entry.description || `${entry.action} (${entry.created_at})`;
    container.appendChild(row);
  });
};

const loadAll = async () => {
  const [stats, trades, reports, settings, world, events, clans, territories, quests, actions, admins] =
    await Promise.all([
      api("/api/dashboard"),
      api("/api/economy/trades"),
      api("/api/economy/reports"),
      api("/api/economy/settings"),
      api("/api/world/state"),
      api("/api/world/events"),
      api("/api/clans"),
      api("/api/territories"),
      api("/api/content/quests"),
      api("/api/logs/actions"),
      api("/api/logs/admin"),
    ]);

  renderStats(stats);
  renderTrades(trades);
  renderGuildReports(reports);
  const settingsForm = document.getElementById("economy-settings");
  if (settings.auction_tax !== null && settings.auction_tax !== undefined) {
    settingsForm.auction_tax.value = settings.auction_tax;
  }
  if (settings.npc_buy_multiplier !== null && settings.npc_buy_multiplier !== undefined) {
    settingsForm.npc_buy_multiplier.value = settings.npc_buy_multiplier;
  }
  renderWorldState(world);
  renderEvents(events);
  renderClans(clans);
  renderTerritories(territories);
  renderQuests(quests);
  renderLogs(actions, "action-logs");
  renderLogs(admins, "admin-logs");
};

const setupHandlers = () => {
  document.getElementById("epoch-btn").addEventListener("click", async () => {
    const stats = await api("/api/dashboard/epoch", { method: "POST" });
    renderStats(stats);
  });

  document.getElementById("trade-list").addEventListener("click", async (event) => {
    if (event.target.tagName !== "BUTTON") return;
    const tradeId = event.target.dataset.id;
    const status = event.target.dataset.action;
    await api(`/api/economy/trades/${tradeId}`, {
      method: "POST",
      body: JSON.stringify({ status }),
    });
    loadAll();
  });

  document.getElementById("guild-list").addEventListener("click", async (event) => {
    if (event.target.tagName !== "BUTTON") return;
    const reportId = event.target.dataset.id;
    const status = event.target.dataset.report;
    await api(`/api/economy/reports/${reportId}`, {
      method: "POST",
      body: JSON.stringify({ status }),
    });
    loadAll();
  });

  document.getElementById("economy-settings").addEventListener("submit", async (event) => {
    event.preventDefault();
    const form = event.target;
    await api("/api/economy/settings", {
      method: "PUT",
      body: JSON.stringify({
        auction_tax: form.auction_tax.value,
        npc_buy_multiplier: form.npc_buy_multiplier.value,
      }),
    });
    loadAll();
  });

  document.getElementById("world-form").addEventListener("submit", async (event) => {
    event.preventDefault();
    const form = event.target;
    await api("/api/world/state", {
      method: "PUT",
      body: JSON.stringify({
        time_mode: form.time_mode.value,
        time_of_day: form.time_of_day.value,
        weather: form.weather.value,
        season: form.season.value,
      }),
    });
    loadAll();
  });

  document.getElementById("event-list").addEventListener("click", async (event) => {
    if (event.target.tagName !== "BUTTON") return;
    const eventId = event.target.dataset.event;
    await api(`/api/world/events/${eventId}/trigger`, { method: "POST" });
    loadAll();
  });

  document.getElementById("player-search").addEventListener("submit", async (event) => {
    event.preventDefault();
    const query = event.target.query.value;
    try {
      const player = await api(`/api/players/search?q=${encodeURIComponent(query)}`);
      renderPlayer(player);
    } catch (error) {
      document.getElementById("player-profile").innerHTML = `<p>${error.message}</p>`;
    }
  });

  document.getElementById("player-profile").addEventListener("click", async (event) => {
    if (event.target.id !== "player-save") return;
    const playerId = event.target.dataset.player;
    const container = document.getElementById("player-profile");
    const level = container.querySelector("input[name='level']").value;
    const gold = container.querySelector("input[name='gold']").value;
    const experience = container.querySelector("input[name='experience']").value;
    const isPk = container.querySelector("input[name='is_pk']").checked;
    const isVip = container.querySelector("input[name='is_vip']").checked;
    const inJail = container.querySelector("input[name='in_jail']").checked;
    await api(`/api/players/${playerId}`, {
      method: "PUT",
      body: JSON.stringify({
        level: Number(level),
        gold: Number(gold),
        experience: Number(experience),
        is_pk: isPk,
        is_vip: isVip,
        in_jail: inJail,
      }),
    });
  });

  document.getElementById("clans").addEventListener("change", async (event) => {
    if (!event.target.dataset.clan) return;
    const clanId = event.target.dataset.clan;
    await api(`/api/clans/${clanId}/leader`, {
      method: "PUT",
      body: JSON.stringify({ leader: event.target.value }),
    });
  });

  document.getElementById("reset-territories").addEventListener("click", async () => {
    await api("/api/territories/reset", { method: "POST" });
    loadAll();
  });

  document.getElementById("quest-list").addEventListener("click", async (event) => {
    if (event.target.tagName !== "BUTTON") return;
    const questId = event.target.dataset.quest;
    await api(`/api/content/quests/${questId}/reset`, { method: "POST" });
    loadAll();
  });

  document.getElementById("spawn-item").addEventListener("submit", async (event) => {
    event.preventDefault();
    const form = event.target;
    await api("/api/content/spawn", {
      method: "POST",
      body: JSON.stringify({
        player_id: Number(form.player_id.value),
        item: form.item.value,
      }),
    });
    form.reset();
  });
};

loadAll()
  .then(setupHandlers)
  .catch((error) => {
    const banner = document.getElementById("error-banner");
    banner.hidden = false;
    banner.textContent = `Ошибка загрузки данных: ${error.message}`;
  });
