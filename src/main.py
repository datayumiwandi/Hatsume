import requests
import random
import os

# URL sumber proxy
URL = "https://raw.githubusercontent.com/Mayumiwandi/Emilia/refs/heads/main/Data/alive.txt"

# Jumlah target proxy per country code
target_per_country = {
    "ID": 4,
    "SG": 3,
    "JP": 2,
    "US": 3,
}

# File output
output_path = "data/active.txt"
os.makedirs(os.path.dirname(output_path), exist_ok=True)

# Kata-kata blacklist (huruf kecil semua)
blacklist_words = {
    "pt", "lpp", "llc", "shpk", "ta", "city", "bv", "am", "retn",
    "company", "sm", "hk", "private", "customer", "ab", "limited", "a", "in", "169", "162"
}

# Fungsi membersihkan dan mengambil 2 kata bersih
def simplify_org(org):
    words = org.lower().split()
    filtered = [w for w in words if w not in blacklist_words]
    return ' '.join(filtered[:2]) if filtered else 'unknown'

# Ambil data proxy dari URL
response = requests.get(URL)
lines = response.text.strip().splitlines()

# Kelompokkan proxy berdasarkan negara
proxies_by_country = {}

for line in lines:
    parts = line.strip().split(',')
    if len(parts) == 4:
        ip, port, cc, org = parts
        if cc in target_per_country:
            org_clean = simplify_org(org)
            cleaned_line = f"{ip},{port},{cc},{org_clean}"
            proxies_by_country.setdefault(cc, []).append(cleaned_line)

# Pilih proxy acak
selected_proxies = []

for cc, count in target_per_country.items():
    proxies = proxies_by_country.get(cc, [])
    if len(proxies) >= count:
        selected_proxies.extend(random.sample(proxies, count))
    else:
        print(f"[⚠️] {cc}: hanya tersedia {len(proxies)} dari {count} yang diminta.")
        selected_proxies.extend(proxies)

# Simpan hasil
with open(output_path, "w") as f:
    for proxy in selected_proxies:
        f.write(proxy + "\n")

print(f"[✅] Total proxy disimpan: {len(selected_proxies)} ke '{output_path}'")
