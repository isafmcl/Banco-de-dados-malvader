class ClienteView {
    constructor() {
        this.nomeUsuarioEl = document.getElementById('nomeUsuario');
        this.saldoEl = document.getElementById('saldo');
        this.transacoesEl = document.getElementById('transacoes');
        this.logoutBtn = document.getElementById('logoutBtn');
    }

    atualizarDadosConta(dados) {
        if (this.nomeUsuarioEl) {
            this.nomeUsuarioEl.textContent = dados.nome;
        }
        if (this.saldoEl) {
            this.saldoEl.textContent = new Intl.NumberFormat('pt-BR', {
                style: 'currency',
                currency: 'BRL'
            }).format(dados.saldo);
        }
    }

    atualizarTransacoes(transacoes) {
        if (!this.transacoesEl) return;

        this.transacoesEl.innerHTML = transacoes.map(transacao => `
            <div class="p-4 border-b">
                <div class="flex justify-between">
                    <span class="font-medium">${transacao.tipo}</span>
                    <span class="${transacao.tipo === 'entrada' ? 'text-green-600' : 'text-red-600'}">
                        ${new Intl.NumberFormat('pt-BR', {
                            style: 'currency',
                            currency: 'BRL'
                        }).format(transacao.valor)}
                    </span>
                </div>
                <div class="text-sm text-gray-600">${new Date(transacao.data).toLocaleDateString('pt-BR')}</div>
            </div>
        `).join('');
    }

    bindLogout(handler) {
        if (this.logoutBtn) {
            this.logoutBtn.onclick = () => handler();
        }
    }

    mostrarErro(mensagem) {
        alert(mensagem);
    }
}
