import os, json
from shutil import copyfile
import subprocess
import click

MODULE_DIR = "modules/simulated_app"
OUT_DIR    = "environments"

def render_and_write(env, port):
    env_dir = os.path.join(OUT_DIR, env["name"])
    os.makedirs(env_dir, exist_ok=True)

    """
    api_key = os.environ.get("API_KEY")
    if not api_key:
        raise Exception("La variable de entorno API_KEY no está definida.")
    
    os.environ["TF_VAR_api_key"] = api_key

    subprocess.run(["terraform", "apply"], cwd="environments/app1")
    """

    # 1) Copia la definición de variables (network.tf.json)
    copyfile(
        os.path.join(MODULE_DIR, "network.tf.json"),
        os.path.join(env_dir, "network.tf.json")
    )

    # 2) Genera main.tf.json SÓLO con recursos
    config = {
        "resource": [
            {
                "null_resource": [
                    {
                        "local_server": [
                            {
                                "triggers": {
                                    "name":    env["name"],
                                    "network": env['network']
                                },
                                "provisioner": [
                                    {
                                        "local-exec": {
                                            "command": (
                                                f"echo 'Arrancando servidor {env['name']} en red {env['network']}"
                                                " en el puerto ${var.port}'"
                                            )
                                        }
                                    }
                                ]
                            }
                        ]
                    }
                ]
            }
        ]
    }

    with open(os.path.join(env_dir, "main.tf.json"), "w") as fp:
        json.dump(config, fp, sort_keys=True, indent=4)
        
# Ejercicio 2: 
@click.command()
@click.option('--count', default=1, help='cantidad de entornos que se van a generar')
@click.option('--prefix', default='app', help='prefijo para el nombre de los entornos')
@click.option('--port', default=3000, help='puerto de los servidores')
def main(count, prefix, port):
    # limpiamos los entornos viejos
    if os.path.isdir(OUT_DIR):
        import shutil
        shutil.rmtree(OUT_DIR)
    click.echo(f"se eliminaron los entornos viejos")
    # creamos los nuevos entornos    
    os.makedirs(OUT_DIR, exist_ok=True)
    envs = []
    for i in range(1, count + 1):
        envs.append({
            "name": f"{prefix}{i}",
            "network": f"net{i}"
        })

    for env in envs:
        render_and_write(env, port)

    click.echo(f"se generaron {count} entornos en '{OUT_DIR}/'")

if __name__ == "__main__":
    main()
    
    """
    # Limpia entornos viejos (si quieres)
    if os.path.isdir(OUT_DIR):
        import shutil
        shutil.rmtree(OUT_DIR)
    

    # Ejercicio 1: El unico directorio en donde se aplican los cambios
    ENVS = [
        {"name": "env2", "network": "net2"},
        {"name": "env3", "network": "net2-peered"}       
    ]
    for env in ENVS:
        render_and_write(env)
    print(f"Generados {len(ENVS)} entornos en '{OUT_DIR}/'")    
    """
    
