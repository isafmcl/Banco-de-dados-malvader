class UsuarioModel {
    constructor() {
        this.API_URL = 'http://127.0.0.1:5000';
    }

    async login(dadosLogin) {
        try {
            const response = await fetch(`${this.API_URL}/login`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json'
                },
                body: JSON.stringify(dadosLogin),
                mode: 'cors'
            });

            if (!response.ok) {
                throw new Error(`Erro na requisição: ${response.status}`);
            }

            return await response.json();
        } catch (error) {
            throw error;
        }
    }

    salvarDadosUsuario(usuario, tipo) {
        localStorage.setItem('usuario', JSON.stringify(usuario));
        localStorage.setItem('tipo_usuario', tipo);
    }
}

