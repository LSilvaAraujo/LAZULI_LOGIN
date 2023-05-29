let botao1 = true;
let botao2 = true;
const botao_um = document.querySelector("#botao_um");
const botao_dois = document.querySelector("#botao_dois");

botao_um.onclick = function changeColor() {
    if (pegaEstado() == true) {
            mudaCor(true);
            guardaEstado(false);

    }else {
        mudaCor(false);
        guardaEstado(true);
    }
};

function pegaEstado() {
    console.log(botao1)
    return botao1;
}

function guardaEstado(teste) {
    console.log(teste)
    botao1 = teste;
};

function mudaCor(state) {
    if (state == true) {
         botao_um.style.backgroundColor = "#071430";
    }else {
        botao_um.style.backgroundColor = "#0037A5";
    }
}