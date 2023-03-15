from flask import Flask, render_template, url_for, request, redirect
import random
import os

app = Flask(__name__)

is_game_over = False
selected_name = ""
score = 0
wrong_answer = 0
message = ""

names_list = os.listdir(os.path.join(app.static_folder, "images"))
random.shuffle(names_list)


@app.route('/', methods=["GET", "POST"])
def index():
    global selected_name, score, message, wrong_answer, names_list, is_game_over
    options = []

    if request.method == "POST":

        if request.form["option"] == selected_name:
            message = "Good job! You got it right!"
            score += 1

        else:
            message = "Sorry, you are wrong :("
            wrong_answer += 1

        return redirect(url_for("index"))

    else:

        try:
            selected_name = names_list[score].split(".")[0]

        except IndexError:
            return render_template("index.html", wrong_answer=wrong_answer, is_game_over=True, score=score)

        else:
            options.append(selected_name)
            for num in range(3):
                name = random.choice(names_list).split(".")[0]
                while name in options:
                    name = random.choice(names_list).split(".")[0]
                options.append(name)
            random.shuffle(options)

    return render_template("index.html", selected_name=selected_name, options=options, score=score, message=message,
                           wrong_answer=wrong_answer, names_list=names_list, is_game_over=is_game_over)


@app.route('/secret')
def secret():
    return render_template("secret.html")


app.run(host='0.0.0.0', port=81)