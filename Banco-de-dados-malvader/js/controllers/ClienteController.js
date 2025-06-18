class ClienteController {
    constructor(model, view) {
        this.model = model;
        this.view = view;
        this.initialize();
    }

    async initialize() {
        try {
            // Verifica apenas se o usuário está logado
            if (!this.model.usuario.id) {
                window.location.href = '../templates/Login.html';
                return;
            }

            // Carrega dados iniciais
            const [dadosConta, transacoes] = await Promise.all([
                this.model.obterDadosConta(),
                this.model.obterTransacoes()
            ]);

            this.view.atualizarDadosConta(dadosConta);
            this.view.atualizarTransacoes(transacoes);
            this.view.bindLogout(this.handleLogout.bind(this));
        } catch (error) {
            this.view.mostrarErro('Erro ao carregar dados do painel');
            console.error(error);
        }
    }

    handleLogout() {
        this.model.logout();
        window.location.href = 'Login.html';
    }
}
