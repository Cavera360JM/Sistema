document.addEventListener("DOMContentLoaded", function() {
    let level = 1;
    const levelElement = document.getElementById("level");
    const questElement = document.getElementById("quest");
    
    // Estrutura de dados para armazenar as missões por dia
    const missionsByDay = {
        1: ["Estudar 2 horas", "Treinar 1 hora", "Ler por 15 minutos"],
        // Adicione mais missões para outros dias conforme necessário
    };

    document.getElementById("increaseBtn").addEventListener("click", function() {
        level++;
        levelElement.innerText = level;
        updateQuest(level);
    });

    function updateQuest(day) {
        const missions = missionsByDay[day] || [];
        if (missions.length > 0) {
            questElement.innerHTML = missions.map(mission => `<p class="mission">${mission}</p>`).join('');
        } else {
            questElement.innerHTML = "<p class='mission'>Nenhuma missão disponível</p>";
        }
    }

    // Inicializar o FullCalendar
    const calendarEl = document.getElementById('calendar');
    const calendar = new FullCalendar.Calendar(calendarEl, {
        selectable: true,
        dateClick: function(info) {
            // Atualizar a quest com base no dia selecionado
            const day = info.date.getDate();
            level = day;
            levelElement.innerText = level;
            updateQuest(day);
        }
    });
    calendar.render();
});

