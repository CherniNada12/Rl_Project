let trainingInterval = null;

async function loadGrid(){
    const res = await fetch("/grid");
    const data = await res.json();
    const gridDiv = document.getElementById("grid");
    gridDiv.innerHTML = "";
    const grid = data.grid;
    const agent = data.agent;
    for(let y=0;y<grid.length;y++){
        for(let x=0;x<grid[y].length;x++){
            const cell = document.createElement("div");
            cell.className="cell";
            if(x===agent.x && y===agent.y) cell.innerText="🤖";
            else if(grid[y][x]===1) cell.innerText="🧱";
            else if(grid[y][x]===2) cell.innerText="⚠️";
            else if(grid[y][x]===3) cell.innerText="💎";
            else if(grid[y][x]===4) cell.innerText="🏁";
            gridDiv.appendChild(cell);
        }
    }
}

async function trainStep(){
    await fetch("/train",{method:"POST", headers:{"Content-Type":"application/json"}, body:JSON.stringify({algorithm:"qlearning"})});
    loadGrid();
}

async function resetGrid(){
    await fetch("/reset",{method:"POST"});
    loadGrid();
}

document.getElementById("startBtn").addEventListener("click", ()=>{
    if(trainingInterval) return;
    trainingInterval = setInterval(trainStep, 200);
    document.getElementById("startBtn").style.display="none";
    document.getElementById("stopBtn").style.display="block";
});

document.getElementById("stopBtn").addEventListener("click", ()=>{
    clearInterval(trainingInterval);
    trainingInterval = null;
    document.getElementById("startBtn").style.display="block";
    document.getElementById("stopBtn").style.display="none";
});

document.getElementById("resetBtn").addEventListener("click", ()=>{
    clearInterval(trainingInterval);
    trainingInterval = null;
    document.getElementById("startBtn").style.display="block";
    document.getElementById("stopBtn").style.display="none";
    resetGrid();
});

window.onload = loadGrid;
