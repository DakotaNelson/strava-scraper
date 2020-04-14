db = db.getSiblingDB('strava')

// this is a two-stage pipeline since it's more complex and losing data would
// be a real bad time - so it goes through and fixes the geo-data initially,
// then once confirmed correct you can delete the old field

db.activity.updateMany( {},
  [
    {"$set": {
      activity_id: {"$toInt": "$activity_id"},
      athlete_id: {"$toInt": "$athlete_id"},
      // this is a new field
      path: {
        type: "LineString",
        // the coordinates went in as lat,lng and need to be lng,lat
        coordinates: {"$map": {
          "input": "$latlng",
          "in": {"$reverseArray": "$$this"}}
        }
      }
      // if setting the "path" field works, later go through and remove the
      // latlng field - it'll be obsolete
    }},
    {"$unset": ["url", "latlng_url"]}
  ]
)

// db.activity.updateMany( {},
//   [
//     {"$unset": "latlng"}
//   ]
// )
