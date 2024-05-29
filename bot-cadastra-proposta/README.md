## Cadastrar propostas no BP

Esse bot foi feito...

## Primeiros passos

1. Crie um ambiente virtual para nao prejudicar a sua maquina.

Vá até o diretório do `bot-cadastra-proposta` e execute o comando:

```sh
python3 -m venv .venv
```

2. Ative o ambiente virtual

```sh
source .venv/bin/activate
```

3. Instale as dependencias

```
pip install -r requirements.txt
```

4. Altere as configurações do projeto

Dentro do arquivo `config_prod.json` e `config_dev.json` altere o valor da chave `chrome_user_data_dir` onde está o usuário 'gio' para o seu usuário.

Para descobrir seu nome de usuário, basta abrir um novo terminal e rodar os comandos:

```sh
cd
cd ..
ls
```

Será mostrado seu nome de usuário.

5. Execute o chrome com uma porta de debug aberta

Execute o seguinte comando em um novo terminal, lembrando de trocar `gio` pelo seu usuário.

```
google-chrome --remote-debugging-port=9222 --user-data-dir=/home/gio/.config/google-chrome/Default
```

6. Agora realize o login no gov.

Certifique-se de realizar o login antes de rodar o código.

7. Rode o código.

No terminal onde voce executou o passo 2, rode o seguinte comando:

```
python main.py
```

E agora basta seguir as instruções!!