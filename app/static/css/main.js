// Scripts do NinaOrganiza

console.log('NinaOrganiza carregado com sucesso!');

// Função para máscaras de telefone
function maskPhone(input) {
    let value = input.value.replace(/\D/g, '');
    if (value.length > 11) value = value.substring(0, 11);
    
    if (value.length > 6) {
        value = '(' + value.substring(0, 2) + ') ' + value.substring(2, 7) + '-' + value.substring(7);
    } else if (value.length > 2) {
        value = '(' + value.substring(0, 2) + ') ' + value.substring(2);
    } else if (value.length > 0) {
        value = '(' + value;
    }
    
    input.value = value;
}

// Função para máscaras de CEP
function maskCep(input) {
    let value = input.value.replace(/\D/g, '');
    if (value.length > 8) value = value.substring(0, 8);
    
    if (value.length > 5) {
        value = value.substring(0, 5) + '-' + value.substring(5);
    }
    
    input.value = value;
}

// Função para buscar CEP (simulação)
function buscarCep(cep) {
    const cepLimpo = cep.replace(/\D/g, '');
    if (cepLimpo.length === 8) {
        // Simulação de busca de CEP
        setTimeout(() => {
            document.getElementById('rua').value = 'Avenida Paulista';
            document.getElementById('bairro').value = 'Bela Vista';
            document.getElementById('cidade').value = 'São Paulo - SP';
        }, 600);
    }
}

// Inicialização
document.addEventListener('DOMContentLoaded', function() {
    // Aplicar máscaras em campos de telefone
    const phoneInputs = document.querySelectorAll('input[type="tel"]');
    phoneInputs.forEach(input => {
        input.addEventListener('input', function() {
            maskPhone(this);
        });
    });
    
    // Aplicar máscaras em campos de CEP
    const cepInputs = document.querySelectorAll('input[name="cep"]');
    cepInputs.forEach(input => {
        input.addEventListener('input', function() {
            maskCep(this);
            buscarCep(this.value);
        });
    });
    
    console.log('Event listeners inicializados');
});