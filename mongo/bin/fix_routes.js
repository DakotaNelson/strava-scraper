db = db.getSiblingDB('strava')
db.routes.updateMany( {},
	[
		{"$set": {route_id: {"$toInt": "$route_id"}}}
	]
)
