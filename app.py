from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import pytz 
import firebase_admin
from firebase_admin import credentials, db 
import time 

# --- CONFIGURAÇÃO ---
app = Flask(__name__)
# Certifique-se de que a SECRET_KEY é única e segura
app.config['SECRET_KEY'] = 'uma_chave_secreta_muito_segura' 

# ----------------------------------------------------
# CONFIGURAÇÃO E CONEXÃO FIREBASE (Realtime Database)
# ----------------------------------------------------
DB_ROOT = None
CONEXAO_OK = False
try:
    # O NOME DO ARQUIVO FOI ATUALIZADO PARA CORRESPONDER AO ARQUIVO QUE VOCÊ CARREGOU.
    cred = credentials.Certificate("ttk2k-642d6-firebase-adminsdk-fbsvc-c83144bedb.json")

    # URL DO SEU BANCO DE DADOS REALTIME
    FIREBASE_URL = 'https://ttk2k-642d6-default-rtdb.firebaseio.com' 
    firebase_admin.initialize_app(cred, {
        'databaseURL': FIREBASE_URL
    })

    DB_ROOT = db.reference()
    CONEXAO_OK = True
    print("Conexão Firebase Realtime Database estabelecida com sucesso!")

except Exception as e:
    # Esta mensagem agora será exibida no console se houver falha
    print(f"ERRO DE CONEXÃO FIREBASE: {e}")
    print("Verifique o arquivo de credenciais e a URL.")
    # A variável CONEXAO_OK permanece False
    

# ----------------------------------------------------
# MAPAS DE DADOS 
# ----------------------------------------------------
STATUS_MAP = {
    1: {'nome': 'Não iniciado', 'cor': 'red'},
    2: {'nome': 'Em andamento', 'cor': 'orange'},
    3: {'nome': 'Concluído', 'cor': 'green'}
}
PRIORIDADE_MAP = {
    1: 'Baixa',
    2: 'Média',
    3: 'Alta'
}

# --- FUNÇÕES AUXILIARES ---

def verificar_conexao(f):
    """Decorator para verificar a conexão antes de executar rotas que dependem do DB.
    Esta função é usada apenas em rotas PÓS-LOGIN."""
    def wrapper(*args, **kwargs):
        if not CONEXAO_OK:
            # Flasha a mensagem de erro da conexão e redireciona para login
            flash("Erro de conexão com o banco de dados. Tente novamente mais tarde.", 'danger')
            return redirect(url_for('login')) 
        return f(*args, **kwargs)
    wrapper.__name__ = f.__name__
    return wrapper

def datetime_brasilia(dt_timestamp):
    # Recebe timestamp (em milissegundos) ou None
    if not dt_timestamp:
        return ""
        
    try:
        dt_utc = datetime.fromtimestamp(dt_timestamp / 1000)
    except:
        return "Data Inválida"

    utc_tz = pytz.utc
    brasilia_tz = pytz.timezone('America/Sao_Paulo')
    
    dt_utc = utc_tz.localize(dt_utc)
    dt_brasilia = dt_utc.astimezone(brasilia_tz)
    
    return dt_brasilia.strftime('%d/%m/%Y %H:%M:%S')

# Adiciona o filtro customizado ao Jinja2
app.jinja_env.filters['datetime_brasilia'] = datetime_brasilia


def login_required(f):
    def wrapper(*args, **kwargs):
        if 'logged_in' not in session:
            flash('Você precisa estar logado para acessar esta página.', 'danger')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    wrapper.__name__ = f.__name__
    return wrapper

def get_all_users():
    """Retorna um dicionário {user_id: user_data} de todos os usuários."""
    if not CONEXAO_OK:
        return {}
    usuarios_ref = DB_ROOT.child('usuarios')
    return usuarios_ref.get() or {}


# --- ROTAS DE AUTENTICAÇÃO ---
# Essas rotas não usam @verificar_conexao para permitir que a tela de login/cadastro abra,
# mesmo que o DB esteja fora do ar. A conexão é verificada manualmente no POST.

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        # Verifica a conexão no POST (onde o DB é usado)
        if not CONEXAO_OK:
            flash("Erro de conexão: Não foi possível salvar o cadastro.", 'danger')
            return redirect(url_for('cadastro'))

        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']

        usuarios_ref = DB_ROOT.child('usuarios')
        # Busca usuários com o email fornecido (depende do índice ".indexOn": "email" no Firebase)
        usuarios = usuarios_ref.order_by_child('email').equal_to(email).get()

        if usuarios:
            flash('E-mail já cadastrado.', 'danger')
            return redirect(url_for('cadastro'))

        novo_usuario_data = {
            'nome': nome,
            'email': email,
            'senha_hash': generate_password_hash(senha),
            'data_registro': int(datetime.now().timestamp() * 1000), 
            'status_conta': True,
            # Adiciona um placeholder de foto de perfil
            'foto_perfil_url': f"https://placehold.co/40x40/3b82f6/ffffff?text={nome[0].upper()}"
        }
        
        usuarios_ref.push(novo_usuario_data)
        
        flash('Cadastro realizado com sucesso! Faça login.', 'success')
        return redirect(url_for('login'))
        
    return render_template('cadastro.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Verifica a conexão no POST (onde o DB é usado)
        if not CONEXAO_OK:
            flash("Erro de conexão: Não foi possível realizar o login.", 'danger')
            return redirect(url_for('login'))
            
        email = request.form['email']
        senha = request.form['senha']

        usuarios_ref = DB_ROOT.child('usuarios')
        # Busca usuários com o email fornecido (depende do índice ".indexOn": "email" no Firebase)
        resultado = usuarios_ref.order_by_child('email').equal_to(email).get()

        if resultado:
            user_firebase_id, user_data = list(resultado.items())[0] 

            if check_password_hash(user_data['senha_hash'], senha):
                session['logged_in'] = True
                session['user_id'] = user_firebase_id 
                session['user_nome'] = user_data['nome']
                # Armazena a foto de perfil na sessão
                session['user_foto'] = user_data.get('foto_perfil_url', 'https://placehold.co/40x40/3b82f6/ffffff?text=U')
                flash('Login bem-sucedido!', 'success')
                return redirect(url_for('index'))
            else:
                flash('E-mail ou senha inválidos.', 'danger')
                return redirect(url_for('login'))
        else:
            flash('E-mail ou senha inválidos.', 'danger')
            return redirect(url_for('login'))
            
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Você foi desconectado.', 'info')
    return redirect(url_for('login'))


# --- ROTAS DE DADOS (USANDO DECORATORS) ---

@app.route('/')
@login_required
@verificar_conexao
def index():
    tarefas_ref = DB_ROOT.child('tarefas')
    tarefas_dict = tarefas_ref.get() 
    
    tarefas_list = []
    if tarefas_dict:
        for firebase_id, tarefa_data in tarefas_dict.items():
            tarefa_data['firebase_id'] = firebase_id
            
            # Mapeia status e prioridade
            tarefa_data['status'] = STATUS_MAP.get(tarefa_data.get('status_id'), {'nome': 'N/A', 'cor': 'gray'})
            tarefa_data['prioridade'] = PRIORIDADE_MAP.get(tarefa_data.get('prioridade_id'), 'N/A')
            
            # TODO: Adicionar lógica para buscar nome do projeto pelo ID
            
            tarefas_list.append(tarefa_data)
            
    # Ordena as tarefas pela data de criação (mais recente primeiro)
    tarefas_list.sort(key=lambda t: t.get('data_criacao', 0), reverse=True)

    return render_template('index.html', tarefas=tarefas_list)


@app.route('/nova_tarefa', methods=['GET', 'POST'])
@login_required
@verificar_conexao
def nova_tarefa():
    # Carrega projetos para seleção
    projetos_data = DB_ROOT.child('projetos').get() or {}
    projetos_opcoes = [{'id': id, 'nome': data['nome']} for id, data in projetos_data.items()]

    # Passa as opções para o template
    status_opcoes = [{'id': k, 'nome': v['nome']} for k, v in STATUS_MAP.items()]
    prioridade_opcoes = [{'id': k, 'nome': v} for k, v in PRIORIDADE_MAP.items()]
    tags_opcoes = DB_ROOT.child('tags').get() or {}
    
    if request.method == 'POST':
        # Conversão para int é importante para o mapeamento
        titulo = request.form['titulo']
        descricao = request.form['descricao']
        status_id = int(request.form['status_id'])
        prioridade_id = int(request.form['prioridade_id'])
        projeto_id = request.form.get('projeto_id') # Pode ser None
        
        # Tags vêm como lista, se selecionadas
        tags_selecionadas = request.form.getlist('tags') 

        nova_tarefa_data = {
            'titulo': titulo,
            'descricao': descricao,
            'status_id': status_id,
            'prioridade_id': prioridade_id,
            'data_criacao': int(datetime.now().timestamp() * 1000), 
            'data_conclusao': None,
            'id_usuario_criador': session.get('user_id'),
            'id_projeto': projeto_id if projeto_id != 'None' else None, # Salva o ID do projeto
            'tags': tags_selecionadas,
            'subtarefas': [], # Inicializa com lista vazia para subtarefas
            'anexos': [] # Inicializa com lista vazia para anexos
        }
        
        tarefas_ref = DB_ROOT.child('tarefas')
        tarefas_ref.push(nova_tarefa_data)
        
        flash('Tarefa criada com sucesso!', 'success')
        return redirect(url_for('index'))
        
    return render_template('nova_tarefa.html', 
                           status_opcoes=status_opcoes, 
                           prioridade_opcoes=prioridade_opcoes,
                           projetos_opcoes=projetos_opcoes,
                           tags_opcoes=tags_opcoes)


@app.route('/tarefa/<string:firebase_id>', methods=['GET'])
@login_required
@verificar_conexao
def tarefa(firebase_id):
    tarefa_ref = DB_ROOT.child('tarefas').child(firebase_id)
    tarefa_data = tarefa_ref.get()
    
    if not tarefa_data:
        flash('Tarefa não encontrada.', 'danger')
        return redirect(url_for('index'))

    tarefa_data['firebase_id'] = firebase_id
    tarefa_data['status'] = STATUS_MAP.get(tarefa_data.get('status_id'), {'nome': 'N/A', 'cor': 'gray'})
    tarefa_data['prioridade'] = PRIORIDADE_MAP.get(tarefa_data.get('prioridade_id'), 'N/A')
    
    # Prepara Subtarefas e Anexos (garante que são listas)
    tarefa_data['subtarefas'] = tarefa_data.get('subtarefas') or []
    tarefa_data['anexos'] = tarefa_data.get('anexos') or []

    comentarios_ref = DB_ROOT.child('comentarios').child(firebase_id)
    comentarios_dict = comentarios_ref.get()
    
    comentarios_list = []
    if comentarios_dict:
        for comm_id, comm_data in comentarios_dict.items():
            comm_data['autor_nome'] = comm_data.get('autor_nome', 'Usuário Desconhecido') 
            comentarios_list.append(comm_data)
        
        comentarios_list.sort(key=lambda c: c.get('data_comentario', 0), reverse=True)

    # Buscar Tags para exibição
    tags_data = DB_ROOT.child('tags').get() or {}
    tags_na_tarefa = [tags_data[tag_id] for tag_id in tarefa_data.get('tags', []) if tag_id in tags_data]


    return render_template('tarefa.html', 
                           tarefa=tarefa_data, 
                           comentarios=comentarios_list,
                           tags_na_tarefa=tags_na_tarefa)

# --- Subtarefas e Anexos (Integração na Rota de Tarefa) ---

@app.route('/tarefa/<string:firebase_id>/add_subtarefa', methods=['POST'])
@login_required
@verificar_conexao
def add_subtarefa(firebase_id):
    tarefa_ref = DB_ROOT.child('tarefas').child(firebase_id)
    descricao = request.form['descricao']
    
    tarefa_data = tarefa_ref.get()
    subtarefas = tarefa_data.get('subtarefas', [])
    
    novo_subtarefa = {
        'descricao': descricao,
        'concluida': False,
        'data_criacao': int(datetime.now().timestamp() * 1000)
    }
    subtarefas.append(novo_subtarefa)
    
    tarefa_ref.update({'subtarefas': subtarefas})
    flash('Subtarefa adicionada!', 'success')
    return redirect(url_for('tarefa', firebase_id=firebase_id))

@app.route('/tarefa/<string:firebase_id>/toggle_subtarefa/<int:index>')
@login_required
@verificar_conexao
def toggle_subtarefa(firebase_id, index):
    tarefa_ref = DB_ROOT.child('tarefas').child(firebase_id)
    tarefa_data = tarefa_ref.get()
    subtarefas = tarefa_data.get('subtarefas', [])
    
    if 0 <= index < len(subtarefas):
        subtarefas[index]['concluida'] = not subtarefas[index]['concluida']
        tarefa_ref.update({'subtarefas': subtarefas})
        flash('Status da subtarefa atualizado!', 'info')
    
    return redirect(url_for('tarefa', firebase_id=firebase_id))

@app.route('/tarefa/<string:firebase_id>/add_anexo', methods=['POST'])
@login_required
@verificar_conexao
def add_anexo(firebase_id):
    tarefa_ref = DB_ROOT.child('tarefas').child(firebase_id)
    nome = request.form['nome']
    url = request.form['url'] # Simulando URL de anexo/link
    
    tarefa_data = tarefa_ref.get()
    anexos = tarefa_data.get('anexos', [])
    
    novo_anexo = {
        'nome': nome,
        'url': url,
        'data_upload': int(datetime.now().timestamp() * 1000)
    }
    anexos.append(novo_anexo)
    
    tarefa_ref.update({'anexos': anexos})
    flash('Anexo adicionado!', 'success')
    return redirect(url_for('tarefa', firebase_id=firebase_id))

# --- Fim Subtarefas e Anexos ---


@app.route('/comentario/<string:firebase_id>', methods=['POST'])
@login_required
@verificar_conexao
def comentar(firebase_id):
    conteudo = request.form['conteudo']
    id_usuario = session.get('user_id')
    user_nome = session.get('user_nome')

    novo_comentario_data = {
        'id_usuario': id_usuario,
        'autor_nome': user_nome, 
        'conteudo': conteudo,
        'data_comentario': int(datetime.now().timestamp() * 1000)
    }
    
    comentarios_ref = DB_ROOT.child('comentarios').child(firebase_id)
    comentarios_ref.push(novo_comentario_data)
    
    flash('Comentário adicionado!', 'success')
    return redirect(url_for('tarefa', firebase_id=firebase_id))


@app.route('/deletar_tarefa/<string:firebase_id>', methods=['POST'])
@login_required
@verificar_conexao
def deletar_tarefa(firebase_id):
    tarefa_ref = DB_ROOT.child('tarefas').child(firebase_id)
    tarefa_data = tarefa_ref.get()
    
    if not tarefa_data:
        flash('Erro: Tarefa não encontrada.', 'danger')
        return redirect(url_for('index'))
        
    tarefa_ref.delete()
    
    # Deleta comentários associados
    DB_ROOT.child('comentarios').child(firebase_id).delete()
    
    flash(f'Tarefa "{tarefa_data.get("titulo", "N/A")}" e seus itens associados foram excluídos com sucesso.', 'success')
    return redirect(url_for('index'))

@app.route('/editar_tarefa/<string:firebase_id>', methods=['GET', 'POST'])
@login_required
@verificar_conexao
def editar_tarefa(firebase_id):
    tarefa_ref = DB_ROOT.child('tarefas').child(firebase_id)
    tarefa_data = tarefa_ref.get()
    
    if not tarefa_data:
        flash('Tarefa não encontrada.', 'danger')
        return redirect(url_for('index'))

    status_opcoes = [{'id': k, 'nome': v['nome']} for k, v in STATUS_MAP.items()]
    prioridade_opcoes = [{'id': k, 'nome': v} for k, v in PRIORIDADE_MAP.items()]
    
    projetos_data = DB_ROOT.child('projetos').get() or {}
    projetos_opcoes = [{'id': id, 'nome': data['nome']} for id, data in projetos_data.items()]
    
    tags_opcoes = DB_ROOT.child('tags').get() or {}
    
    if request.method == 'POST':
        update_data = {
            'titulo': request.form['titulo'],
            'descricao': request.form['descricao'],
            'status_id': int(request.form['status_id']),
            'prioridade_id': int(request.form['prioridade_id']),
            'id_projeto': request.form.get('projeto_id') if request.form.get('projeto_id') != 'None' else None,
            'tags': request.form.getlist('tags')
        }
        
        tarefa_ref.update(update_data)
        
        flash('Tarefa atualizada com sucesso!', 'success')
        return redirect(url_for('tarefa', firebase_id=firebase_id))
        
    tarefa_data['firebase_id'] = firebase_id
    # Passa as opções e a tarefa existente para o template
    return render_template('editar_tarefa.html', 
                           tarefa=tarefa_data, 
                           status_opcoes=status_opcoes, 
                           prioridade_opcoes=prioridade_opcoes,
                           projetos_opcoes=projetos_opcoes,
                           tags_opcoes=tags_opcoes)

@app.route('/concluir_tarefa/<string:firebase_id>')
@login_required
@verificar_conexao
def concluir_tarefa(firebase_id):
    tarefa_ref = DB_ROOT.child('tarefas').child(firebase_id)
    
    tarefa_ref.update({
        'status_id': 3, # 3 é o ID de Concluído
        'data_conclusao': int(datetime.now().timestamp() * 1000)
    })
    
    flash('Tarefa concluída!', 'success')
    return redirect(url_for('index'))


# --- ROTAS DE PROJETOS (CRUD) ---

@app.route('/projetos')
@login_required
@verificar_conexao
def projetos():
    projetos_data = DB_ROOT.child('projetos').get() or {}
    projetos_list = []
    for id, data in projetos_data.items():
        data['firebase_id'] = id
        projetos_list.append(data)
        
    return render_template('projetos.html', projetos_list=projetos_list)

@app.route('/novo_projeto', methods=['GET', 'POST'])
@login_required
@verificar_conexao
def novo_projeto():
    if request.method == 'POST':
        nome = request.form['nome']
        descricao = request.form['descricao']
        
        novo_projeto_data = {
            'nome': nome,
            'descricao': descricao,
            'data_criacao': int(datetime.now().timestamp() * 1000)
        }
        DB_ROOT.child('projetos').push(novo_projeto_data)
        flash('Projeto criado com sucesso!', 'success')
        return redirect(url_for('projetos'))
        
    return render_template('novo_projeto.html')

@app.route('/deletar_projeto/<string:firebase_id>', methods=['POST'])
@login_required
@verificar_conexao
def deletar_projeto(firebase_id):
    projeto_ref = DB_ROOT.child('projetos').child(firebase_id)
    projeto_data = projeto_ref.get()
    
    if not projeto_data:
        flash('Erro: Projeto não encontrado.', 'danger')
        return redirect(url_for('projetos'))
        
    projeto_ref.delete()
    flash(f'Projeto "{projeto_data.get("nome", "N/A")}" excluído com sucesso.', 'success')
    return redirect(url_for('projetos'))


# --- ROTAS DE EQUIPES (CRUD e Membros) ---

@app.route('/equipes')
@login_required
@verificar_conexao
def equipes():
    equipes_data = DB_ROOT.child('equipes').get() or {}
    equipes_list = []
    for id, data in equipes_data.items():
        data['firebase_id'] = id
        data['total_membros'] = len(data.get('membros', []))
        equipes_list.append(data)
        
    return render_template('equipes.html', equipes_list=equipes_list)

@app.route('/nova_equipe', methods=['GET', 'POST'])
@login_required
@verificar_conexao
def nova_equipe():
    if request.method == 'POST':
        nome = request.form['nome']
        descricao = request.form['descricao']
        
        nova_equipe_data = {
            'nome': nome,
            'descricao': descricao,
            'membros': [], # Lista de IDs de usuário
            'data_criacao': int(datetime.now().timestamp() * 1000)
        }
        DB_ROOT.child('equipes').push(nova_equipe_data)
        flash('Equipe criada com sucesso! Adicione membros agora.', 'success')
        return redirect(url_for('equipes'))
        
    return render_template('nova_equipe.html')


@app.route('/equipe/<string:firebase_id>/membros', methods=['GET', 'POST'])
@login_required
@verificar_conexao
def gerenciar_membros(firebase_id):
    equipe_ref = DB_ROOT.child('equipes').child(firebase_id)
    equipe_data = equipe_ref.get()
    
    if not equipe_data:
        flash('Equipe não encontrada.', 'danger')
        return redirect(url_for('equipes'))

    todos_usuarios = get_all_users()
    membros_ids = equipe_data.get('membros', [])
    
    # Mapeia IDs para dados completos
    membros_atuais = [{'id': uid, 'nome': todos_usuarios.get(uid, {}).get('nome', 'Usuário Desconhecido'), 'email': todos_usuarios.get(uid, {}).get('email', 'N/A')} 
                     for uid in membros_ids if uid in todos_usuarios]
    
    # Usuários disponíveis (não membros)
    disponiveis = [{'id': uid, 'nome': data.get('nome'), 'email': data.get('email')} 
                   for uid, data in todos_usuarios.items() if uid not in membros_ids]

    if request.method == 'POST':
        # Esta rota lida com a adição de membros
        user_id = request.form['user_id']
        
        if user_id not in membros_ids and user_id in todos_usuarios:
            membros_ids.append(user_id)
            equipe_ref.update({'membros': membros_ids})
            flash(f'Membro adicionado à equipe "{equipe_data["nome"]}".', 'success')
        
        return redirect(url_for('gerenciar_membros', firebase_id=firebase_id))

    return render_template('gerenciar_membros.html', 
                           equipe=equipe_data, 
                           membros_atuais=membros_atuais, 
                           disponiveis=disponiveis,
                           firebase_id=firebase_id)

@app.route('/equipe/<string:equipe_id>/remover_membro/<string:user_id>', methods=['POST'])
@login_required
@verificar_conexao
def remover_membro(equipe_id, user_id):
    equipe_ref = DB_ROOT.child('equipes').child(equipe_id)
    equipe_data = equipe_ref.get()
    
    if not equipe_data:
        flash('Equipe não encontrada.', 'danger')
        return redirect(url_for('equipes'))
        
    membros_ids = equipe_data.get('membros', [])
    
    try:
        membros_ids.remove(user_id)
        equipe_ref.update({'membros': membros_ids})
        flash('Membro removido com sucesso.', 'info')
    except ValueError:
        flash('Erro: Membro não estava na equipe.', 'warning')
        
    return redirect(url_for('gerenciar_membros', firebase_id=equipe_id))


# --- ROTAS DE TAGS (CRUD) ---

@app.route('/tags')
@login_required
@verificar_conexao
def tags():
    tags_data = DB_ROOT.child('tags').get() or {}
    tags_list = []
    for id, data in tags_data.items():
        data['firebase_id'] = id
        tags_list.append(data)
        
    return render_template('tags.html', tags_list=tags_list)

@app.route('/nova_tag', methods=['POST'])
@login_required
@verificar_conexao
def nova_tag():
    nome = request.form['nome']
    
    if not nome:
        flash('O nome da Tag não pode ser vazio.', 'warning')
        return redirect(url_for('tags'))
        
    nova_tag_data = {
        'nome': nome,
        'cor': request.form.get('cor', '#3b82f6'), # Cor padrão azul
        'data_criacao': int(datetime.now().timestamp() * 1000)
    }
    DB_ROOT.child('tags').push(nova_tag_data)
    flash('Tag criada com sucesso!', 'success')
    return redirect(url_for('tags'))

@app.route('/deletar_tag/<string:firebase_id>', methods=['POST'])
@login_required
@verificar_conexao
def deletar_tag(firebase_id):
    tag_ref = DB_ROOT.child('tags').child(firebase_id)
    tag_data = tag_ref.get()
    
    if not tag_data:
        flash('Erro: Tag não encontrada.', 'danger')
        return redirect(url_for('tags'))
        
    tag_ref.delete()
    flash(f'Tag "{tag_data.get("nome", "N/A")}" excluída com sucesso.', 'success')
    return redirect(url_for('tags'))


# --- ROTAS DE LISTAGEM SIMPLES ---
# Rotas /membros, /historico, /subtarefas continuam como listagem, mas agora /membros usa o get_all_users

@app.route('/membros')
@login_required
@verificar_conexao
def membros():
    usuarios_data = get_all_users()
    usuarios_list = []
    
    if usuarios_data:
        for id, data in usuarios_data.items():
            data['firebase_id'] = id
            data['foto_perfil_url'] = data.get('foto_perfil_url', 'https://placehold.co/40x40/3b82f6/ffffff?text=U') # Garantir foto
            usuarios_list.append(data)
    
    return render_template('membros.html', usuarios_list=usuarios_list)
    
@app.route('/historico')
@login_required
@verificar_conexao
def historico():
    # Retorna o template vazio
    return render_template('historico.html', historico_items=[]) 

@app.route('/subtarefas')
@login_required
@verificar_conexao
def subtarefas():
    # Retorna o template vazio (Esta rota não é mais usada para CRUD, a lógica está em /tarefa/<id>)
    return render_template('subtarefas.html', subtarefas=[]) 


if __name__ == '__main__':
    app.run(debug=True)