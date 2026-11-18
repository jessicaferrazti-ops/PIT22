# Pausa & Prosa — projeto acadêmico

Duas versões do website de uma cafeteria fictícia, com identidade visual própria.

## Tecnologias
- HTML, CSS e JavaScript
- Python 3 + Flask
- SQLite
- Organização inspirada em MVC: `models/`, `controllers/`, `templates/` e `static/`.

## Executar no Windows
1. Instale Python 3.
2. Abra a pasta da versão desejada.
3. Execute `iniciar_windows.bat`.
4. Acesse http://127.0.0.1:5000.

Ou manualmente: `python -m venv venv`, ative o ambiente, `pip install -r requirements.txt` e `python app.py`.

## Dados de demonstração
O banco SQLite é criado automaticamente na primeira execução e recebe produtos fictícios.

## Versão 2 — acesso administrativo
Usuário inicial: `admin`
Senha inicial: `pausa2026`
Defina `ADMIN_USER`, `ADMIN_PASSWORD` e `SECRET_KEY` como variáveis de ambiente antes de publicar. As credenciais padrão são apenas para demonstração local.

## Observação acadêmica
Os resultados de avaliação devem ser identificados como simulados caso não tenham sido realizados testes reais.
