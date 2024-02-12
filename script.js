document.addEventListener("DOMContentLoaded", function() {
    const startButton = document.getElementById("startButton");
    const missionContainer = document.getElementById("missionContainer");
    const expBar = document.getElementById("expBar");
    const completeDayBtn = document.getElementById("completeDayBtn");

    startButton.addEventListener("click", function() {
        missionContainer.style.display = "block";
        startButton.style.display = "none"; // Esconde o botão "Começar Agora"
    });

    let level = 1;
    let exp = 0;
    const expNeeded = 100; // Quantidade de EXP necessária para subir de nível
    const levelElement = document.getElementById("level");
    const questElement = document.getElementById("quest");

    const missionsByDay = {
        1: ["Treinar 1 hora por dia", "Estudar 2 horas", "Ler por 15 minutos"],
    };

    completeDayBtn.addEventListener("click", function() {
        exp = 0; // Reseta a barra de experiência ao concluir o dia
        expBar.style.width = "0%";
        updateQuest(level);
    });

    function updateQuest(day) {
        const missions = missionsByDay[day] || [];
        if (missions.length > 0) {
            questElement.innerHTML = missions.map(mission => `<p class="mission"><input type="checkbox" onchange="updateExp(this)"> ${mission}</p>`).join('');
        } else {
            questElement.innerHTML = "<p class='mission'>Nenhuma missão disponível</p>";
        }
    }

    function updateExp(checkbox) {
        if (checkbox.checked) {
            exp += 25; // Quantidade de EXP ganha por missão concluída
            const progress = (exp / expNeeded) * 100;
            expBar.style.width = progress + "%";
            if (exp >= expNeeded) {
                exp = 0; // Reseta a barra de experiência ao subir de nível
                level++;
                levelElement.innerText = level;
                expBar.style.width = "0%";
                updateQuest(level);
            }
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


