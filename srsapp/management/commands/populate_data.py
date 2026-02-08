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

        self.stdout.write(self.style.SUCCESS("Successfully populated sample data"))
