import requests, time

def dead_revive():
    print("Base — Dead Token Revive Detector (0 volume → sudden $50k+ in <5 min)")
    # pair → (time, volume_h24)
    graveyard = {}

    while True:
        try:
            r = requests.get("https://api.dexscreener.com/latest/dex/pairs/base")
            now = time.time()

            for pair in r.json().get("pairs", []):
                addr = pair["pairAddress"]
                vol = pair.get("volume", {}).get("h24", 0) or 0
                age = now - pair.get("pairCreatedAt", 0) / 1000

                if age < 300 or age > 86400: continue  # 5 min to 1 day old

                if addr not in graveyard:
                    graveyard[addr] = (now, vol)
                    continue

                last_t, last_vol = graveyard[addr]
                delta_t = now - last_t

                if last_vol < 1000 and vol > 50_000 and delta_t < 300:
                    token = pair["baseToken"]["symbol"]
                    print(f"DEAD TOKEN REVIVED\n"
                          f"{token} was silent — now ${vol:,.0f} volume\n"
                          f"Revival after {delta_t/60:.0f} min flatline\n"
                          f"https://dexscreener.com/base/{addr}\n"
                          f"→ Zombie pump incoming\n"
                          f"→ Either sniper resurrection or coordinated attack\n"
                          f"{'ZOMBIE'*25}")

                graveyard[addr] = (now, vol)

        except:
            pass
        time.sleep(6.1)

if __name__ == "__main__":
    dead_revive()
