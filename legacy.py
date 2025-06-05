import os
import json

# network.tf.json

ENV_DIR = "environments/legacy_env"
LEGACY_DIR = "legacy"
os.makedirs(ENV_DIR, exist_ok=True)
config_path = os.path.join (LEGACY_DIR, "config.cfg")

with open (config_path, "r", encoding="utf-8") as file:
    lines = file.readlines()

port = None
for line in lines:
    if line.startswith("PORT="):
        port = line.strip().split("=")[1]
        break

if port is None:
    raise ValueError("No se encontró el valor del puerto en el archivo de configuracion")

network_tfjson_file = {
    "variable": [  
        {
            "port": [
                {
                    "type": "string",
                    "default": port,
                    "description": "Puerto local de conexion"
                }
            ]
        }
    ] 

}

with open(os.path.join(ENV_DIR, "network.tf.json"), "w") as file:
    json.dump(network_tfjson_file, file, indent=4)

# main.tf.json
main_tfjson_file = {
    "resource": [
        {
            "null_resource": [ 
                {
                    "legacy_resource": [
                        {
                            "triggers": {
                                "port": "${var.port}"
                            },
                            "provisioner": [
                                {
                                    "local-exec": {
                                        "command": f"echo 'Arrancando ${{var.port}}'"
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

with open(os.path.join(ENV_DIR, "main.tf.json"), "w") as file:
    json.dump(main_tfjson_file, file, indent=4)