document.addEventListener("DOMContentLoaded", function() {
    let level = 1;
    const levelElement = document.getElementById("level");
    const questElement = document.querySelector(".quest");

    document.getElementById("increaseBtn").addEventListener("click", function() {
        level++;
        levelElement.innerText = level;
        updateQuest(level);
    });

    function updateQuest(level) {
        switch (level) {
            case 2:
                questElement.innerText = "Missão: Treinar por 1 hora";
                break;
            case 3:
                questElement.innerText = "Missão: Ler por 15 minutos";
                break;
            // Adicione mais missões para níveis mais altos, se necessário
            default:
                questElement.innerText = "Nenhuma missão disponível";
                break;
        }
    }
});
