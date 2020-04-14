db = db.getSiblingDB('strava')
db.users.updateMany( {},
	[
		{"$set": {
			user_id: {"$toInt": "$user_id"},
			num_following: {"$toInt": "$num_following"},
			num_followers: {"$toInt": "$num_followers"}
		}},
		{"$unset": "user_url"}
	]
)
