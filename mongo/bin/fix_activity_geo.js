db = db.getSiblingDB('strava')

// a "LineString" element needs > 1 coordinate pair to be valid
// if we have == 1, just double it so it's two identical points
db.activity.updateMany( {"path.coordinates": {"$size": 1}},
  [
    {"$set": {
        "path.coordinates": {
          // just "fake" a second point to make len > 1
          "$concatArrays": ["$path.coordinates", "$path.coordinates"]
        }
      }
    }
  ]
)

// if we have zero points.. just set the whole field to null
db.activity.updateMany( {"path.coordinates": {"$size": 0}},
  [
    {"$set":
      {
      "path": null
      }
    }
  ]
)
