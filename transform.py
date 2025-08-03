import json

stops = dict()

with open("data/gtfs-sverige2-agency-stops.txt", "r") as file:
    lines = file.readlines()

    for i, line in enumerate(lines):
        if i == 0: continue

        values = line.split(",")
        national_id = values[1].strip()
        sl_area_id = int(values[2].strip())

        if not national_id in stops: stops[national_id] = sl_area_id

with open("docs/sl-sites-test.json", "w") as file:
    file.write(json.dumps(stops, indent=2))
    pass
