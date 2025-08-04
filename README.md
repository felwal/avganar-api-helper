# Avgånär API helper

SL discontinued their [Nearby Stops 2](https://github.com/trafiklab/trafiklab.se/blob/development/content/api/our-apis/sl/nearby-stops-2.md) API, central to [Avgånär](https://github.com/felwal/avganar), without providing a replacement. The purpose of this static API is only to fill this need.

Use [ResRobot 2.1 Nearby Stops](https://www.trafiklab.se/api/our-apis/resrobot-v21/nearby-stops) to get `national_id` ("rikshållplats"), then transform to SL "site id":

`api.avganar.felixwallin.se/sl-national-stops/<national_id>.json`

Example response:

```json
{
  "national_id": 740021013,
  "site_id": 9117
}
```

The data is combined from [SL Transport](https://www.trafiklab.se/api/our-apis/sl/transport) sites and [GTFS Sverige 2](https://www.trafiklab.se/api/gtfs-datasets/gtfs-sverige-2) agency stops.
