class ClienteModel {
    constructor() {
        this.API_URL = 'http://127.0.0.1:5000';
        this.usuario = JSON.parse(localStorage.getItem('usuario') || '{}');
        this.tipo = localStorage.getItem('tipo_usuario');
    }

    async obterDadosConta() {
        try {
            const response = await fetch(`${this.API_URL}/conta/${this.usuario.id}`, {
                method: 'GET',
                headers: {
                    'Accept': 'application/json'
                }
            });

            if (!response.ok) {
                throw new Error(`Erro na requisição: ${response.status}`);
            }

            return await response.json();
        } catch (error) {
            throw error;
        }
    }

    async obterTransacoes() {
        try {
            const response = await fetch(`${this.API_URL}/transacoes/${this.usuario.id}`, {
                method: 'GET',
                headers: {
                    'Accept': 'application/json'
                }
            });

            if (!response.ok) {
                throw new Error(`Erro na requisição: ${response.status}`);
            }

            return await response.json();
        } catch (error) {
            throw error;
        }
    }

    logout() {
        localStorage.removeItem('usuario');
        localStorage.removeItem('tipo_usuario');
    }
}
