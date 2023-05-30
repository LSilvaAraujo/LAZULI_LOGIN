import yagmail


def fale_conosco():
    # Initialize yagmail with your email account
    yag = yagmail.SMTP('atendimentocliente.lazuli@gmail.com')

    # Compose the email
    subject = "Hello from yagmail"
    content = "This is the body of the email."
    to = "atendimentocliente.lazuli@gmail.com"

    # Send the email
    yag.send(to, subject, content)

    # Close the connection
    yag.close()

fale_conosco()