# imports
import socket
import json

def extractData(ledger):
    ledger = ledger['ledger']
    title = ledger['title']
    date = ledger['date']
    people = [person['name'] for person in ledger['people']]
    people = ', '.join(people)
    summary = ledger['summary']
    items = ledger['transactions']
    htmlTable = []
    for item in items:
        htmlTable.append(f"<tr><td>{item['item']}</td><td>{item['amount']}</td><td>{item['date']}</td><td>{item['paid_by']}</td></tr>")
    htmlTable = ''.join(htmlTable)

    return title, date, people, summary, htmlTable

def generateHTML(title, date, people, summary, table):
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
        <p>You have been sent a record of shared expenses between {people}. The following is a snapshop of that ledger from {date}</p>
        <table style="width:80%">
    <tr>
        <th>Item</th>
        <th>Amount</th>
        <th>Date</th>
        <th>Paid By</th>
    </tr>
    {table}
    </table>
    <p>Note that items with an " * " means they have been edited. Items with "del" have been removed from the summary.</p>
        <h2>Ledger summary: {summary}</h2>
    </body>
    </html>'''

    return html

# setup
HOST = "localhost"
PORT = 65432
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))

while True:
    server.listen(1)
    print(f'Server listening on port: {PORT} \n')
    commSocket, addr = server.accept()
    print(f'Connected by {addr} \n')

    dataLen = int(commSocket.recv(1024).decode())
    print(f'length of data to receive: {dataLen} \n')
    # LENGTH VERIFICATION
    commSocket.send(str(dataLen).encode())
    
    ledgerData = ''
    while True:
        data = commSocket.recv(1024).decode()
        ledgerData += data
        # print('in second while loop')
        if len(ledgerData) == dataLen:
            print(f'Server received: {ledgerData}\n')
            ledgerData = json.loads(ledgerData)

            title, date, people, summary, htmlTable = extractData(ledgerData)
            html = generateHTML(title, date, people, summary, htmlTable)

            commSocket.send(html.encode())
            print('sending html')
            commSocket.close()
            print('Connection closed.')
            break

        
    
