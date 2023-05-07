import requests
import json


class CTFdClient():
    def __init__(self, url, token):
        self.url = url
        self.token = token

    def get_challenges(self):
        return self.__get("challenges", {"view": "admin"})

    def create_challenge(self, name, value=1, type="standard", description=None, category=None, flag=None):
        payload = {
            "name": name,
            "type": type,
            "value": value,
            "category": category or ""
        }
        if description:
            payload["description"] = description

        return self.__post("challenges", payload)

    def update_challenge(self, id, name=None, value=None, type=None, description=None, category=None):
        payload = {
            "name": name,
            "type": type,
            "value": value,
            "description": description,
            "category": category or ""
        }

        # Using a for loop to remove keys with Value as None
        for key, value in dict(payload).items():
            if value is None:
                del payload[key]

        return self.__patch("challenges/{}".format(id), payload)

    def delete_challenge(self, id):
        return self.__delete("challenges/{}".format(id))

    def add_flag(self, challenge_id, flag, type="static"):
        payload = {
            "challenge_id": challenge_id,
            "content": flag,
            "type": type
        }
        return self.__post("flags", payload)

    def set_prerequisites(self, challenge_id, required_challenges_ids):
        payload = {
            "requirements": {
                "prerequisites": required_challenges_ids
            }
        }
        return self.__patch("challenges/{}".format(challenge_id), payload)

    def __get(self, path, params={}):
        return requests.get(
            "{}{}".format(self.url, path),
            params=params,
            headers=self.__headers()
        )

    def __delete(self, path):
        return requests.delete(
            "{}{}".format(self.url, path),
            headers=self.__headers()
        )

    def __post(self, path, payload):
        return requests.post(
            "{}{}".format(self.url, path),
            data=json.dumps(payload),
            headers=self.__headers()
        )

    def __patch(self, path, payload):
        return requests.patch(
            "{}{}".format(self.url, path),
            data=json.dumps(payload),
            headers=self.__headers()
        )

    def __headers(self):
        return {
            "Content-type": "application/json",
            "Authorization": "Token {}".format(self.token)
        }
