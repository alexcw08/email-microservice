# imports
import json
import socket

# connecting
HOST = 'localhost'
PORT = 65432
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.connect((HOST, PORT))
print(f"Connected to server:{HOST}:{PORT}... \n")

# json to test with
ledgerJSON = {
    "ledger": {
        "title": "Second Ledger",
        "date": "2023-08-08",
        "people": [
            {
                "name": "Heath Ledger",
                "email": "hl@fakemail.com"
            },
            {
                "name": "Johanna W",
                "email": "jw@fakemail.com"
            },
            {
                "name": "James S.A. Corey",
                "email": "jsac@fakemail.com"
            }
        ],
        "summary": "Expense total: $3294.16\tTotal per person: $1098.05\nHeath Ledger owes $1087.8. Johanna W owes $848.05. James S.A. Corey is owed $1935.86. ",
        "transactions": [
            {
                "item": "First transaction",
                "amount": "10.25",
                "date": "2023-04-01*",
                "paid_by": "Heath Ledger"
            },
            {
                "item": "Little Purchase",
                "amount": "3000.21",
                "date": "2023-05-20",
                "paid_by": "James S.A. Corey"
            },
            {
                "item": "Mystery Items",
                "amount": "250.00",
                "date": "2023-06-08*",
                "paid_by": "Johanna W"
            },
            {
                "item": "Fourth Transaction",
                "amount": "33.70",
                "date": "2023-07-23",
                "paid_by": "James S.A. Corey"
            }
        ]
    }
}
# ledgerJSON = {
#     "ledger": [
#         {
#             "title": "Just cussin' around."
#         },
#         {
#             "summary": ""
#         },
#         {
#             "persons": [
#                 {
#                     "name": "Randy Marsh",
#                     "email": "randy@sp.com"
#                 },
#                 {
#                     "name": "Heath Ledger",
#                     "email": "hl@dk.com"
#                 },
#                 {
#                     "name": "Stanley Kubrick",
#                     "email": "sfk@movie.god.com"
#                 }
#             ]
#         },
#         {
#             "items": [
#                 {
#                     "item": "Go Karts",
#                     "amount": "350.00",
#                     "date": "2008-04-01",
#                     "paid_by": "Randy Marsh"
#                 },
#                 {
#                     "item": "Brewskies",
#                     "amount": "91.55",
#                     "date": "2008-04-01",
#                     "paid_by": "Heath Ledger"
#                 },
#                 {
#                     "item": "Hotdog Competition",
#                     "amount": "33.00",
#                     "date": "2008-10-20",
#                     "paid_by": "Stanley Kubrick"
#                 },
#                 {
#                     "item": "(del)L",
#                     "amount": "900,000.00",
#                     "date": "2009-06-02",
#                     "paid_by": "Stanley Kubrick"
#                 },
#                 {
#                     "item": "River Cruise",
#                     "amount": "1,900.00****",
#                     "date": "2011-10-19",
#                     "paid_by": "Stanley Kubrick"
#                 },
#                 {
#                     "item": "Video Games",
#                     "amount": "60.00",
#                     "date": "2012-08-30",
#                     "paid_by": "Heath Ledger"
#                 },
#                 {
#                     "item": "Brews",
#                     "amount": "32.00",
#                     "date": "2012-05-01",
#                     "paid_by": "Randy Marsh"
#                 },
#                 {
#                     "item": "Golf",
#                     "amount": "800.00",
#                     "date": "2013-07-26",
#                     "paid_by": "Heath Ledger"
#                 }
#             ]
#         },
#         {
#             "date": "2023-07-25"
#         }
#     ]
# }

ledgerStr = json.dumps(ledgerJSON)

ledgLen = str(len(ledgerStr))
print(f"Sending Ledger length to server: \n\t{ledgLen} \n")
clientSocket.send(ledgLen.encode())

# LENGTH VERIFICATION
lenVer = clientSocket.recv(1024).decode()

if lenVer == ledgLen:
    print(f"Sending Ledger to server\n\t{ledgerStr} \n")
    clientSocket.send(ledgerStr.encode())
    print("Sent Ledger to server successfully. \n")

    # RECEIVING HTML from SERVER
    html = ''
    while True:
        res = clientSocket.recv(2024).decode()
        html += res

        if not res:
            print(f'HTML received from server: {html} \n')
            # create email.html
            filename = 'email.html'
            file = open(filename, 'w')
            file.write(html)
            file.close()
            print('email.html has been created')
            break






