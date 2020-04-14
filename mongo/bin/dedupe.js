db = db.getSiblingDB('strava')

db.activity.aggregate(
  {
    "$group" :
    {
      "_id":
      {
        "$toInt": "$activity_id"
      },
      "count": { "$sum": 1 }
    }
  },
  {
    "$match":
    {
      "_id" :{ "$ne" : null } ,
      "count" : {"$gt": 1}
    }
  },
  // this next step is unnecessary (just adds a forEach) but was helpful
  // in debugging so whatever, deal with it
  {
    "$group" :
    {
      "_id": null,
      "duplicates": { "$addToSet": "$_id" }
    }
  }
).forEach(function(doc) {
  doc.duplicates.forEach(function(act_id) {
    db.activity.deleteOne({"activity_id": act_id});
  });
});
