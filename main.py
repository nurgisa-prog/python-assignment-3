import os
import csv
import json
import sys

class FileManager:
    def __init__(self, filename):
        self.filename = filename

    def check_file(self):
        print("Checking file...")
        if os.path.exists(self.filename):
            print(f"File found: {self.filename}")
            return True
        else:
            print(f"Error: {self.filename} not found. Please download from LMS.")
            return False

    def create_output_folder(self, folder='output'):
        print("Checking output folder...")
        if not os.path.exists(folder):
            os.makedirs(folder)
            print(f"Output folder created: {folder}/")
        else:
            print(f"Output folder already exists: {folder}/")

class DataLoader:
    def __init__(self, filename):
        self.filename = filename
        self.students = []

    def load(self):
        print("\nLoading data...")
        try:
            with open(self.filename, mode='r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                self.students = list(reader)
            print(f"Data loaded successfully: {len(self.students)} students")
            return self.students
        except FileNotFoundError:
            print(f"Error: File '{self.filename}' not found.")
            return []

    def preview(self, n=5):
        print(f"\nFirst {n} rows:")
        print("-" * 35)
        for row in self.students[:n]:
            print(f"{row['student_id']} | {row['age']} | {row['gender']} | {row['country']} | GPA: {row['GPA']}")
        print("-" * 35)

class DataAnalyser:
    def __init__(self, students):
        self.students = students
        self.result = {}

    def analyse(self):
        country_counts = {}
        for row in self.students:
            try:
                float(row['GPA']) 
                c = row['country']
                country_counts[c] = country_counts.get(c, 0) + 1
            except ValueError:
                print(f"Warning: skip row {row.get('student_id')} due to invalid data.")
                continue

        sorted_c = sorted(country_counts.items(), key=lambda x: x[1], reverse=True)
        top_3 = sorted_c[:3]

        self.result = {
            "analysis": "Country Analysis",
            "total_students": len(self.students),
            "total_countries": len(country_counts),
            "top_3_countries": [{"country": c[0], "count": c[1]} for c in top_3],
            "all_countries": country_counts
        }
        return self.result

    def print_results(self):
        print("\n" + "-" * 35)
        print("Country Analysis")
        print("-" * 35)
        print(f"Total countries : {self.result['total_countries']}")
        print("Top 3 Countries:")
        for i, item in enumerate(self.result['top_3_countries'], start=1):
            print(f"{i}. {item['country']} : {item['count']}")
        print("-" * 35)

    def run_advanced_filters(self):
        print("\n" + "-" * 35)
        print("Lambda / Map / Filter")
        print("-" * 35)
        
        high_gpa = list(filter(lambda s: float(s['GPA']) > 3.5, self.students))
        print(f"GPA > 3.5 : {len(high_gpa)}")

        gpas = list(map(lambda s: float(s['GPA']), self.students))
        print(f"GPA values (first 5) : {gpas[:5]}")

        att_col = 'class_attendance_percent'
        if self.students and att_col in self.students[0]:
            good_att = list(filter(lambda s: float(s[att_col]) > 90, self.students))
            print(f"Attendance > 90% : {len(good_att)}")
        print("-" * 35)

class ResultSaver:
    def __init__(self, result, output_path):
        self.result = result
        self.output_path = output_path

    def save_json(self):
        try:
            with open(self.output_path, 'w', encoding='utf-8') as f:
                json.dump(self.result, f, indent=4, ensure_ascii=False)
            print(f"\nResult saved to {self.output_path}")
        except Exception as e:
            print(f"Error saving JSON: {e}")

def main():
    filename = "students.csv"
    output_path = "output/result.json"

    fm = FileManager(filename)
    if not fm.check_file():
        return
    fm.create_output_folder()

    dl = DataLoader(filename)
    data = dl.load()
    if not data: return
    dl.preview(n=5)

    analyser = DataAnalyser(data)
    analyser.analyse()
    analyser.print_results()
    analyser.run_advanced_filters()

    saver = ResultSaver(analyser.result, output_path)
    saver.save_json()

    print("\nTesting error handling for missing file:")
    test_dl = DataLoader("wrong_file.csv")
    test_dl.load()

if __name__ == "__main__":
    main()