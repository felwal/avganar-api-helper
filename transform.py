import json

national_ids_by_area_id = dict()

# link national id -> sl area id
with open("data/gtfs-sverige2-agency-stops.txt", "r", encoding="utf-8") as file:
    lines = file.readlines()
    national_sites_with_duplicate_sl_area_id = 0

    for i, line in enumerate(lines):
        if i == 0: continue # skip header

        values = line.split(",")
        national_id = values[1].strip()
        area_id = int(values[2].strip())

        if area_id not in national_ids_by_area_id:
            national_ids_by_area_id[area_id] = national_id
        else:
            #print("national sites", national_id, national_ids_by_area_id[area_id], "have same sl area id", area_id)
            national_sites_with_duplicate_sl_area_id += 1
            pass

    print("national sites:", len(lines) - 1)
    print("national sites with duplicate sl area id:", national_sites_with_duplicate_sl_area_id)

stops_by_national_id = dict()

# link sl area id -> sl site id
with open("data/sl-transport-sites.json", "r", encoding="utf-8") as file:
    sites = json.load(file)
    sl_sites_with_duplicate_national_id = 0
    sl_sites_without_national_id = 0

    for site in sites:
        national_id = -1

        # get the shortest name
        name = site["name"]
        if "alias" in site:
            for alias in site["alias"]:
                if len(alias) < len(name):
                    name = alias

        previous_national_ids = []
        site_ids_already_linked = []

        for area_id in site["stop_areas"]:
            # skip if its not connected to any national id
            if area_id not in national_ids_by_area_id: continue

            national_id = national_ids_by_area_id[area_id]

            if national_id not in stops_by_national_id or stops_by_national_id[national_id]["site_id"] in site_ids_already_linked:
                # if the site occupying this national id is already linked to another national id, override it
                stops_by_national_id[national_id] = {"site_id": site["id"], "name": name}
            else:
                site_ids_already_linked.append(stops_by_national_id[national_id]["site_id"])
                #print("sl sites", site["id"], stops_by_national_id[national_id], "have same national id", national_id)
                sl_sites_with_duplicate_national_id += 1

        if national_id == -1:
            #print("sl site", site["id"], "lacks national id")
            sl_sites_without_national_id += 1
            continue

    print("sl sites:", len(sites))
    print("sl sites with duplicate national id:", sl_sites_with_duplicate_national_id)
    print("sl sites without national id:", sl_sites_without_national_id)
    print("national sites with sl site id:", len(stops_by_national_id))


for national_id, stop in stops_by_national_id.items():
    with open(f"docs/sl-national-stops/{national_id}.json", "w", encoding="utf-8") as file:
        file.write(json.dumps(stop, indent=2, ensure_ascii=False))

with open("docs/sl-national-stops.json", "w", encoding="utf-8") as file:
    file.write(json.dumps(stops_by_national_id, indent=2, ensure_ascii=False))
