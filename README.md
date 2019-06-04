---
VISÃO GERAL
---

twitter-capture é um script em Python para coleta e stream de tweets.

Para coleta (REST API), múltiplas credenciais podem ser usadas; para stream,
autenticação requer também a chave e a senha do token de acesso (v1.1).

Requer a biblioteca python3-twython e credenciais no arquivo "config.py".

```
USO: twitter-capture.py [-h] [-v] -q QUERY
                        [-t {stream,terms,users,userids,ids,id}] [-l LANG]
                        [-g GEOCODE] [-n NUMBER] [-m MAX] [-s SINCE]
                        [-u URL] [-w WAIT] [--log LOG] [--nolog] [--nourl]
```

---
INSTALANDO
---

* **[Python](https://www.python.org/downloads/)** (3.6.8+)

Este script foi escrito na linguagem **Python** e requer a biblioteca
**Twython** para interagir com a API do Twitter. Para instalá-la, abra um
prompt de comando (```cmd```) ou terminal no seu computador e execute:

> * No **Linux** (Debian/Ubuntu): ```sudo apt install python3-twython```

> * No **Windows**:  ```py -3 -m pip install twython```

---
CONFIGURANDO
---

É necessário ter uma chave de aplicativo (*app key*) do Twitter, criada em:

> https://developer.twitter.com/en/apps

Antes de rodar o script, é preciso definir as credenciais do Twitter no arquivo
"config.py", na pasta do script, seguindo o exemplo em "config_EXAMPLE.py".

```
APP_KEYS            lista de chaves e senhas do Twitter, exemplo:
                    [ ['chave_1', 'senha_1'] , ['chave_2','senha_2'] ]
APP_KEY             necessário para stream ou coleta (se APP_KEYS indefinido)
APP_SECRET          necessário para stream ou coleta (se APP_KEYS indefinido)
OAUTH_TOKEN         necessário para stream apenas
OAUTH_TOKEN_SECRET  necessário para stream apenas
POST_URL            URL para enviar tweets capturados (padrão: nenhuma)
STREAM_RTS          ativa ou desativa o stream de retweets (padrão: True)
STREAM_ATS          ativa ou desativa o stream de respostas (padrão: True)
```

---
EXECUÇÃO
---

Para a execução, apenas o argumento QUERY (*-q*) é necessário. Lista com todos:

```
-h, --help                       mostra mensagem de ajuda e sai
-v, --version                    mostra versão do programa e sai
-q QUERY, --query QUERY          termos para buscar (OBRIGATÓRIO)
-t TYPE, --type TYPE             tipo de busca
                                   terms: termos ou hashtags (padrão)
                                   stream: tweets publicados ao vivo
                                   users: timelines de nomes de perfis
                                   userids: timelines de IDs de perfis
                                   ids: captura vários IDs de tweets
                                   id: captura um ID de tweet
-l LANG, --lang LANG             idioma para pesquisar por
-g GEOCODE, --geocode GEOCODE    localização de busca (ex: "-20.3,-40.2,100km")
                                                    ("latitude,longitude,raio")
-n NUMBER, --number NUMBER       number of tweets to finish search
-m MAX, --max MAX                máximo ID de tweet para capturar
-s SINCE, --since SINCE          mínimo ID de tweet para capturar
-u URL, --url URL                URL para enviar tweets capturados
-w WAIT, --wait WAIT             minutos para refazer pesquisa (padrão: OFF)
--log LOG                        salvar informações de execução no arquivo LOG
--nolog                          NÃO salvar informações de execução no arquivo
--nourl                          NÃO enviar tweets para a URL definida
```

---
EXEMPLOS
---

Capturar tweets com "Brasil" publicados nos últimos 9 dias:
```
twitter-capture.py -q "Brasil"
```

Capturar tweets que contém "Labic" em português a cada 15 minutos:
```
twitter-capture.py -q "Labic" -l pt -w 15
```

Capurar tweets que contém "#ForaTemer" em português apenas:
```
twitter-capture.py -q "#ForaTemer lang:pt" -t stream
```

Capturar os últimos 100 tweets da timeline de @ufeslabic:
```
twitter-capture.py -q "@ufeslabic" -t users -n 100
```

Lista de operadores disponíveis para busca no Twitter:
```
assitindo agora       contém ambos 'assitindo' e 'agora' (padrão)
“happy hour”          contém a frase exata 'happy hour'
amor ou odio          contém ou 'amor' ou 'ódio' (ou both)
#haiku                contém a hashtag 'haiku'
from:alexiskold       publicado pelo perfil 'alexiskold'
to:techcrunch         publicado para o perfil 'techcrunch'
@mashable             menciona o perfil 'mashable'
since:2015-07-19      publicado após a data '2015-07-19'
until:2015-07-19      publicado antes da data '2015-07-19'
filme -assustador     contém 'filme', mas não 'assustador'
cinema :)             contém 'cinema' com uma atitude positiva
aviao :(              contém 'aviao' com uma atitude negativa
transito ?            contém 'transito' e fazendo uma pergunta
gatos filter:links    contém 'gatos' com um link para um site
noticias source:web   contém 'noticias' e enviado pelo site
```