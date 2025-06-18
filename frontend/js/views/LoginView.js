class LoginView {
    constructor() {
        this.tipoUsuarioEl = document.getElementById('tipoUsuario');
        this.otpContainerEl = document.getElementById('otpContainer');
        this.clienteBtnEl = document.getElementById('clienteBtn');
        this.funcionarioBtnEl = document.getElementById('funcionarioBtn');
        this.loginForm = document.getElementById('loginForm');
    }

    bindToggleTipo(handler) {
        this.clienteBtnEl.onclick = () => handler('cliente');
        this.funcionarioBtnEl.onclick = () => handler('funcionario');
    }

    bindLoginSubmit(handler) {
        this.loginForm.onsubmit = async (event) => {
            event.preventDefault();
            
            const dadosLogin = {
                cpf: document.getElementById('cpf').value,
                senha: document.getElementById('senha').value,
                tipo_usuario: this.tipoUsuarioEl.value
            };

            if (dadosLogin.tipo_usuario === 'funcionario') {
                dadosLogin.otp = document.getElementById('otp').value;
            }

            await handler(dadosLogin);
        };
    }

    atualizarInterface(tipo) {
        const isCliente = tipo === 'cliente';
        this.tipoUsuarioEl.value = tipo;
        
        // Atualiza visual dos botões
        this.clienteBtnEl.classList.toggle('bg-blue-600', isCliente);
        this.clienteBtnEl.classList.toggle('bg-gray-600', !isCliente);
        this.funcionarioBtnEl.classList.toggle('bg-blue-600', !isCliente);
        this.funcionarioBtnEl.classList.toggle('bg-gray-600', isCliente);
        
        // Mostra/esconde campo OTP
        this.otpContainerEl.classList.toggle('hidden', isCliente);
    }

    mostrarErro(mensagem) {
        alert(mensagem);
    }
}
