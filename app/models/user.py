class User:
    name: str = ''
    organization: str = ''
    rating: int = 0
    rank: str = 'newbie'
    max_rating: int = 0
    max_rank: str = 'newbie'
    contributions: int = 0
    registration_unix_time: int = 0

    submissions: int = 0
    accepted: int = 0
    wrong_ans: int = 0
    tle: int = 0

    contests: int = 0

    # singleton instance
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(User, cls).__new__(cls)
        return cls._instance
