import yaml
from loguru import logger

from db.mongo import MongoDB


def seed_configs():
    mongo = MongoDB()
    release_admins_team = mongo.db['teams'].find_one({'name': 'release_admins'})
    if release_admins_team is not None and len(release_admins_team['members']) > 0:
        logger.success("already seed...")
        exit(0)

    with open("seed.yml", "r") as file:
        data = yaml.safe_load(file)

    telegram_users = data['tapsi']['telegram']['users']
    teams = data['tapsi']['teams']

    try:
        telegram_users_list = [
            {"name": name, "telegram_id": value['telegram_id'], "username": value['telegram_username']}
            for name, value in telegram_users.items()
        ]
        teams_list = [
            {
                "name": name,
                "members": [
                    {
                        "name": x,
                        "telegram_id": telegram_users[x]['telegram_id'],
                        "username": telegram_users[x]['telegram_username']
                    } for x in members]
            }
            for name, members in teams.items()
        ]
    except Exception as ex:
        logger.error(f"wrong config file, follow readme.md \n{ex}")
        exit(1)

    mongo.db.telegram_users.insert_many(telegram_users_list)
    mongo.db.teams.insert_many(teams_list)

    logger.success(f"After insert: telegram user count: {mongo.db.telegram_users.count_documents({})}")
    logger.success(f"After insert: team count: {mongo.db.teams.count_documents({})}")


if __name__ == "__main__":
    seed_configs()
