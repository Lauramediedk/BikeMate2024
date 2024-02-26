from db import db


def upload_profile_image(user_id, new_image_path):
    query = (
        """
        MATCH (user:User {user_id: $user_id})
        SET user.image_path = $image_path
        """
    )
    parameters = {
        "user_id": user_id,
        "image_path": new_image_path,
    }

    try:
        db.run_query(query, parameters)
    except Exception as e:
        raise RuntimeError(f"Fejl ved upload af billede: {str(e)}") from e


def get_profile_image(user_id):
    query = (
        """
        MATCH (user:User {user_id: $user_id})
        RETURN user.image_path as image_path
        """
    )
    parameters = {
        "user_id": user_id,
    }

    result = db.run_query(query, parameters)

    # Hent alle records fra resultatet
    records = list(result)

    # Hent image_path fra det første resultat, eller returner None, hvis der ikke er nogen data
    image_path = records[0]["image_path"] if records else None
    return image_path


def remove_profile_image(user_id):
    query = (
        """
        MATCH (user:User {user_id: $user_id})
        REMOVE user.image_path
        """
    )
    parameters = {
        "user_id": user_id
    }

    try:
        db.run_query(query, parameters)
    except Exception as e:
        raise RuntimeError(f"Kunne ikke fjerne billede: {str(e)}") from e


def upload_user_bio(user_id, bio):
    query = (
        """
        MATCH (user:User {user_id: $user_id})
        SET user.bio = $bio
        """
    )
    parameters = {
        "user_id": user_id,
        "bio": bio,
    }

    try:
        db.run_query(query, parameters)
    except Exception as e:
        raise RuntimeError(f"Fejl ved upload af billede: {str(e)}") from e


def get_user_bio(user_id):
    query = (
        """
        MATCH (user:User {user_id: $user_id})
        RETURN user.bio as bio
        """
    )
    parameters = {
        "user_id": user_id,
    }

    result = db.run_query(query, parameters)

    records = list(result)

    bio = records[0]["bio"] if records else None
    return bio
