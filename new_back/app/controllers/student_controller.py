from ..models.student import Student

def get_student_by_id(student_id):
    return Student.query.get(student_id)