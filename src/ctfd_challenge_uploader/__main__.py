from ctfd_challenge_uploader.challenges import Challenges
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Send challenges to CTFd')
    parser.add_argument('challenges_file', metavar='challenges_file',
                        help='File where challenges are being described')

    args = parser.parse_args()
    challenges = Challenges(args.challenges_file)
    challenges.sync()
