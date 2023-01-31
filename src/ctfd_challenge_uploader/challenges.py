from dotenv import load_dotenv
import os
from ctfd_client import CTFdClient


class Challenges:

    CHALLENGE_PREFIX = "Challenge name:"
    DESCRIPTION_PREFIX = "Description:"
    CATEGORY_PREFIX = "Category:"
    FLAG_PREFIX = "Flag:"

    def __init__(self, challenges_file):
        self.challences_file = challenges_file
        self.challenges = []
        self.__challenge_names_arr = None
        self.__existing_challenges_arr = None

    def sync(self):
        self.__load_ctfd_config()
        self.__parse_file()
        self.__remove_missing_challenges()
        self.__create_new_challenges()

    def get_challenges(self):
        self.__parse_file()

        return self.challenges

    def __load_ctfd_config(self):
        load_dotenv()
        load_dotenv(".env.local")
        self.ctfd_client = CTFdClient(
            os.getenv("CTFD_URL"), os.getenv("CTFD_ACCESS_TOKEN"))

    def __parse_file(self):
        with open(self.challences_file, "r") as file:
            lines = file.readlines()
        current_challenge = ""

        for line in lines:
            if self.CHALLENGE_PREFIX in line:
                challenge_name = line.split(
                    self.CHALLENGE_PREFIX)[1].strip()
                if current_challenge:
                    self.challenges.append(current_challenge)

                current_challenge = {
                    "name": challenge_name
                }

            if current_challenge:
                if self.DESCRIPTION_PREFIX in line:
                    current_challenge["description"] = line.split(
                        self.DESCRIPTION_PREFIX)[1].strip()

                if self.FLAG_PREFIX in line:
                    current_challenge["flag"] = line.split(
                        self.FLAG_PREFIX)[1].strip()

                if self.CATEGORY_PREFIX in line:
                    current_challenge["category"] = line.split(
                        self.CATEGORY_PREFIX)[1].strip()

        self.challenges.append(current_challenge)

    def __remove_missing_challenges(self):
        for challenge in self.__existing_challenges():
            if not challenge["name"] in self.__challenge_names():
                print("Challenge '{}' not found in given file, removing it..".format(
                    challenge["name"]))
                self.ctfd_client.delete_challenge(challenge["id"])

    def __existing_challenges(self):
        if not self.__existing_challenges_arr:
            self.__existing_challenges_arr = self.ctfd_client.get_challenges().json()[
                "data"]

        return self.__existing_challenges_arr

    def __challenge_names(self):
        if not self.__challenge_names_arr:
            self.__challenge_names_arr = [ch["name"] for ch in self.challenges]

        return self.__challenge_names_arr

    def __create_new_challenges(self):
        for challenge in self.challenges:
            existing_challenge = self.__existing_challenge(challenge["name"])
            if existing_challenge:
                print("Updating challenge '{}'".format(challenge["name"]))
                self.ctfd_client.update_challenge(existing_challenge["id"],
                                                  name=challenge["name"],
                                                  category=challenge.get(
                                                      "category") or None,
                                                  description=challenge.get(
                                                      "description") or None
                                                  )
            else:
                print("Creating challenge '{}'".format(challenge["name"]))
                created_challenge_response = self.ctfd_client.create_challenge(
                    **challenge)

                if created_challenge_response.status_code == 200:
                    challenge_data = created_challenge_response.json()["data"]

                    self.ctfd_client.add_flag(
                        challenge_data["id"], challenge["flag"])

    def __existing_challenge(self, challenge_name):
        for ch in self.__existing_challenges_arr:
            if challenge_name == ch["name"]:
                return ch

        return None
