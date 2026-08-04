
def generate_course_links(skills):
    course_links = {}

    for skill in skills:
        query = skill.replace(" ", "+")
        
        course_links[skill] = {
            "Coursera": f"https://www.coursera.org/search?query={query}",
            "Udemy": f"https://www.udemy.com/courses/search/?q={query}",
            "YouTube": f"https://www.youtube.com/results?search_query={query}",
            "NPTEL": f"https://nptel.ac.in/courses?search_query={query}"
        }

    return course_links

def get_top_missing_skills(missing_skills, n=3):
    return list(missing_skills)[:n]
