class LoginController {
    constructor(model, view) {
        this.model = model;
        this.view = view;
        this.initialize();
    }
   //inicializa
    initialize() {
        this.view.bindToggleTipo(this.handleToggleTipo.bind(this));
        this.view.bindLoginSubmit(this.handleLogin.bind(this));
    }

    handleToggleTipo(tipo) {
        this.view.atualizarInterface(tipo);
    }

    async handleLogin(dadosLogin) {
        try {
            const data = await this.model.login(dadosLogin);
            
            if (data.success) {
                this.model.salvarDadosUsuario(data.usuario, data.tipo);                window.location.href = data.tipo === 'cliente' 
                    ? '../templates/painel_cliente.html' 
                    : '../templates/painel_funcionario.html';
            } else {
                this.view.mostrarErro(data.message || 'Usuário não encontrado.');
            }
        } catch (error) {
            const mensagem = error.message.includes('fetch')
                ? 'Erro de conexão: Verifique se o servidor está rodando.'
                : `Erro ao conectar com o servidor: ${error.message}`;
            this.view.mostrarErro(mensagem);
        }
    }
}
