from db import db

def check_friendship(from_user_id, to_user_id):
    query = (
        """
        MATCH (fromUser:User {user_id: $from_user_id})-[r:FRIENDS_WITH]-(toUser:User {user_id: $to_user_id})
        RETURN EXISTS((fromUser)-[r]-()) AS isFriend
        """
    )

    parameters = {
        "from_user_id": from_user_id,
        "to_user_id": to_user_id,
    }

    try:
        result = db.run_query(query, parameters)
        return result[0]['isFriend'] if result else False
    except Exception as e:
        raise RuntimeError(f"Kunne ikke tjekke venskabsstatus: {str(e)}") from e

def get_friends(user_id):
    query = (
        """
        MATCH (u:User {user_id: $user_id})-[r:FRIENDS_WITH]-(friend:User)
        RETURN friend.user_id AS userId,
        friend.first_name AS fName,
        friend.last_name AS lName,
        friend.image_path AS profileImage
        """
    )

    parameters = {
        "user_id": user_id,
    }

    try:
        result = db.run_query(query, parameters)
        return [record for record in result] if result else None
    except Exception as e:
        raise RuntimeError(f"Kunne ikke hente venneliste: {str(e)}") from e

def get_recommended_friends(user_id):
    # We make sure to not show the recommended users if there is a relation
    query = (
        """
        MATCH (u:User {user_id: $user_id})-[:FRIENDS_WITH]-(common_friend)-[:FRIENDS_WITH]-(recommended_user)
        WHERE NOT (u)-[:FRIENDS_WITH]-(recommended_user)
        AND u.user_id <> recommended_user.user_id
        AND NOT (u)-[:FRIEND_REQUEST]-(recommended_user)
        RETURN recommended_user.user_id AS userId,
            recommended_user.first_name AS firstName,
            recommended_user.last_name AS lastName,
            recommended_user.image_path AS imagePath
        """
    )

    parameters = {
        "user_id": user_id,
    }

    try:
        result = db.run_query(query, parameters)
        return [record for record in result] if result else []
    except Exception as e:
        raise RuntimeError(f"Could not fetch recommended friends: {str(e)}") from e

def view_profile(user_id, logged_in_user):
    query = (
        """
        MATCH (u:User {user_id: $user_id})
        OPTIONAL MATCH (loggedIn:User {user_id: $logged_in_user})
        OPTIONAL MATCH (u)-[:FRIENDS_WITH]-(friend:User)
        OPTIONAL MATCH (u)-[:JOINED]->(event:Event)
        RETURN u.user_id AS userId,
            u.first_name AS firstName,
            u.last_name AS lastName,
            u.image_path AS imagePath,
            u.bio AS bio,
            COLLECT(DISTINCT {
            userId: friend.user_id,
            firstName: friend.first_name,
            lastName: friend.last_name,
            imagePath: friend.image_path
            }) as friends,
            COLLECT(DISTINCT event) AS events,
            EXISTS((loggedIn)-[:FRIEND_REQUEST]->(u)) AS requestSent,
            EXISTS((loggedIn)-[:FRIENDS_WITH]-(u)) AS isFriend
        """
    )

    parameters = {
        "user_id": user_id,
        "logged_in_user": logged_in_user,
    }

    try:
        result = db.run_query(query, parameters)
        return result[0] if result else None
    except Exception as e:
        raise RuntimeError(f"Kunne ikke gå til brugerens dashboard: {str(e)}") from e

def delete_friendship(from_user_id, to_user_id):
    query = (
        """
        MATCH (fromUser:User)-[r:FRIENDS_WITH]-(toUser:User)
        WHERE fromUser.user_id = $from_user_id AND toUser.user_id = $to_user_id
        DELETE r
        RETURN fromUser, toUser
        """
    )

    parameters = {
        "from_user_id": from_user_id,
        "to_user_id": to_user_id,
    }

    try:
        db.run_query(query, parameters)
        return True
    except Exception as e:
        raise RuntimeError(f"Kunne ikke slette anmodningen: {str(e)}") from e

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

def get_friend_requests(to_user_id):
    query = (
        """
        MATCH (fromUser:User)-[r:FRIEND_REQUEST]->(toUser:User {user_id: $to_user_id})
        RETURN fromUser.user_id AS fromUserId, fromUser.first_name AS firstName,
        fromUser.last_name AS lastName,
        fromUser.image_path AS imagePath
        """
    )

    parameters = {
        "to_user_id": to_user_id,
    }

    try:
        result = db.run_query(query, parameters)
        return result
    except Exception as e:
        raise RuntimeError(f"Kunne ikke henter anmodninger: {str(e)}") from e

def accept_friend_request(from_user_id, to_user_id):
    query = (
        """
        MATCH (fromUser:User)-[r:FRIEND_REQUEST]->(toUser:User)
        WHERE fromUser.user_id = $from_user_id AND toUser.user_id = $to_user_id
        DELETE r
        MERGE (fromUser)-[:FRIENDS_WITH]-(toUser)
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

def delete_friend_request(from_user_id, to_user_id):
    query = (
        """
        MATCH (fromUser:User)-[r:FRIEND_REQUEST]->(toUser:User)
        WHERE fromUser.user_id = $from_user_id
        DELETE r
        RETURN fromUser, toUser
        """
    )

    parameters = {
        "from_user_id": from_user_id,
        "to_user_id": to_user_id,
    }

    try:
        db.run_query(query, parameters)
        return True
    except Exception as e:
        raise RuntimeError(f"Kunne ikke slette anmodningen: {str(e)}") from e

def search_user(search_term, user_id):
    query = (
        """
        CALL db.index.fulltext.queryNodes("firstname_and_lastname", $search_term)
        YIELD node, score
        MATCH (loggedIn:User {user_id: $user_id})
        WHERE NOT node.user_id = $user_id
        WITH node, score, loggedIn
        RETURN
            node.user_id AS userId,
            node.first_name AS firstName,
            node.last_name AS lastName,
            node.image_path AS imagePath,
            score,
            EXISTS((loggedIn)-[:FRIEND_REQUEST]->(node)) AS requestSent,
            EXISTS((loggedIn)-[:FRIENDS_WITH]-(node)) AS isFriend
        ORDER BY score DESC
        """
    )
    parameters = {
        "search_term": search_term,
        "user_id": user_id,
    }

    try:
        result = db.run_query(query, parameters)
        return result
    except Exception as e:
        raise RuntimeError(f"Kunne ikke afsende anmodning: {str(e)}") from e
