cat db.json | '.[] .drugs' > drugs
awk '!a[$0]++' drugs > drugs