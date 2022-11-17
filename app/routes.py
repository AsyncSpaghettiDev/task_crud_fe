from flask import (
    Flask,
    request,
    render_template,
    redirect
)
import requests

BACKEND_URL = 'http://127.0.0.1:5000/tasks'
app = Flask(__name__)


@app.get("/")
def view_home():
    return render_template("index.html")


@app.get("/list")
def view_tasks():
    response = requests.get(BACKEND_URL).json()
    status = request.args.get('status')
    return render_template("list.html", tasks=response["tasks"], status=status)


@app.get("/task/<int:task_id>")
def get_single_task(task_id):
    url = f'{BACKEND_URL}/{task_id}'
    response = requests.get(url).json()
    return render_template("detail.html", task=response["task"])


@app.get("/task")
def view_create_task():
    return render_template("create.html")


@app.post("/task")
def create_task():
    data = request.form
    task_json = {
        "title": data["task_title"],
        "subtitle": data["task_subtitle"],
        "body": data["task_body"],
    }
    response = requests.post(BACKEND_URL, json=task_json)
    if response.status_code == 201:
        return redirect("/list?status=create_success")
    else:
        return redirect("/list?status=create_failure")


@app.get("/tasks/edit/<int:task_id>")
def edit_task(task_id):
    url = f'{BACKEND_URL}/{task_id}'
    response = requests.get(url).json()
    return render_template("edit.html", task=response["task"])


@app.post("/tasks/edit/<int:task_id>")
def update_task(task_id):
    url = f'{BACKEND_URL}/{task_id}'
    data = request.form
    task_json = {
        "title": data["title"],
        "subtitle": data["subtitle"],
        "body": data["body"],
        "active": data.get("active", False)
    }
    response = requests.put(url, json=task_json)
    if response.status_code == 204:
        return redirect("/list?status=update_success")
    else:
        return redirect("/list?status=update_failure")


@app.post("/tasks/<int:task_id>")
def delete_task(task_id):
    url = f'{BACKEND_URL}/{task_id}'
    response = requests.delete(url)
    if response.status_code == 204:
        return redirect("/list?status=delete_success")
    else:
        return redirect("/list?status=delete_failure")
