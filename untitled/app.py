from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def hello_world():
    if request.method == "POST":
        print('test')
        return render_template('test.html')
    else:
        return render_template('test.html')



if __name__ == '__main__':
    app.run()
