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
    "US": 2,
    "MY": 1,
}

# Output path
output_path = "data/active.txt"
os.makedirs(os.path.dirname(output_path), exist_ok=True)

# Kata blacklist
blacklist_words = {
    "pt", "lpp", "llc", "shpk", "ta", "city", "bv", "am", "retn",
    "company", "sm", "hk", "private", "customer", "ab", "limited", "a", "in", "169", "162"
}

# Fungsi membersihkan org dan ambil 2 kata saja
def simplify_org(org):
    words = org.lower().split()
    filtered = [w for w in words if w not in blacklist_words]
    return ' '.join(filtered[:2]) if filtered else 'unknown'

# Ambil data dari URL
response = requests.get(URL)
lines = response.text.strip().splitlines()

proxies_by_country = {}

for line in lines:
    parts = line.strip().split(',')
    if len(parts) == 4:
        ip, port, cc, org = parts
        if cc in target_per_country:
            org_clean = simplify_org(org)
            proxies_by_country.setdefault(cc, []).append((ip, port, cc, org_clean))

# Pilih proxy acak dan beri nomor duplikat
selected_proxies = []
org_counter = {}

for cc, count in target_per_country.items():
    proxies = proxies_by_country.get(cc, [])
    if len(proxies) >= count:
        picked = random.sample(proxies, count)
    else:
        print(f"[⚠️] {cc}: hanya tersedia {len(proxies)} dari {count} yang diminta.")
        picked = proxies

    for ip, port, cc, org in picked:
        # Tambahkan angka jika nama org sudah pernah muncul
        org_counter[org] = org_counter.get(org, 0) + 1
        final_org = f"{org} {org_counter[org]}" if org_counter[org] > 1 else org
        selected_proxies.append(f"{ip},{port},{cc},{final_org}")

# Simpan hasil
with open(output_path, "w") as f:
    for proxy in selected_proxies:
        f.write(proxy + "\n")

print(f"[✅] Total proxy disimpan: {len(selected_proxies)} ke '{output_path}'")
