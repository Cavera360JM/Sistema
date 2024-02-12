document.addEventListener("DOMContentLoaded", function() {
    let level = 1;
    const levelElement = document.getElementById("level");

    document.getElementById("increaseBtn").addEventListener("click", function() {
        level++;
        levelElement.innerText = level;
    });
});
