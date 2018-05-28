# should probably do this using a js script but long live bash

mongo strava --eval 'db.createCollection("sitemap")'
mongo strava --eval 'db.activity.createIndex( { "url": 1 }, { unique: true } )'

mongo strava --eval 'db.createCollection("activity")'
mongo strava --eval 'db.activity.createIndex( { "activity_id": 1 }, { unique: true } )'

mongo strava --eval 'db.createCollection("clubs")'
mongo strava --eval 'db.clubs.createIndex( { "club_id": 1 }, { unique: true } )'

mongo strava --eval 'db.createCollection("routes")'
mongo strava --eval 'db.routes.createIndex( { "route_id": 1 }, { unique: true } )'

mongo strava --eval 'db.createCollection("segments")'
mongo strava --eval 'db.segments.createIndex( { "segment_id": 1 }, { unique: true } )'

mongo strava --eval 'db.createCollection("users")'
mongo strava --eval 'db.users.createIndex( { "user_id": 1 }, { unique: true } )'
