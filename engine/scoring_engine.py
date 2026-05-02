from config import WEIGHTS
class ScoringEngine:
    @staticmethod
    def calculate_final_score(scores_dict):
        final_score = (scores_dict['fundamental'] * WEIGHTS['fundamental'] +
                      scores_dict['technical'] * WEIGHTS['technical'] +
                      scores_dict['chip'] * WEIGHTS['chip'] +
                      scores_dict['news'] * WEIGHTS['news'])
        return round(final_score, 2)
