"""การตรวจสอบบัตรนักศึกษา"""
def main():
    """ logic """
    student_id = input()
    if len(student_id) >= 8 and student_id[2] == '1' and student_id[3] == '6':
        print("yes")
    else:
        print("no")

main()
