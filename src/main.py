import requests
import random
import os

# URL sumber data proxy
URL = "https://raw.githubusercontent.com/Mayumiwandi/Emilia/refs/heads/main/Data/alive.txt"

# Jumlah target proxy per country code
target_per_country = {
    "ID": 4,
    "SG": 3,
    "JP": 2,
    "US": 3,
}

# Path output (untuk GitHub Actions)
output_path = "data/active.txt"

# Pastikan folder 'data' ada
os.makedirs(os.path.dirname(output_path), exist_ok=True)

# Ambil data proxy dari URL
response = requests.get(URL)
lines = response.text.strip().splitlines()

# Kelompokkan proxy berdasarkan country code
proxies_by_country = {}

for line in lines:
    parts = line.strip().split(',')
    if len(parts) == 4:
        ip, port, cc, org = parts
        if cc in target_per_country:
            proxies_by_country.setdefault(cc, []).append(line)

# Ambil proxy secara acak sesuai jumlah target
selected_proxies = []

for cc, count in target_per_country.items():
    proxies = proxies_by_country.get(cc, [])
    if len(proxies) >= count:
        selected_proxies.extend(random.sample(proxies, count))
    else:
        print(f"[⚠️] {cc}: hanya tersedia {len(proxies)} dari {count} yang diminta.")
        selected_proxies.extend(proxies)

# Simpan ke file output
with open(output_path, "w") as f:
    for proxy in selected_proxies:
        f.write(proxy + "\n")

print(f"[✅] Total proxy disimpan: {len(selected_proxies)} ke '{output_path}'")
