from db import db

def get_challenges():
        query = "MATCH (c:Challenges) RETURN c"

        result = db.run_query(query)

        if result:
            return result
        else:
            print("No challenges found")
            return None