def send_mail(toaddr, my_subject, my_text, ccaddr=None):
    """
      Send an email to an address, with a subject and a text (can be a list) passed as argument.
      Using my.bot.pc@gmail.com
    """

    import smtplib
    import email.message

    fromaddr = 'my.bot.pc@gmail.com'
    username = 'my.bot.pc@gmail.com'
    password = 'ienid8Ah'

    server = smtplib.SMTP('smtp.gmail.com', 587, timeout=120)
    server.ehlo()
    server.starttls()

    server.login(username,password)

    msg = email.message.Message()
    msg.set_charset("ISO-8859-16")
    msg['From'] = fromaddr
    msg['To'] = toaddr
    if ccaddr:
        msg['Cc'] = ccaddr
    msg['Subject'] = my_subject
    if ccaddr:
        toaddr = [toaddr] + [ccaddr]

    body = my_text.encode("ISO-8859-16")
    msg.set_payload(body)
    import pdb; pdb.set_trace()
    server.sendmail(fromaddr, toaddr, msg.as_string())
    server.quit()

def send_html_email(toaddr, my_subject, my_html_template, my_text, ccaddr=None):
    """
      Send an html email to an address, with a subject and a text passed as argument.
      Using my.bot.pc@gmail.com
    """

    import smtplib

    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText

    fromaddr = 'my.bot.pc@gmail.com'
    username = 'my.bot.pc@gmail.com'
    password = 'ienid8Ah'

    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('alternative')
    msg['From'] = fromaddr
    msg['To'] = toaddr
    if ccaddr:
        msg['Cc'] = ccaddr
    msg['Subject'] = my_subject

    if ccaddr:
        toaddr = [toaddr] + [ccaddr]

    # Create the body of the message (a plain-text and an HTML version).
    html = open(my_html_template, 'r')
    message = html.read().format(text= my_text)
    # Record the MIME types of both parts - text/plain and text/html.
    part2 = MIMEText(message, 'html')

    server = smtplib.SMTP('smtp.gmail.com', 587, timeout=120)
    server.ehlo()
    server.starttls()
    server.login(username, password)
    msg.set_payload(part2)
    server.sendmail(fromaddr, toaddr, msg.as_string())
    server.quit()


# --------------------
# TESTS
# --------------------
if __name__ == '__main__':

    main_message = """<table>\n    <tr>\n        <th>Key</th>\n        <th>Value</th>\n    </tr>\n    <tr>\n        <td>date_mise_en_ligne</td>\n        <td>Mise en ligne le 4 mars à 13:49</td>\n    </tr>\n    <tr>\n        <td>vendeur</td>\n        <td>Pro Immobilier Century 21 Etude Saint-Seurin Numéro SIREN : 527600043</td>\n    </tr>\n    <tr>\n        <td>Prix</td>\n        <td>430 000\xa0€</td>\n    </tr>\n    <tr>\n        <td>Ville</td>\n        <td>Bordeaux 33100</td>\n    </tr>\n    <tr>\n        <td>Frais d&#x27;agence inclus</td>\n        <td>Oui</td>\n    </tr>\n    <tr>\n        <td>Type de bien</td>\n        <td>Appartement</td>\n    </tr>\n    <tr>\n        <td>Pièces</td>\n        <td>4</td>\n    </tr>\n    <tr>\n        <td>Surface</td>\n        <td>107 m 2</td>\n    </tr>\n    <tr>\n        <td>GES</td>\n        <td>A (moins de 5)</td>\n    </tr>\n    <tr>\n        <td>Classe énergie</td>\n        <td>B (de 51 à 90)</td>\n    </tr>\n    <tr>\n        <td>URL</td>\n        <td>https://www.leboncoin.fr/ventes_immobilieres/1078300305.htm?ca=2_s</td>\n    </tr>\n</table>"""
    main_message = main_message + '\n' + 'Coucou'
    import pdb; pdb.set_trace()
    send_html_email("constant.pierre@gmail.com",
                    "bot test html",
                    r'C:\Users\Constant\PycharmProjects\1702_bot_LBC\email_template.html',
                    main_message)
    #send_mail("constant.pierre@gmail.com", "bot test 2", main_message)