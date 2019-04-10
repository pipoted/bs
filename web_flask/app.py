from flask import Flask, render_template

app = Flask(__name__)


@app.route('/home')
def home_page():
    return render_template('home.html')


@app.route('/city/<city_name>')
def city_page(city_name):
    desc = 'test' + city_name
    return render_template('city_page.html', city_name=city_name, desc=desc)


@app.route('/lan/<lan_name>')
def lan_page(lan_name):
    desc = 'test' + lan_name
    return render_template('lan_page.html', lan_name=lan_name, desc=desc)


if __name__ == '__main__':
    app.run()
