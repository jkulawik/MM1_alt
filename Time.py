class Time:
    def __init__(self, practical, teoretical, confidence_interval):
        self.practical = practical
        self.teoretical = teoretical
        self.confidence_interval = confidence_interval

    def __str__(self): return f'teoretical: {self.teoretical} practical {self.practical} confidence {self.confidence_interval}'
