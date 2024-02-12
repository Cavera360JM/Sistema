document.addEventListener("DOMContentLoaded", function() {
    const startButton = document.getElementById("startButton");
    const missionContainer = document.getElementById("missionContainer");

    startButton.addEventListener("click", function() {
        missionContainer.style.display = "block";
    });

    let level = 1;
    const levelElement = document.getElementById("level");
    const questElement = document.getElementById("quest");

    const missionsByDay = {
        1: ["Treinar 1 hora por dia", "Estudar 2 horas", "Ler por 15 minutos"],
    };

    document.getElementById("increaseBtn").addEventListener("click", function() {
        level++;
        levelElement.innerText = level;
        updateQuest(level);
    });

    function updateQuest(day) {
        const missions = missionsByDay[day] || [];
        if (missions.length > 0) {
            questElement.innerHTML = missions.map(mission => `<p class="mission"><input type="checkbox"> ${mission}</p>`).join('');
        } else {
            questElement.innerHTML = "<p class='mission'>Nenhuma missão disponível</p>";
        }
    }

    const calendarEl = document.getElementById('calendar');
    const calendar = new FullCalendar.Calendar(calendarEl, {
        selectable: true,
        dateClick: function(info) {
            const day = info.date.getDate();
            level = day;
            levelElement.innerText = level;
            updateQuest(day);
        }
    });
    calendar.render();
});

