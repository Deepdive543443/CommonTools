from flask import Flask, render_template, request
import re

app = Flask(__name__)

@app.route("/")
def init():
    return render_template("upload_example.html")

@app.route("/upload.cgi", methods=["POST"])
def uploader():
    data_bytes = request.get_data()

    span_ = re.search(b'<SIZE>(.*?)<NAME>', data_bytes)
    if span_:
        chunksize = int(span_.group(1).decode('utf-8'))

    span_ = re.search(b'<NAME>(.*?)<BYTE>', data_bytes)
    if span_:
        filename = span_.group(1)

    span_ = re.search(b'<BYTE>', data_bytes)
    if span_:
        bin_idx = span_.span()[1]

    f = open(filename.decode('utf-8'), "ab")
    f.write(data_bytes[bin_idx: bin_idx + chunksize])
    f.close()

    return "uploaded"

if __name__ == "__main__":
    app.run(host="0.0.0.0")