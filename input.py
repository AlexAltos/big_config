from variables import *
import shutil
import os

path = os.path.abspath(os.curdir)  # путь запуска скрипта
script_path = f"{path}/gitlab"

# рекурсивное удаление папки и фалов
if os.path.isdir(script_path):
    print("-- dell folder gitlab-- ")
    path_dell = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'gitlab')
    shutil.rmtree(path_dell)
    # Создаем папку gitlab
    os.mkdir(script_path)

# Удаляем дубли, сортируем по имени
server = sorted(set(server.split()))
transact = sorted(set(transact.split()))
exchange = sorted(set(exchange.split()))



# Создаем массив с именами и портами
main_list_variables=[]
for nn in server :
    name_list = {"group": "server", "name": nn, "port_db": port_db, "port_server": port_server, "port_visor": port_visor}
    port_db += 1
    port_server += 1
    port_visor += 1
    main_list_variables.append(name_list)

for nn in transact :
    name_list = {"group": "transact", "name": nn, "port_db": port_db, "port_server": port_server, "port_visor": port_visor}
    port_db += 1
    port_server += 1
    port_visor += 1
    main_list_variables.append(name_list)

for nn in exchange :
    name_list = {"group": "exchange", "name": nn, "port_db": port_db, "port_server": port_server, "port_visor": port_visor}
    port_db += 1
    port_server += 1
    port_visor += 1
    main_list_variables.append(name_list)



#############  git clone #############
def git_clone_sigen():

    def git_clone(f_name, f_clone_general, f_branch_general):
        from git import Repo

        print(f"clone: {f_name}")
        Repo.clone_from(
            f"{f_clone_general}",
            f"{script_path}/{f_name}",
            branch=f_branch_general
        )

    name_general = 'general'
    clone_general = 'git@gitlab/general.git'
    branch_general = "main"

    name_transact = 'transact'
    clone_transact = 'git@gitlab/transact.git'
    branch_transact = "main"

    name_project = 'project'
    clone_Project = "git@gitlab/project.git"
    branch_Project = "main"

    name_nginx = 'nginx'
    clone_nginx = "git@gitlab/nginx.git"
    branch_nginx = "main"

    git_clone(name_general, clone_general, branch_general)
    git_clone(name_transact, clone_transact, branch_transact)
    git_clone(name_project, clone_Project, branch_Project)
    git_clone(name_nginx, clone_nginx, branch_nginx)


def docker_compose_db():
    name = OUTPUT_DC_DB
    print(f"-> {name}")
    value = value_dc  # берем статичные параметры из переменной

    for index, element in enumerate(main_list_variables):
        if element["group"] == "server":
            value += template_docker_compose_db(element["name"], element["port_db"])

    for index, element in enumerate(main_list_variables):
        if element["group"] == "transact":
            value += template_docker_compose_db(element["name"], element["port_db"])

    for index, element in enumerate(main_list_variables):
        if element["group"] == "exchange":
            value += template_docker_compose_db(element["name"], element["port_db"])

    file = open(f"{script_path}/{name}", "w")
    file.write(value)
    file.close()


def docker_compose_server():
    name = OUTPUT_DC_SERVER
    print(f"-> {name}")
    value = value_dc  # берем статичные параметры из переменной

    for index, element in enumerate(main_list_variables):
        if element["group"] == "server":
            value += template_docker_compose_server(element["name"], element["port_server"], element["port_visor"])

    for index, element in enumerate(main_list_variables):
        if element["group"] == "transact":
            value += template_docker_compose_server(element["name"], element["port_server"], element["port_visor"])

    for index, element in enumerate(main_list_variables):
        if element["group"] == "exchange":
            value += template_docker_compose_server(element["name"], element["port_server"], element["port_visor"])

    file = open(f"{script_path}/{name}", "w")
    file.write(value)
    file.close()


def docker_compose_local():
    name = OUTPUT_DC_LOCAL
    print(f"-> {name}")
    value = value_dc_local  # берем статичные параметры из переменной

    for index, element in enumerate(main_list_variables):
        if element["group"] == "server":
            value += template_docker_compose_local_server(element["name"], element["port_server"], element["port_visor"])

    for index, element in enumerate(main_list_variables):
        if element["group"] == "transact":
            value += template_docker_compose_local_transact(element["name"], element["port_server"], element["port_visor"])

    for index, element in enumerate(main_list_variables):
        if element["group"] == "exchange":
            value += template_docker_compose_local_exchange(element["name"], element["port_server"], element["port_visor"])

    file = open(f"{script_path}/{name}", "w")
    file.write(value)
    file.close()


def env_common(): # общие параметры для всех проектов
    name = OUTPUT_ENV
    print(f"-> {name}")
    value = value_template_env  # берем статичные параметры из переменной

    #value = ""
    # Добавляем динамические
    value += "\n# Главный сервер"
    for nn in server:
        value += "\nSERVER_" + nn.upper() + '_ADDRESS=' + nn

    value += "\n\n# Криптовалюты"
    for nn in transact:
        value += "\nSERVER_" + nn.upper() + '_ADDRESS=' + nn

    value += "\n\n# Стаканы"
    for nn in exchange:
        value += "\nSERVER_" + nn.upper() + '_ADDRESS=' + nn

    file = open(f"{script_path}/{name}", "w")
    file.write(value)
    file.close()


def env_common_list_db():
    name = OUTPUT_DB_NAME_PORT_LIST_OFFICE
    print(f"-> {name}")

    value = f"""
DB_HOST = {DB_HOST}
DB_USER = {DB_USER}
DB_PASSWORD = {DB_PASSWORD}

DB_NAME:PORT
"""
    value += "\n# Главный сервер"
    for index, element in enumerate(main_list_variables):
        if element["group"] == "server":
            value += f'\n{element["name"]} : {element["port_db"]}'

    value += "\n\n# Криптовалюты"
    for index, element in enumerate(main_list_variables):
        if element["group"] == "transact":
            value += f'\n{element["name"]} : {element["port_db"]}'

    value += "\n\n# Стаканы"
    for index, element in enumerate(main_list_variables):
        if element["group"] == "exchange":
            value += f'\n{element["name"]} : {element["port_db"]}'

    file = open(f"{script_path}/{name}", "w")
    file.write(value)
    file.close()



def env_target(f_target_name, f_target_env, f_common_env, f_port, f_stand): # Зачищаем/обновляем ссылки на БД ENV
    lines_set = {""}

    # теги по которым будет делаться поиск и удалеине всей строки если найдет
    tag_list = {'# База', 'DB_USER', 'DB_FAMILY', 'DB_PASSWORD', 'DB_PORT', 'DB_HOST', 'DB_NAME=',
                '# Прослушивание уведомлений', 'POMM_DSN=pgsql://',
                'SERVER_SOCKET=',
                'SOCKET_SERVER=',
                'SERVER_WEBSOCKET_ADDRESS=',
                'SOCKET_HELPER_API_KEY='
                }

    # удаляем старый таргет БД из ENV
    for tag in tag_list:
        with open(f_target_env, "r+") as f:
            new_f = f.readlines()
            f.seek(0)
            for line in new_f:
                if tag not in line:
                    f.write(line)
            f.truncate()

    # пишем новый таргет БД
    #value = template_env_target(f_target_name, f_port)

    if f_stand == 'local' :
        user = DB_USER
        password = DB_PASSWORD
        host = DB_HOST
        name = f_target_name
        port = f_port

    if f_stand == 'office' :
        user = DB_USER
        password = DB_PASSWORD
        host = f"db_{f_target_name}"
        name = f_target_name
        port = 5432

    value = template_env_target(user, password, host, name, port) # шаблон
    with open(f_target_env, 'r+') as f:
        lines = f.readlines()
        f.seek(0)
        f.write(value)
        for line in lines:
            f.write(line)
        f.close()

    # Зачищаем повторы в таргете, из env_common
    with open(f_common_env, 'r') as f_env:
        for lines in f_env.read().splitlines():
            lines_set.add(lines)  # Получаем все значения в тип set, исключив повторы

        lines_set.remove("")  # удаляем пустоту из списка сравнения, для корректного сравнения и удаления

        # удаляем повторы
        for dell in lines_set:
            with open(f_target_env, "r+") as f:
                new_f = f.readlines()
                f.seek(0)
                for line in new_f:
                    if dell not in line:
                        f.write(line)
                f.truncate()


def env_rewrite(f_stand_p, f_stand_f):  # Обновляем статичный и динамический ENV в самом проекте general
    print(f"-> env_rewrite")
    common_env = f"{script_path}/general/.deploy/{OUTPUT_ENV}"

    shutil.copy2(f"{script_path}/{OUTPUT_ENV}", f"{script_path}/general/.deploy/{OUTPUT_ENV}")
    shutil.copy2(f"{script_path}/{OUTPUT_ENV}", f"{script_path}/transact/.deploy/{OUTPUT_ENV}")
    shutil.copy2(f"{script_path}/{OUTPUT_DC_LOCAL}", f"{script_path}/general/.deploy/{OUTPUT_DC_LOCAL}")
    shutil.copy2(f"{script_path}/{OUTPUT_DB_NAME_PORT_LIST_OFFICE}", f"{script_path}/general/.deploy/{OUTPUT_DB_NAME_PORT_LIST_OFFICE}")

    #################### server
    for index, element in enumerate(main_list_variables):
        if element["group"] == "server":
            target_name = element["name"]
            target_port = element["port_db"]
            target_env = f'{script_path}/general/{target_name}/.deploy/{f_stand_p}/.env.{f_stand_f}'

            # создаем конфиг
            env_target(target_name, target_env, common_env, target_port, f_stand_f)


    #################### exchange
    for index, element in enumerate(main_list_variables):
        if element["group"] == "exchange":
            target_name = element["name"]
            target_port = element["port_db"]
            target_env = f"{script_path}/general/exchange/.deploy/{f_stand_p}/{target_name}/.env.{f_stand_f}"
            common_env = f"{script_path}/general/.deploy/{OUTPUT_ENV}"
            target_path = f"{script_path}/general/exchange/.deploy/{f_stand_p}/{target_name}"

            # Если раздела нет, создаем его стартовый конфиг
            if not os.path.isdir(target_path):
                os.mkdir(target_path)

                if f_stand_f == 'local':
                    file = open(f"{target_path}/yii", "w")
                    file.write(template_yii)
                    file.close()

                    file = open(f"{target_path}/index.php", "w")
                    file.write(template_index)
                    file.close()

                if f_stand_f == 'office':
                    file = open(f"{target_path}/daemon.conf", "w")
                    file.write(" ")
                    file.close()

                    file = open(f"{target_path}/Dockerfile", "w")
                    file.write(template_dockerfile_exchange(target_name))
                    file.close()


                file = open(f"{target_path}/.env.{f_stand_f}", "w")
                file.write(template_exchange_env)
                file.close()

                template_server = template_server_local.replace("{server}", f"{target_name}")
                file = open(f"{target_path}/server.conf", "w")
                file.write(template_server)
                file.close()

            # создем единый силь конфигов для nginx
            if not os.path.exists(f"{target_path}/server.conf"):
                template_server = template_server_local.replace("{server}", f"{target_name}")
                file = open(f"{target_path}/server.conf", "w")
                file.write(template_server)
                file.close()

            # copy_out = f'{script_path}/general/exchange/.deploy/.local/{target_name}/.env.local'
            # copy_in =  f'{script_path}/general/exchange/.deploy/.local/{target_name}/.env_2.local'
            # shutil.copy2(copy_out, copy_in)
            # target_env = copy_in

            # создаем конфиг
            env_target(target_name, target_env, common_env, target_port, f_stand_f)



    #################### transact
    for index, element in enumerate(main_list_variables):
        if element["group"] == "transact":
            target_name = element["name"]
            target_port = element["port_db"]
            target_env = f'{script_path}/transact/.deploy/{f_stand_p}/{target_name}/.env.{f_stand_f}'
            common_env = f"{script_path}/transact/.deploy/{OUTPUT_ENV}"
            target_path = f'{script_path}/transact/.deploy/{f_stand_p}/{target_name}'


            # Если раздела нет, создаем его стартовый конфиг
            if not os.path.isdir(target_path):
                os.mkdir(target_path)

                if f_stand_f == 'local':
                    file = open(f"{target_path}/yii", "w")
                    file.write(template_yii)
                    file.close()

                    file = open(f"{target_path}/index.php", "w")
                    file.write(template_index)
                    file.close()

                if f_stand_f == 'office':
                    file = open(f"{target_path}/daemon.conf", "w")
                    file.write(" ")
                    file.close()

                    file = open(f"{target_path}/Dockerfile", "w")
                    file.write(template_dockerfile_transact(target_name))
                    file.close()

                file = open(f"{target_path}/.env.{f_stand_f}", "w")
                file.write(template_exchange_env)
                file.close()

                template_server = template_server_local.replace("{server}", f"{target_name}")
                file = open(f"{target_path}/server.conf", "w")
                file.write(template_server)
                file.close()

            # создем единый силь конфигов для nginx
            if not os.path.exists(f"{target_path}/server.conf"):
                template_server = template_server_local.replace("{server}", f"{target_name}")
                file = open(f"{target_path}/server.conf", "w")
                file.write(template_server)
                file.close()

            # copy_out = f'{script_path}/general/exchange/.deploy/.local/{target_name}/.env.local'
            # copy_in =  f'{script_path}/general/exchange/.deploy/.local/{target_name}/.env_2.local'
            # shutil.copy2(copy_out, copy_in)
            # target_env = copy_in

            # создаем конфиг
            env_target(target_name, target_env, common_env, target_port, f_stand_f)


def supervisor_monitor_conf(project):
    print(f"-> supervisor/supervisor.php")
    common_env = f"{script_path}/project/{project}/supervisor/supervisord-monitor/application/config/supervisor.php"
    value = template_supervisor_conf_header

    for index, element in enumerate(main_list_variables):
        if element["group"] == "server":
            value += template_supervisor_conf(element["name"])

    for index, element in enumerate(main_list_variables):
        if element["group"] == "transact":
            value += template_supervisor_conf(element["name"])

    for index, element in enumerate(main_list_variables):
        if element["group"] == "exchange":
            value += template_supervisor_conf(element["name"])

    value += template_supervisor_conf_footer

    file = open(common_env, "w")
    file.write(value)
    file.close()


def supervisor_nginx_conf(project):
    # берем готовый конфиг, отрезаем от него кусок начинабщийся на '####### Supervisor #######', переписываем новые зависимости
    print(f"-> nginx/sigen-proxy.conf")
    common_env = f"{script_path}/nginx/{project}/exc-supervisor.conf"

    sep = '####### Supervisor #######'
    file = open(common_env, "r")
    info = file.read().rstrip('\n')
    res = info.split(sep, 1)[0]

    value = sep
    for index, element in enumerate(main_list_variables):
        if element["group"] == "server":
            template_nginx = template_nginx_conf.replace("{f_name}", str(element["name"]))
            template_nginx = template_nginx.replace("{f_port_v}", str(element["port_visor"]))

            value += template_nginx

    for index, element in enumerate(main_list_variables):
        if element["group"] == "transact":
            template_nginx = template_nginx_conf.replace("{f_name}", str(element["name"]))
            template_nginx = template_nginx.replace("{f_port_v}", str(element["port_visor"]))
            value += template_nginx

    for index, element in enumerate(main_list_variables):
        if element["group"] == "exchange":
            template_nginx = template_nginx_conf.replace("{f_name}", str(element["name"]))
            template_nginx = template_nginx.replace("{f_port_v}", str(element["port_visor"]))
            value += template_nginx
    res += value
    res += "\n}"

    file = open(common_env, "w")
    file.write(res)
    file.close()


def git_commit_push(project):
    print("\nGit commit / push :")
    file_out = f"{script_path}/{OUTPUT_DC_SERVER}"  # "docker-compose-server.yml"
    file_in = f"{script_path}/project/{project}/{OUTPUT_DC_SERVER}"
    shutil.copy2(file_out, file_in)

    file_out = f"{script_path}/{OUTPUT_DC_DB}"  #  "docker-compose-db.yml"
    file_in = f"{script_path}/project/{project}/{OUTPUT_DC_DB}"
    shutil.copy2(file_out, file_in)

    os.chdir(f"{script_path}/project/{project}")
    os.system("git add .")
    os.system("git commit -m '[tech] script gen'")
    os.system("git push")

    os.chdir(f"{script_path}/nginx/{project}")
    os.system("git add .")
    os.system("git commit -m '[tech] script gen'")
    os.system("git push")

    os.chdir(f"{script_path}/transact")
    os.system("git add .")
    os.system("git commit -m '[tech] script gen'")
    os.system("git push")

    os.chdir(f"{script_path}/general")
    os.system("git add .")
    os.system("git commit -m '[tech] script gen'")
    os.system("git push")

