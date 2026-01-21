import subprocess
import requests
import whois

def run_ping(target):
    cmd = ["ping", "-n", "4", target]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.stdout


def run_dns(target):
    cmd = ["nslookup", target]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.stdout


def run_whois(target):
    try:
        data = whois.whois(target)

        output = ""
        for key, value in data.items():
            output += f"{key}: {value}\n"

        return output

    except Exception as e:
        return f"WHOIS error: {e}"


def run_headers(target):
    try:
        if not target.startswith("http"):
            target = "http://" + target
        r = requests.get(target, timeout=5)
        headers = ""
        for k, v in r.headers.items():
            headers += f"{k}: {v}\n"
        return headers
    except Exception as e:
        return str(e)
