let level = 0;
let experience = 0;
let physical = 0;
let intelligence = 0;
let music = 0;

const expNeededPerLevel = 100;

function completeQuest(quest) {
    switch (quest) {
        case "Estudar 2 horas":
            experience += 50;
            intelligence += 1;
            break;
        case "Treinar 1 hora":
            experience += 30;
            physical += 1;
            break;
        case "Ler por 15 minutos":
            experience += 20;
            intelligence += 1;
            break;
        case "Tocar o instrumento":
            experience += 40;
            music += 1;
            break;
        default:
            break;
    }
    updateStats();
}

function updateStats() {
    document.getElementById('level').innerText = level;
    document.getElementById('experience').innerText = experience;
    document.getElementById('physical').innerText = physical;
    document.getElementById('intelligence').innerText = intelligence;
    document.getElementById('music').innerText = music;
    const expNeeded = expNeededPerLevel - (experience % expNeededPerLevel);
    document.getElementById('exp-needed').innerText = expNeeded;

    const totalQuests = 4; // Número total de quests diárias
    const completedQuests = physical > 0 + intelligence > 0 + music > 0 ? 1 : 0; // Conta quests completadas
    const dailyProgress = Math.round((completedQuests / totalQuests) * 100); // Calcula progresso diário
    document.getElementById('daily-progress').innerText = dailyProgress;
}

function saveDailyReflection() {
    const dailyReflectionText = document.getElementById('daily-reflection-text').value;
    // Salvar a anotação em algum lugar (por exemplo, armazenamento local ou banco de dados)
    console.log("Anotação do dia salva:", dailyReflectionText);

    // Resetar o campo de texto após salvar
    document.getElementById('daily-reflection-text').value = "";
}

function showPreviousReflections() {
    // Recuperar anotações anteriores (do armazenamento local ou banco de dados) e exibir para o usuário
    console.log("Anotações anteriores:");
    // Exibir anotações anteriores em algum lugar na interface do usuário
}

updateStats(); // Atualizar estatísticas iniciais ao carregar a página

    });
    calendar.render();
});


