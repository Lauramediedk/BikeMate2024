from db import db


def get_user_invites(user_id):
    query = (
        """
        MATCH (admin:User)-[:SENT_INVITE]->(e:Event)<-[:PENDING_INVITE]-(u:User {user_id: $user_id})
        RETURN e.event_id AS event_id, e.title AS event_name,
        admin.user_id AS admin_id, admin.first_name AS first_name, admin.last_name AS last_name
        """
    )

    parameters = {
        "user_id": user_id,
    }

    try:
        result = db.run_query(query, parameters)
        print(result)  # Tilføj denne linje for at inspicere resultaterne
        invitations = []
        for record in result:
            if 'first_name' in record and 'last_name' in record:
                full_name = f"{record['first_name']} {record['last_name']}"
                invitations.append({
                    'event_id': record['event_id'],
                    'event_name': record['event_name'],
                    'full_name': full_name,
                })
        return invitations
    except Exception as e:
        raise RuntimeError(f"Error retrieving invitations: {str(e)}") from e
