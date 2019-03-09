"""A web application for tracking projects, students, and student grades."""

from flask import Flask, request, render_template, redirect 

import hackbright

app = Flask(__name__)


@app.route("/student")
def get_student():
    """Show information about a student."""

    github = request.args.get('github')

    first, last, github = hackbright.get_student_by_github(github)

    if first == None: 
        # flash("Student not in database")
        return redirect("/student-add")

    list_student_grades = hackbright.get_grades_by_github(github)

    # return "{} is the GitHub account for {} {}".format(github, first, last)

    html = render_template("student_info.html",
                           first=first,
                           last=last,
                           github=github,
                           list_student_grades = list_student_grades)
    return html

@app.route("/student-search")
def get_student_form():
    """Show form for searching for a student."""

    return render_template("student_search.html")


@app.route("/student-add")
def student_add_form():
    """Add a student."""

    return render_template("student_add.html")


@app.route("/student-add", methods=['POST'])
def student_add():
    """Add a student and redirect to /student"""
    github = request.form.get('github')
    first_name = request.form.get('fname')
    last_name = request.form.get('lname')

    hackbright.make_new_student(first_name, last_name, github)

    html = render_template("student_added.html",
                           first=first_name,
                           last=last_name,
                           github=github)
    return html


@app.route("/project")
def display_project():
    """Display project title, desscription, max_grade"""
    project = request.args.get('project')
    title, description, max_grade = hackbright.get_project_by_title(project)
    list_stident_grades = hackbright.get_grades_by_title(title)



    return render_template("project_info.html",
                            title = title,
                            description = description,
                            max_grade = max_grade, 
                            list_stident_grades = list_stident_grades)

@app.route("/homepage")
def display_homepage():
    """Homepage with list of projects and students"""
    students = hackbright.get_students()

    projects = hackbright.get_projects()

    return render_template("homepage.html",
                            students = students,
                            projects = projects)

if __name__ == "__main__":
    hackbright.connect_to_db(app)
    app.run(debug=True)
