from db import db

def send_friend_request(from_user_id, to_user_id):
    query = (
        """
        MATCH (fromUser:User {user_id: $from_user_id}), (toUser:User {user_id: $to_user_id})
        MERGE (fromUser)-[r:FRIEND_REQUEST]->(toUser)
        RETURN r
        """
    )

    parameters = {
        "from_user_id": from_user_id,
        "to_user_id": to_user_id,
    }

    try:
        result = db.run_query(query, parameters)
        return result[0] if result else None
    except Exception as e:
        raise RuntimeError(f"Kunne ikke afsende anmodning: {str(e)}") from e

def accept_friend_request(from_user_id, to_user_id):
    query = (
        """
        MATCH (fromUser:User)-[r:FRIEND_REQUEST]->(toUser:User)
        WHERE fromUser.user_id = $from_user_id AND toUser.user_id = $to_user_id
        DELETE r
        CREATE (fromUser)-[:FRIENDS_WITH]->(toUser)
        RETURN fromUser, toUser
        """
    )

    parameters = {
        "from_user_id": from_user_id,
        "to_user_id": to_user_id,
    }

    try:
        result = db.run_query(query, parameters)
        return result[0] if result else None
    except Exception as e:
        raise RuntimeError(f"Kunne ikke afsende anmodning: {str(e)}") from e

def search_user(search_term):
    query = (
        """
        CALL db.index.fulltext.queryNodes("firstname_and_lastname", $search_term)
        YIELD node, score
        RETURN node.first_name AS firstName, node.last_name AS lastName, node.image_path AS imagePath, score
        ORDER BY score DESC
        """
    )
    # Get the most relevant/closer match of results by using score

    parameters = {
        "search_term": search_term
    }

    try:
        result = db.run_query(query, parameters)
        return result
    except Exception as e:
        raise RuntimeError(f"Kunne ikke afsende anmodning: {str(e)}") from e
