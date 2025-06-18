from flask import Flask, request, jsonify
from flask_cors import CORS
from src.services.auth_service import get_auth_service
from src.services.financial_service import get_financial_service
from src.services.account_service import get_account_service
from src.utils.statistics import get_statistics_service

app = Flask(__name__)
CORS(app, origins=['http://127.0.0.1:5504', 'http://localhost:5504', 'http://127.0.0.1:5000', 'http://localhost:5000', '*'])

def error_response(message, status=500):
    """Retorna uma resposta de erro padronizada"""
    return jsonify({'success': False, 'message': message}), status

@app.route('/login', methods=['POST'])
def login():
    try:
        dados = request.json
        auth_service = get_auth_service()
        tipo_usuario = dados.get('tipo_usuario', 'cliente')
        
        # Autentica cliente ou funcionário
        if tipo_usuario == 'cliente':
            resultado = auth_service.autenticar_cliente(dados['cpf'], dados['senha'])
        else:
            if 'otp' not in dados:
                return error_response('Código OTP é obrigatório para funcionários', 400)
            resultado = auth_service.autenticar_funcionario(dados['cpf'], dados['senha'], dados['otp'])
        
        if not resultado:
            return error_response('Usuário não encontrado ou credenciais inválidas', 401)
        
        return jsonify({
            'success': True,
            'usuario': resultado,
            'tipo': tipo_usuario
        })
        
    except Exception as e:
        return error_response(f'Erro durante o login: {str(e)}')

@app.route('/saldo/<cpf>', methods=['GET'])
def get_saldo(cpf):
    try:
        saldo = get_financial_service().consultar_saldo(cpf)
        return jsonify({'saldo': saldo})
    except Exception as e:
        return error_response(f'Erro ao consultar saldo: {str(e)}')

@app.route('/deposito', methods=['POST'])
def deposito():
    try:
        dados = request.json
        sucesso = get_financial_service().realizar_deposito(
            dados['numero_conta'],
            float(dados['valor'])
        )
        return jsonify({'success': sucesso})
    except Exception as e:
        return error_response(f'Erro ao realizar depósito: {str(e)}')

@app.route('/saque', methods=['POST'])
def saque():
    try:
        dados = request.json
        sucesso = get_financial_service().realizar_saque(
            dados['numero_conta'],
            float(dados['valor'])
        )
        return jsonify({'success': sucesso})
    except Exception as e:
        return error_response(f'Erro ao realizar saque: {str(e)}')

@app.route('/transferencia', methods=['POST'])
def transferencia():
    try:
        dados = request.json
        sucesso = get_financial_service().realizar_transferencia(
            dados['conta_origem'],
            dados['conta_destino'],
            float(dados['valor']),
            dados.get('descricao', 'Transferência via internet banking')
        )
        return jsonify({'success': sucesso})
    except Exception as e:
        return error_response(f'Erro ao realizar transferência: {str(e)}')

@app.route('/estatisticas', methods=['GET'])
def estatisticas():
    """Endpoint para funcionários obterem estatísticas do banco"""
    try:
        stats = get_statistics_service().obter_estatisticas_banco()
        return jsonify(stats)
    except Exception as e:
        return error_response(f'Erro ao obter estatísticas: {str(e)}')

@app.route('/criar-cliente', methods=['POST'])
def criar_cliente():
    """Endpoint para funcionários criarem novos clientes"""
    try:
        dados = request.json
        numero_conta = get_account_service().criar_conta_cliente(
            dados['nome'],
            dados['cpf'],
            dados['data_nascimento'],
            dados['telefone'],
            dados['senha'],
            dados.get('saldo_inicial', 0)
        )
        
        if not numero_conta:
            return error_response('Erro ao criar cliente')
            
        return jsonify({'success': True, 'numero_conta': numero_conta})
    except Exception as e:
        return error_response(f'Erro ao criar cliente: {str(e)}')

@app.route('/criar-funcionario', methods=['POST'])
def criar_funcionario():
    """Endpoint para criar novos funcionários"""
    try:
        dados = request.json
        otp_inicial = get_account_service().criar_funcionario(
            dados['nome'],
            dados['cpf'],
            dados['senha'],
            dados['cargo'],
            dados['codigo_funcionario']
        )
        return jsonify({'success': True, 'otp_inicial': otp_inicial})
    except Exception as e:
        return error_response(f'Erro ao criar funcionário: {str(e)}')

@app.route('/consultar_otp/<cpf>', methods=['GET'])
def consultar_otp(cpf):
    try:
        otp = get_auth_service().consultar_otp_funcionario(cpf)
        if not otp:
            return error_response('Funcionário não encontrado', 404)
        return jsonify({'success': True, 'otp': otp})
    except Exception as e:
        return error_response(f'Erro ao consultar OTP: {str(e)}')

@app.route('/teste')
def teste():
    return jsonify({"message": "API funcionando", "status": "ok"})

@app.route('/consultar-cliente/<cpf>', methods=['GET'])
def consultar_cliente(cpf):
    """Endpoint para consultar informações de um cliente"""
    try:
        cliente = get_account_service().consultar_cliente(cpf)
        if not cliente:
            return error_response('Cliente não encontrado', 404)
        return jsonify(cliente)
    except Exception as e:
        return error_response(f'Erro ao consultar cliente: {str(e)}')

@app.route('/consultar-transacoes/<numero_conta>', methods=['GET'])
def consultar_transacoes(numero_conta):
    """Endpoint para consultar transações de uma conta"""
    try:
        transacoes = get_financial_service().consultar_transacoes(numero_conta)
        return jsonify(transacoes)
    except Exception as e:
        return error_response(f'Erro ao consultar transações: {str(e)}')

@app.route('/clientes-inadimplentes', methods=['GET'])
def consultar_inadimplentes():
    """Endpoint para consultar clientes inadimplentes"""
    try:
        inadimplentes = get_financial_service().consultar_inadimplentes()
        return jsonify(inadimplentes)
    except Exception as e:
        return error_response(f'Erro ao consultar inadimplentes: {str(e)}')

@app.route('/encerrar-conta', methods=['POST'])
def encerrar_conta():
    """Endpoint para encerrar conta de cliente"""
    try:
        dados = request.json
        sucesso = get_account_service().encerrar_conta(dados['numero_conta'])
        return jsonify({'success': sucesso})
    except Exception as e:
        return error_response(f'Erro ao encerrar conta: {str(e)}')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)