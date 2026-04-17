from flask import request
from flask import jsonify
from werkzeug.utils import secure_filename
import threading, os

from app import app
from models import db,file_results

done = False
result = 0

ip = "localhost"


def parkinson_check(filename):
    from Parkinson.ParkinsonCheck import predict
    prediction = predict(filename)
    global result
    result = int(prediction[0])


@app.route('/')
def index():
    return "Apmycure Homepage"


def diagnose(filename):
    parkinson_check(filename)

    global done
    done = True

    os.remove(filename)

    file_result = file_results(filename, ip, result)
    db.session.add(file_result)
    db.session.commit()


@app.route('/upload', methods=['POST'])
def upload():
    f = request.files['file']
    filename = secure_filename(f.filename)
    f.save(filename)
    global done, ip
    done = False
    ip = str(request.remote_addr)
    diagnose_thread = threading.Thread(target=diagnose, args=[filename])
    diagnose_thread.daemon = True
    diagnose_thread.start()

    return "upload done"


@app.route('/done', methods=['POST', 'GET'])
def done_func():
    return "true" if done else "false"


@app.route('/getresult', methods=['POST', 'GET'])
def return_result():
    global done
    done = False
    return jsonify({"Parkinson": result})


@app.route('/history', methods=['GET', 'POST'])
def get_history():
    file_result = file_results.query.filter_by(ip=str(request.remote_addr)).all()
    return jsonify({"file_results": list(map(lambda x: {"filename": x.filename, "Parkinson": x.Presult}, file_result))})


if __name__ == '__main__':
    app.run()

