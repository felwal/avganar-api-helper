import json

national_ids_by_area_id = dict()

# link national id -> sl area id
with open("data/gtfs-sverige2-agency-stops.txt", "r") as file:
    lines = file.readlines()
    national_sites_with_duplicate_sl_area_id = 0

    for i, line in enumerate(lines):
        if i == 0: continue # skip header

        values = line.split(",")
        national_id = values[1].strip()
        area_id = int(values[2].strip())

        if not area_id in national_ids_by_area_id:
            national_ids_by_area_id[area_id] = national_id
        else:
            #print("national sites", national_id, national_ids_by_area_id[area_id], "have same sl area id", area_id)
            national_sites_with_duplicate_sl_area_id += 1
            pass

    print("national sites:", len(lines) - 1)
    print("national sites with duplicate sl area id:", national_sites_with_duplicate_sl_area_id)

site_ids_by_national_id = dict()

# link sl area id -> sl site id
with open("data/sl-transport-sites.json", "r", encoding="utf-8") as file:
    sites = json.load(file)
    sl_sites_with_duplicate_national_id = 0
    sl_sites_without_national_id = 0

    for site in sites:
        national_id = -1

        for area_id in site["stop_areas"]:
            if not area_id in national_ids_by_area_id: continue

            national_id = national_ids_by_area_id[area_id]

            if not national_id in site_ids_by_national_id:
                site_ids_by_national_id[national_id] = site["id"]
            else:
                #print("sl sites", site["id"], stops_by_national_id[national_id], "have same national id", national_id)
                sl_sites_with_duplicate_national_id += 1
                pass

        if national_id == -1:
            #print("sl site", site["id"], "lacks national id")
            sl_sites_without_national_id += 1
            continue

    print("sl sites:", len(sites))
    print("sl sites with duplicate national id:", sl_sites_with_duplicate_national_id)
    print("sl sites without national id:", sl_sites_without_national_id)
    print("national sites with sl site id:", len(site_ids_by_national_id))

stops = []

for national_id, site_id in site_ids_by_national_id.items():
    stop = {"national_id": national_id, "site_id": site_id}
    stops.append(stop)

    with open(f"docs/sl-national-stops/{national_id}.json", "w", encoding="utf-8") as file:
        file.write(json.dumps(stop, indent=2))

with open("docs/sl-national-stops.json", "w", encoding="utf-8") as file:
    file.write(json.dumps(stops, indent=2))
