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


def join_challenges(user_id, challenge_id):
    try:
        query = (
            """
            MATCH (u:User {user_id: $user_id}), (c:Challenges {challenge_id: $challenge_id})
            MERGE (u)-[:JOINED]->(c)
            RETURN u, c
            """
        )
        parameters = {"user_id": user_id, "challenge_id": challenge_id}
        db.run_query(query, parameters)

        return True

    except Exception as e:
        print(f"Error joining challenge: {str(e)}")
        return False


def check_if_joined(user_id, challenge_id):
    try:
        query = (
            """
            MATCH (u:User {user_id: $user_id})-[:JOINED]->(c:Challenges {challenge_id: $challenge_id})
            RETURN COUNT(*) AS count
            """
        )
        parameters = {"user_id": user_id, "challenge_id": challenge_id}
        result = db.run_query(query, parameters)

        if result:
            return result[0]["count"] > 0
        else:
            return False

    except Exception as e:
        print(f"Error checking if user joined challenge: {str(e)}")
        return False
