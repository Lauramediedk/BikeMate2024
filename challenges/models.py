from db import db

def get_challenges():
        try:
            challenges = []
            query = "MATCH (c:Challenges) RETURN c"

            result = db.run_query(query)

            for record in result:
                challenges.append(record['c'])

            return challenges

        except Exception as e:
            print(f"Could not get challenges: {str(e)}")
            return None

