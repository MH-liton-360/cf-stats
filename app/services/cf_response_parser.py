from collections import defaultdict
from app.models.user import User
from app.services.cf_request_handler import CFRequestHandler

class CFResponseParser:
    """Parse responses of Codeforces API."""

    @staticmethod
    def parse():
        CFRequestHandler.make_request()
        user = User()
        CFResponseParser._parse_user_info(CFRequestHandler.user_info, user)
        CFResponseParser._parse_user_submission(CFRequestHandler.user_submission, user)
        CFResponseParser._parse_rating_changes(CFRequestHandler.rating_changes, user)
        return user

    @staticmethod
    def _parse_user_info(user_info, user: User):
        user.name = user_info.get('firstName', '') + ' ' + user_info.get('lastName', '')
        user.organization = user_info.get('organization', '')
        user.rating = user_info.get('rating', 0)
        user.rank = user_info.get('rank', 'newbie')
        user.max_rating = user_info.get('maxRating', 0)
        user.max_rank = user_info.get('maxRank', 'newbie')
        user.contributions = user_info.get('contribution', 0)
        user.registration_unix_time = user_info.get('registrationTimeSeconds', 0)

    @staticmethod
    def _parse_user_submission(user_submission, user: User):
        user.submissions = len(user_submission)
        freq = defaultdict(int)
        for sb in user_submission:
            freq[sb['verdict']] += 1

        user.accepted = freq['OK']
        user.wrong_ans = freq['WRONG_ANSWER']
        user.tle = freq['TIME_LIMIT_EXCEEDED']

    @staticmethod
    def _parse_rating_changes(rating_changes, user: User):
        user.contests = len(rating_changes)
