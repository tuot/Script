import re
from pathlib import Path

import fire
import requests

BLOCK_DOMAIN = "https://anti-ad.net/domains.txt"


def is_ip(ip_str):
    pattern = re.compile(
        r'^((25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(25[0-5]|2[0-4]\d|[01]?\d\d?)$')
    if pattern.match(ip_str):
        return True
    else:
        return False


def get_ad_domain():
    response = requests.request("GET", BLOCK_DOMAIN)
    return response.text.split("\n")


def get_block_domain(log_path):
    result = {}
    ad_domain_list = get_ad_domain()
    try:
        log_path = Path(log_path)
        with log_path.open("r", encoding='utf-8') as f:
            for line in f:
                if line and "error" not in line and " - " in line:
                    app_name = line.split(" - ")[0].strip().split(" ")[2]
                    domain_pre = line.split(" - ")[1].strip()
                    domain = domain_pre.split(" ")[0].split(":")[0]
                    if "(" in domain:
                        domain = domain[:domain.index("(")]
                    if is_ip(domain):
                        continue
                    if domain in ad_domain_list:
                        if domain in result:
                            result[domain].append(app_name)
                        else:
                            result[domain] = [app_name]
    except Exception as err:
        print(err)

    for k, value in result.items():
        result[k] = list(set(value))
    print(len(result.keys()), ";".join(result.keys()))
    return result


if __name__ == '__main__':
    fire.Fire()
