from collections import defaultdict
from app.models.user import User
from app.services.cf_request_handler import CFRequestHandler

class CFResponseParser:
    """Parse responses of Codeforces API."""

    @staticmethod
    def parse() -> User:
        """Parse API responses and return a User object."""
        CFRequestHandler.make_request()
        user_info = CFResponseParser._parse_user_info(CFRequestHandler.user_info)
        submissions = CFResponseParser._parse_user_submission(CFRequestHandler.user_submission)
        contests = CFResponseParser._parse_rating_changes(CFRequestHandler.rating_changes)

        user = User()
        # User info
        user.name = user_info.get('name', '')
        user.organization = user_info.get('organization', '')
        user.rating = user_info.get('rating', 0)
        user.rank = user_info.get('rank', 'newbie')
        user.max_rating = user_info.get('maxRating', 0)
        user.max_rank = user_info.get('maxRank', 'newbie')
        user.contributions = user_info.get('contribution', 0)
        user.registration_unix_time = user_info.get('registrationTimeSeconds', 0)

        # Submissions info
        user.submissions = submissions['total']
        user.accepted = submissions['OK']
        user.wrong_ans = submissions['WRONG_ANSWER']
        user.tle = submissions['TIME_LIMIT_EXCEEDED']

        # Contests info
        user.contests = contests

        return user

    @classmethod
    def _parse_user_info(cls, user_info):
        """Parse basic profile info."""
        return {
            'name': user_info.get('firstName', '') + ' ' + user_info.get('lastName', ''),
            'organization': user_info.get('organization', ''),
            'rating': user_info.get('rating', 0),
            'rank': user_info.get('rank', 'newbie'),
            'maxRating': user_info.get('maxRating', 0),
            'maxRank': user_info.get('maxRank', 'newbie'),
            'contribution': user_info.get('contribution', 0),
            'registrationTimeSeconds': user_info.get('registrationTimeSeconds', 0)
        }

    @classmethod
    def _parse_user_submission(cls, user_submission):
        """Parse submission verdicts."""
        freq = defaultdict(int)
        for sb in user_submission:
            freq[sb['verdict']] += 1
        return {
            'total': len(user_submission),
            'OK': freq['OK'],
            'WRONG_ANSWER': freq['WRONG_ANSWER'],
            'TIME_LIMIT_EXCEEDED': freq['TIME_LIMIT_EXCEEDED']
        }

    @classmethod
    def _parse_rating_changes(cls, rating_changes):
        """Return number of contests."""
        return len(rating_changes)


if __name__ == '__main__':
    user = CFResponseParser.parse()
    print(user.__dict__)
