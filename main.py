from variables import *
from input import *


########################################
print("")
print(f"count {len(server)}:  {server}")
print(f"count {len(transact)}: {transact}")
print(f"count {len(exchange)}: {exchange}")

print("\ngit_clone: run")
git_clone_sigen()
print("git_clone: stop")


########################################
print("\nStart Build file:")
env_common()
env_common_list_db()
docker_compose_db()
docker_compose_server()
docker_compose_local()
env_rewrite(".local", "local")
env_rewrite("office", "office")
supervisor_monitor_conf("exc")
supervisor_nginx_conf("exc")


########################################
git_commit_push("exc")
