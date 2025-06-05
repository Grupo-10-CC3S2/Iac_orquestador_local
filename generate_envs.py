import os, json
from shutil import copyfile


MODULE_DIR = "modules/simulated_app"
OUT_DIR    = "environments"

def render_and_write(env):
    env_dir = os.path.join(OUT_DIR, env["name"])
    os.makedirs(env_dir, exist_ok=True)

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
                        env["name"]: [
                            {
                                "triggers": {
                                    "name":    env["name"],
                                    "network": "${var.network}"
                                },
                                "provisioner": [
                                    {
                                        "local-exec": {
                                            "command": (
                                                f"echo 'Arrancando servidor {env['name']}"
                                                " en red ${var.network}'"
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

if __name__ == "__main__":
    """
    # Limpia entornos viejos (si quieres)
    if os.path.isdir(OUT_DIR):
        import shutil
        shutil.rmtree(OUT_DIR)
    """

    # Ejercicio 1: El unico directorio en donde se aplican los cambios
    ENVS = [{"name": "app1"}]
    for env in ENVS:
        render_and_write(env)
    print(f"Generados {len(ENVS)} entornos en '{OUT_DIR}/'")