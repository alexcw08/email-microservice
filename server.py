# imports
import socket
import json

# setup
HOST = "localhost"
PORT = 65432
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))


while True:
    server.listen(1)
    print(f'Server listening on port: {PORT}')
    print('')
    # receive connection
    commSocket, addr = server.accept()
    print(f"Connected by {addr}")
    print('')

    # receive ledger data
    dataMsg = commSocket.recv(1024).decode()

    print('Server received:', dataMsg)
    print('')
    # convert string to dictionary
    dataMsg = json.loads(dataMsg)
    # extract the necessary info from data
    title = dataMsg['ledger'][0]['title']
    date = dataMsg['ledger'][4]['date']
    people = []
    for person in dataMsg['ledger'][2]['persons']:
        people.append(person['name'])
    peopleString = ', '.join(people)
    summary = dataMsg['ledger'][1]['summary']
    items = dataMsg['ledger'][3]['items']
    htmlTable = []
    for item in items:
        htmlTable.append(f"<tr><td>{item['item']}</td><td>{item['amount']}</td><td>{item['date']}</td><td>{item['paid_by']}</td></tr>")
    htmlTable = ''.join(htmlTable)

    # f string containing the entire html
    html = f'''<!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Email</title>
    </head>
    <body>
        <h1>Subject: {title}</h1>
        <p>You have been sent a record of shared expenses between {peopleString}. The following is a snapshop of that ledger from {date}</p>
        <table style="width:80%">
    <tr>
        <th>Item</th>
        <th>Amount</th>
        <th>Date</th>
        <th>Paid By</th>
    </tr>
    {htmlTable}
    </table>
    <p>Note that items with an " * " means they have been edited. Items with "del" have been removed from the summary.</p>
        <h2>Ledger summary: {summary}</h2>
    </body>
    </html>'''
    # send html size and data
    htmlLen = str(len(html))
    print('sending length of html:', htmlLen)
    print('')
    commSocket.send(htmlLen.encode())
    commSocket.send(html.encode())
    print('sending html')
    commSocket.close()
    print('Connection closed.')