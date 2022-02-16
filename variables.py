server = "admin auth log web"
transact = "bat bip bnb"
exchange = "batbnb bipbtc bnbbtc"

OUTPUT_ENV = "env_common"
OUTPUT_DB_NAME_PORT_LIST_OFFICE = "DB_NAME_PORT_LIST_OFFICE"
OUTPUT_DC_DB = "docker-compose-db.yml"
OUTPUT_DC_SERVER = "docker-compose-server.yml"
OUTPUT_DC_LOCAL = "docker-compose-local.yml"

DB_USER = "postgres"
DB_PASSWORD = "----"
DB_HOST = "10.0.0.0"
port_db = 5001
port_server = 8001
port_visor = 9001

supervisor_log = "devel"
supervisor_pass = "----"
supervisor_host = "exc-supervisor.tm"

######################################################
value_template_env = """
# Центрифуга
SERVER_SOCKET=z_centrifugo:8000/api
SOCKET_SERVER=z_centrifugo:8000/api
SERVER_WEBSOCKET_ADDRESS=ws://z_centrifugo:8000
SOCKET_HELPER_API_KEY=33333
"""

value_dc = """
version: '3.5'
services:
"""

def template_docker_compose_db(f_name, f_port):
    template = f"""
  db_{f_name}:
    container_name: db_{f_name}
    image: postgres:12.5
    restart: always
    volumes:
      - ./db/{f_name}:/var/lib/postgresql/data
    environment:
      POSTGRES_PASSWORD: {DB_PASSWORD}
      POSTGRES_USER: {DB_USER}
      POSTGRES_DB: {f_name}
    ports:
      - {f_port}:5432  
"""
    return template

def template_docker_compose_server(f_name, f_port_s, f_port_v, branch="${BRANCH}"):
    template = f"""
  {f_name}:
    container_name: {f_name}
    image: harbor.am/exchange/{f_name}:{branch}
    restart: always
    tty: true
    ports:
      - {f_port_s}:80
      - {f_port_v}:9001
    env_file:
      - ./env/env_common
      - ./env/.{f_name}
"""
    return template

def template_env_target(f_user, f_password, f_host, f_name, f_port):
    template = f"""
# База [Докер контейнер]
DB_FAMILY=pgsql:host={f_host};port={f_port};dbname={f_name}
DB_HOST={f_host}
DB_PORT={f_port}
DB_NAME={f_name}
DB_USER={f_user}
DB_PASSWORD={f_password}

# Прослушивание уведомлений от базы
POMM_DSN=pgsql://{f_user}:{f_password}@{f_host}:{f_port}/{f_name}

"""
    return template


value_dc_local = f"""
version: '3.5'
services:

  centrifugo:
    container_name: centrifugo  
    image: centrifugo/centrifugo:v3.1
    restart: always
    tty: true
    ulimits:
      nofile:
        soft: 65535
        hard: 65535
    volumes:
      - /var/www/html/web/.deploy/.local/centrifugo/config.json:/centrifugo/config.json
    command: centrifugo --config config.json --port=8000 --admin
    ports:
      - 8000:8000

  globalredis:
    container_name: globalredis
    image: redis:5-alpine3.12
    command: redis-server
    restart: always
    volumes:
      - /volumes/globalredis:/data

  proxy:
    container_name: proxy
    image: nginx:stable-alpine
    restart: always
    ports:
      - 80:80
    volumes:
      - /var/www/html/web/.deploy/.local/proxy/internal-proxy.conf:/etc/nginx/conf.d/web.conf
      - /var/www/html/p2p/.deploy/.local/proxy/internal-proxy.conf:/etc/nginx/conf.d/p2p.conf
      - /var/www/html/admin/.deploy/.local/proxy/internal-proxy.conf:/etc/nginx/conf.d/admin.conf
"""

def template_docker_compose_local_server(f_name, f_port_s, f_port_v):
    template = f"""
  {f_name}:
    container_name: {f_name}
    image: harbor/server/php:71
    restart: always
    tty: true
    environment:
      PHP_IDE_CONFIG: "serverName={f_name}.local"
    ports:
      - {f_port_s}:80
      - {f_port_v}:9001
    volumes:
      - /var/www/html/sigen/{f_name}:/var/www/html
      - /var/www/html/sigen/{f_name}/.deploy/.local/server.conf:/etc/nginx/conf.d/server.conf
      - /var/www/html/sigen/{f_name}/.deploy/.local/20-xdebug.ini:/etc/php/7.1/fpm/conf.d/20-xdebug.ini
    working_dir: /var/www/html/
    env_file:
      - /var/www/html/sigen/.deploy/env_common
      - /var/www/html/sigen/{f_name}/.deploy/.local/.env.local
      
"""
    return template

def template_docker_compose_local_transact(f_name, f_port_s, f_port_v):
    template = f"""
  {f_name}:
    image: harbor/server/php:71
    container_name: {f_name}
    restart: always
    tty: true
    environment:
      PHP_IDE_CONFIG: "serverName={f_name}.local"
    ports:
      - {f_port_s}:80
      - {f_port_v}:9001
    volumes:
      - /var/www/html/sigen/transact:/var/www/html
      - /var/www/html/sigen/transact/.deploy/.local/{f_name}/server.conf:/etc/nginx/conf.d/server.conf
      - /var/www/html/sigen/transact/.deploy/.local/20-xdebug.ini:/etc/php/7.1/fpm/conf.d/20-xdebug.ini
    working_dir: /var/www/html/.deploy/.local/{f_name}
    env_file:
      - /var/www/html/sigen/.deploy/env_common
      - /var/www/html/sigen/transact/.deploy/.local/{f_name}/.env.local
      
"""
    return template

def template_docker_compose_local_exchange(f_name, f_port_s, f_port_v):
    template = f"""
  {f_name}:
    container_name: {f_name}  
    image: harbor/server/php:71
    restart: always
    tty: true
    environment:
      PHP_IDE_CONFIG: "serverName={f_name}.local"
    ports:
      - {f_port_s}:80
      - {f_port_v}:9001
    volumes:
      - /var/www/html/exchange:/var/www/html
      - /var/www/html/exchange/.deploy/.local/{f_name}/server.conf:/etc/nginx/conf.d/server.conf
      - /var/www/html/exchange/.deploy/.local/20-xdebug.ini:/etc/php/7.1/fpm/conf.d/20-xdebug.ini
    working_dir: /var/www/html/.deploy/.local/{f_name}
    env_file:
      - /var/www/html/.deploy/env_common
      - /var/www/html/exchange/.deploy/.local/{f_name}/.env.local   
    
"""
    return template

template_yii = f"""
<?php
$a = require_once __DIR__ . '/../yii-common-local.php';
eval($a);

"""

template_index = f"""
<?php
$a = require_once __DIR__ . '/../index-common-local.php';
eval($a);

"""

template_exchange_env = f"""
# Валюты
SERVER_MAIN_CURRENCY=
SERVER_LAST_CURRENCY=

# Id торговых ботов
EXCHANGE_BOT_IDS=111,11

"""

template_server_local = """
upstream php_fpm {
    server unix:/run/php/php7.1-fpm.sock;
}

server {
    listen      80;
    server_name {server}.local;

    charset utf-8;
    client_max_body_size 128M;

    root   /var/www/html/.deploy/.local/{server};
    index  index.php;

    location / {
        try_files $uri $uri/ /index.php$is_args$args;
    }

    location ~ ^/assets/.*\.php$ {
        deny all;
    }

    location ~ ^/(status|ping)$ {
        include        fastcgi_params;
        fastcgi_param  SCRIPT_FILENAME /var/www/html/.deploy/.local/{server}/index.php;
        fastcgi_pass   php_fpm;
    }

    location ~ \.php$ {
        include        fastcgi_params;
        fastcgi_param  SCRIPT_FILENAME $document_root$fastcgi_script_name;
        fastcgi_pass   php_fpm;
        try_files      $uri =404;
    }

    location ~* /\. {
        deny all;
    }
}

"""

################### supervisor ###################
template_supervisor_conf_header = """<?php
# Title name
$config['title'] = 'Local supervisors monitoring';

# Dashboard columns. 2 or 3
$config['supervisor_cols'] = 3;

# Refresh Dashboard every x seconds. 0 to disable
$config['refresh'] = 0;

# Enable or disable Alarm Sound
$config['enable_alarm'] = false;

# Show hostname after server name
$config['show_host'] = false;

$config['supervisor_servers'] = [
"""

def template_supervisor_conf(f_name):
    template = f"""
    '{f_name}' => [
        'external_url' => 'https://{supervisor_log}:{supervisor_pass}@{supervisor_host}/super{f_name}',
        'url' => 'http://{f_name}/RPC2',
        'port' => '9001',
    ],    
"""
    return template


template_supervisor_conf_footer = """
];

# Set timeout connecting to remote supervisord RPC2 interface
$config['timeout'] = 3;

# Path to Redmine new issue url
$config['redmine_url'] = ''; # http://redmine.url/path_to_new_issue_url

# Default Redmine assigne ID
$config['redmine_assigne_id'] = ''; # 69
"""

################### ###################


template_nginx_conf = """
    location /super{f_name}/ {
        auth_basic "Restricted Area";
        auth_basic_user_file /etc/nginx/.htpasswd;
        rewrite ^/super{f_name}(.+)$ $1 break;
        proxy_pass http://localhost:{f_port_v};
        proxy_http_version 1.1;
        proxy_buffering off;
        proxy_set_header Connection "";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
"""

def template_dockerfile_exchange(f_name):
    template = f"""
FROM harbor.smw.team/exchange/exchange:default

COPY .deploy/office/{f_name}/daemon.conf /etc/supervisor/conf.d/
COPY .deploy/office/{f_name}/server.conf /etc/nginx/conf.d/
#COPY .deploy/office/{f_name}/.env.office /var/www/html/.env

WORKDIR /var/www/html/  
"""
    return template

def template_dockerfile_transact(f_name):
    template = f"""
FROM harbor/exchange/transact:default

COPY daemon.conf /etc/supervisor/conf.d/
COPY server.conf /etc/nginx/conf.d/

WORKDIR /var/www/html

"""
    return template