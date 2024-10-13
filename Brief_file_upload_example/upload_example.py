from flask import Flask, render_template, request
import re

app = Flask(__name__)

@app.route("/")
def init():
    return render_template("upload_example.html")

@app.route("/upload.cgi", methods=["POST"])
def uploader():
    data_bytes = request.get_data()

    f = open("uploaded_files/byte_dump", "wb")
    f.write(data_bytes)
    f.close()

    span_ = re.search(b'<NAME>(.*?)</NAME>', data_bytes)
    if span_:
        filename = span_.group(1)

    span_ = re.search(b'<SIZE>(.*?)</SIZE>', data_bytes)
    if span_:
        filesize = int(span_.group(1).decode('utf-8'))

    span_ = re.search(b'<BYTE>', data_bytes)
    if span_:
        bin_idx = span_.span()[1]

    print(filename, filesize, bin_idx)

    f = open("uploaded_files/" + filename.decode('utf-8'), "wb")
    f.write(data_bytes[bin_idx: bin_idx + filesize])
    f.close()

    return "Upload success"

if __name__ == "__main__":
    app.run(host="0.0.0.0")