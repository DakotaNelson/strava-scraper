db = db.getSiblingDB('strava')

db.clubs.updateMany( {},
  [
    {
      "$set": {
        club_id: {"$toInt": "$club_id"},
        club_num_members: {"$toInt": "$club_num_members"},
        club_members: {
          "$map": {
            "input": "$club_members",
            "in": {"$convert":
              {
                input: "$$this",
                to: "int",
                onError: "$$this"
                // some usernames are actual names (for "pro" users), but
                // most are integer user IDs
              }
            }
          }
        }
      }
    }
  ]
)
