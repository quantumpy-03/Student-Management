import random
from django.core.management.base import BaseCommand
from srsapp.models import Course, Subjects, Student
from datetime import date


class Command(BaseCommand):
    help = "Populates the database with sample data"

    def handle(self, *args, **kwargs):
        self.stdout.write("Populating data...")

        # Create Courses
        courses_data = [
            ("CSE", "Computer Science Engineering"),
            ("ME", "Mechanical Engineering"),
            ("ECE", "Electronics and Communication"),
            ("BCA", "Bachelor of Computer Applications"),
            ("MCA", "Master of Computer Applications"),
        ]

        courses = []
        for short, full in courses_data:
            course, created = Course.objects.get_or_create(
                courseshortname=short, defaults={"coursefullname": full}
            )
            courses.append(course)
            if created:
                self.stdout.write(f"Created Course: {full}")

        # Create Subjects for each course
        subjects_list = []
        for course in courses:
            if not Subjects.objects.filter(course_id=course).exists():
                subj = Subjects.objects.create(
                    course_id=course,
                    subject1=f"{course.courseshortname} 101",
                    subject2=f"{course.courseshortname} 102",
                    subject3=f"{course.courseshortname} 103",
                    subject4=f"{course.courseshortname} 104",
                    subject5=f"{course.courseshortname} 105",
                )
                subjects_list.append(subj)
                self.stdout.write(f"Created Subjects for {course.coursefullname}")
            else:
                subjects_list.append(Subjects.objects.get(course_id=course))

        # Create Students
        first_names = [
            "Aarav",
            "Vivaan",
            "Aditya",
            "Vihaan",
            "Arjun",
            "Sai",
            "Reyansh",
            "Ayaan",
            "Krishna",
            "Ishaan",
            "Diya",
            "Saanvi",
            "Anya",
            "Aadhya",
            "Pari",
            "Ananya",
            "Myra",
            "Riya",
            "Kiara",
            "Ira",
        ]
        last_names = [
            "Sharma",
            "Verma",
            "Gupta",
            "Malhotra",
            "Bhatia",
            "Mehta",
            "Joshi",
            "Nair",
            "Patel",
            "Reddy",
            "Singh",
            "Kumar",
            "Das",
            "Roy",
            "Chopra",
        ]
        cities = [
            "Mumbai",
            "Delhi",
            "Bangalore",
            "Hyderabad",
            "Chennai",
            "Kolkata",
            "Pune",
            "Jaipur",
        ]

        for i in range(20):
            course = random.choice(courses)
            subject = Subjects.objects.get(
                course_id=course
            )  # Assuming one subject set per course for simplicity here

            fname = random.choice(first_names)
            lname = random.choice(last_names)

            Student.objects.create(
                course_id=course,
                subjects_id=subject,
                roll_number=random.randint(100000, 999999),
                session="2025-2026",
                fname=fname,
                mname="",
                lname=lname,
                gender=random.choice(["Male", "Female"]),
                gname=f"Mr. {lname}",
                ocp="Private",
                income="500000",
                category="General",
                ph="No",
                nation="Indian",
                mobno=f"9{random.randint(100000000, 999999999)}",
                email=f"{fname.lower()}.{lname.lower()}@example.com",
                country="India",
                state="Maharashtra",  # Simplified
                city=random.choice(cities),
                padd="Sample Address",
                cadd="Sample Address",
                class1="10th",
                board1="CBSE",
                roll1=str(random.randint(10000, 99999)),
                pyear1="2023",
                class2="12th",
                board2="CBSE",
                roll2=str(random.randint(10000, 99999)),
                pyear2="2025",
                sub1=f"{course.courseshortname} Core",
                marks1=random.randint(60, 99),
                fmarks1=100,
                sub2="Elective",
                marks2=random.randint(60, 99),
                fmarks2=100,
            )

        self.stdout.write(self.style.SUCCESS("Successfully populated sample data"))
