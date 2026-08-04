from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def similarity_score(resume_text, jd_text):
    tfidf = TfidfVectorizer()
    vectors = tfidf.fit_transform([resume_text, jd_text])
    score = cosine_similarity(vectors[0], vectors[1])
    return score[0][0]


def skill_match_score(resume_skills, jd_skills):
    resume_set = set(resume_skills)
    jd_set = set(jd_skills)

    matched_skills = resume_set.intersection(jd_set)

    if len(jd_set) == 0:
        return 0.0

    score = len(matched_skills) / len(jd_set)
    return round(score * 100, 2)


def calculate_final_score(context_score_raw, skill_score_percent):
    context_score_percent = context_score_raw * 100

    weight_skills = 0.70
    weight_context = 0.30

    final_score = (
        skill_score_percent * weight_skills
        + context_score_percent * weight_context
    )

    return round(final_score, 2)