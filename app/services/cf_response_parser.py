from collections import defaultdict
from app.models.user import User
from app.services.cf_request_handler import CFRequestHandler

class CFResponseParser:
    """Parse responses of Codeforces API."""
    
    user = User()  # <-- single shared user instance

    @staticmethod
    def parse():
        """Parse and make user object."""
        CFRequestHandler.make_request()
        CFResponseParser._parse_user_info(CFRequestHandler.user_info)
        CFResponseParser._parse_user_submission(CFRequestHandler.user_submission)
        CFResponseParser._parse_rating_changes(CFRequestHandler.rating_changes)
        return CFResponseParser.user

    @classmethod
    def _parse_user_info(cls, user_info):
        """Parse and set user's basic profile."""
        cls.user.name = user_info.get('firstName', '') + ' ' + user_info.get('lastName', '')
        cls.user.organization = user_info.get('organization', '')
        cls.user.rating = user_info.get('rating', 0)
        cls.user.rank = user_info.get('rank', 'newbie')
        cls.user.max_rating = user_info.get('maxRating', 0)
        cls.user.max_rank = user_info.get('maxRank', 'newbie')
        cls.user.contributions = user_info.get('contribution', 0)
        cls.user.registration_unix_time = user_info.get('registrationTimeSeconds', 0)

    @classmethod
    def _parse_user_submission(cls, user_submission):
        """Parse and save submission related details."""
        cls.user.submissions = len(user_submission)
        freq = defaultdict(int)
        for sb in user_submission:
            freq[sb.get('verdict', 'UNKNOWN')] += 1

        cls.user.accepted = freq['OK']
        cls.user.wrong_ans = freq['WRONG_ANSWER']
        cls.user.tle = freq['TIME_LIMIT_EXCEEDED']

    @classmethod
    def _parse_rating_changes(cls, rating_changes):
        """Sets total number of contests participated by the user."""
        cls.user.contests = len(rating_changes)


if __name__ == '__main__':
    user = CFResponseParser.parse()
    print(user)
