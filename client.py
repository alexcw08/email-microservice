# imports
import json
import socket

# connecting
HOST = 'localhost'
PORT = 65432
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.connect((HOST, PORT))
print(f"Connected to server:{HOST}:{PORT}...")
print('')

# json to test with
ledgerJSON = {
    "ledger": [
        {
            "title": "Just cussin' around."
        },
        {
            "summary": ""
        },
        {
            "persons": [
                {
                    "name": "Randy Marsh",
                    "email": "randy@sp.com"
                },
                {
                    "name": "Heath Ledger",
                    "email": "hl@dk.com"
                },
                {
                    "name": "Stanley Kubrick",
                    "email": "sfk@movie.god.com"
                }
            ]
        },
        {
            "items": [
                {
                    "item": "Go Karts",
                    "amount": "350.00",
                    "date": "2008-04-01",
                    "paid_by": "Randy Marsh"
                },
                {
                    "item": "Brewskies",
                    "amount": "91.55",
                    "date": "2008-04-01",
                    "paid_by": "Heath Ledger"
                },
                {
                    "item": "Hotdog Competition",
                    "amount": "33.00",
                    "date": "2008-10-20",
                    "paid_by": "Stanley Kubrick"
                },
                {
                    "item": "(del)L",
                    "amount": "900,000.00",
                    "date": "2009-06-02",
                    "paid_by": "Stanley Kubrick"
                },
                {
                    "item": "River Cruise",
                    "amount": "1,900.00****",
                    "date": "2011-10-19",
                    "paid_by": "Stanley Kubrick"
                },
                {
                    "item": "Video Games",
                    "amount": "60.00",
                    "date": "2012-08-30",
                    "paid_by": "Heath Ledger"
                },
                {
                    "item": "Brews",
                    "amount": "32.00",
                    "date": "2012-05-01",
                    "paid_by": "Randy Marsh"
                },
                {
                    "item": "Golf",
                    "amount": "800.00",
                    "date": "2013-07-26",
                    "paid_by": "Heath Ledger"
                }
            ]
        },
        {
            "date": "2023-07-25"
        }
    ]
}

# convert to string
ledgerStr = json.dumps(ledgerJSON)

# SENDING TO SERVER
print(f"Sending Ledger to server\n\t{ledgerStr}")
clientSocket.send(ledgerStr.encode())
print('')
print("Sent Ledger to server successfully.")

# RECEIVING HTML from SERVER
html = ''
while True:
    res = clientSocket.recv(2024).decode()
    html += res

    if not res:
        print('')
        print('HTML received from server:', html)
        # create email.html
        filename = 'email.html'
        file = open(filename, 'w')
        file.write(html)
        file.close()
        print('')
        print('email.html has been created')
        break






