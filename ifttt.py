import requests

def email_alert(first, second, third):
    report = {}
    report["value1"] = first
    report["value2"] = second
    report["value3"] = third
    requests.post("https://maker.ifttt.com/trigger/mustafa/with/key/dF1S1xDUky_NZKhH7gEN4Y23ffn_uH4UnekZpjfmlnO", data=report)    
while 1:
    print("Choose your first string.")
    a = raw_input()
    print("Choose your second string.")
    b = raw_input()
    print("Choose your third string.")
    c = raw_input()
    email_alert(a, b, c)
