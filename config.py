import os
import yaml


def load_config() -> dict:
    """loads all the .yaml settings files located in /settings and returns it to a variable"""
    config_data = {}

    for filename in sorted(os.listdir("./settings")):
        if filename.endswith(".yaml") or filename.endswith(".yml"):
            filepath = os.path.join("./settings", filename)
            with open(filepath, "r", encoding="utf-8") as file:
                data = yaml.safe_load(file) or {}
                config_data.update(data)

    return config_data


config = load_config()


def get_file_path(domain: str, name: str, config: dict = config) -> os.path:
    """returns the file path for a given domain and name"""
    base_path = config.get("data", {}).get("base_path", "./data")
    domain_info = config.get("data", {}).get(domain, {})
    if not domain_info:
        raise ValueError(f"domain '{domain}' not found in config.")
    file_info = domain_info.get(name)
    if not file_info:
        raise ValueError(f"Name '{name}' not found under domain '{domain}' in config.")
    file_name = file_info.get("file")
    if not file_name:
        raise ValueError(f"No file name specified for '{name}' in domain '{domain}'.")
    return os.path.join(base_path, domain, file_name)
