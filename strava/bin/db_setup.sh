# should probably do this using a js script but long live bash

mongo --eval 'use strava-new'

mongo --eval 'db.createCollection("activity")'
mongo --eval 'db.activity.createIndex( { "activity_id": 1 }, { unique: true } )'

mongo --eval 'db.createCollection("clubs")'
mongo --eval 'db.clubs.createIndex( { "club_id": 1 }, { unique: true } )'

mongo --eval 'db.createCollection("routes")'
mongo --eval 'db.routes.createIndex( { "route_id": 1 }, { unique: true } )'

mongo --eval 'db.createCollection("segments")'
mongo --eval 'db.segments.createIndex( { "segment_id": 1 }, { unique: true } )'

mongo --eval 'db.createCollection("users")'
mongo --eval 'db.users.createIndex( { "user_id": 1 }, { unique: true } )'
