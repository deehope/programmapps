from flask import Flask
from lab_3.lab3_requests11 import lab3_requests11 

app = Flask(__name__)

app.register_blueprint(lab3_requests11)

@app.route("/")
@app.route("/index")
def labs():
    return '''
<!DOCTYPE html>
<body>
    <header>
        НГТУ, ФБИ-23. Разработка программных приложений
    </header>
    <main>
        <h1>Лабораторные работы</h1>
        <div>
        <a href="/number/">Лабораторная работа 3</a><br>
        </div>
    </main>
</body>
</html>
'''

if __name__ == '__main__':
    app.run(debug=True)