# Windows Login Email Alert

Script Python que envia um e-mail de alerta toda vez que alguém faz login no computador Windows. O e-mail inclui informações da sessão e uma foto tirada pela webcam no momento do login.

## O que é enviado no alerta

- Data e hora do login
- Nome do computador
- Usuário logado
- Versão do sistema operacional
- IP local e IP público
- Foto da webcam (se disponível)

## Pré-requisitos

- Python 3.10+
- Conta no [Resend](https://resend.com) com uma chave de API e um domínio verificado
- Webcam (opcional — o script funciona sem ela)

## Instalação

**1. Clone o repositório**

```bash
git clone https://github.com/sandropeixoto/windows-login-email-alert.git
cd windows-login-email-alert
```

**2. Instale as dependências**

```bash
pip install -r requirements.txt
```

**3. Configure as credenciais**

Edite as variáveis no topo do `login_alert.py`:

```python
RESEND_API_KEY = "re_SUA_CHAVE_AQUI"
FROM_EMAIL     = "alerta@seudominio.com"   # deve ser um domínio verificado no Resend
TO_EMAIL       = "voce@email.com"
```

Ou defina como variáveis de ambiente (recomendado):

```
RESEND_API_KEY=re_SUA_CHAVE_AQUI
ALERT_FROM=alerta@seudominio.com
ALERT_TO=voce@email.com
```

## Executar na inicialização do Windows

Para que o alerta seja disparado automaticamente a cada login:

1. Pressione `Win + R`, cole o caminho abaixo e dê Enter:
   ```
   %APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup
   ```
2. Crie um atalho do arquivo `run_alert.vbs` nessa pasta.

O `run_alert.vbs` executa o script Python em segundo plano usando `pythonw`, sem abrir nenhuma janela de terminal.

## Estrutura do projeto

```
windows-login-email-alert/
├── login_alert.py   # Script principal
├── run_alert.vbs    # Launcher silencioso para o Startup do Windows
├── requirements.txt # Dependências Python
└── login_alert.log  # Gerado automaticamente em tempo de execução
```

## Dependências

| Pacote | Uso |
|---|---|
| `resend` | Envio de e-mail via API |
| `requests` | Consulta do IP público |
| `opencv-python` | Captura de foto pela webcam |

## Log

Todas as execuções são registradas no arquivo `login_alert.log` criado automaticamente na mesma pasta do script.
