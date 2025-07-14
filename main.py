# from app.cv_parser import extract_cv_text
# from app.jd_parser import extract_jd_text
# from app.matcher import get_match_score
# import os

# def main():
#     jd_file = "uploads/jds/sample_jd.txt"
#     cv_folder = "uploads/cvs"

#     jd_text = extract_jd_text(jd_file)
#     results = []

#     for cv_file in os.listdir(cv_folder):
#         cv_path = os.path.join(cv_folder, cv_file)
#         try:
#             cv_text = extract_cv_text(cv_path)
#             score = get_match_score(cv_text, jd_text)
#             results.append((cv_file, round(score, 2)))
#         except Exception as e:
#             print(f"Failed to process {cv_file}: {e}")

#     results.sort(key=lambda x: x[1], reverse=True)
#     print("\nTop Candidates:")
#     for cv_name, score in results:
#         print(f"{cv_name}: {score}% match")

# if __name__ == "__main__":
#     main()



from app.routes import app

if __name__ == "__main__":
    app.run(debug=True)
