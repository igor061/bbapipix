import re
import subprocess


def load_server_certificates(server):
    command = [
        'openssl',
        's_client',
        '-showcerts',
        '-servername',
        server,
        #'-starttls',
        '-connect',
        f'{server}:443',
        #'-key', 'bb_srgold_pvt.pem', '-cert', 'bb_srgold_cer.pem',
        #'-key', 'private_key.pem',  '-cert',  'cert.pem'
    ]
    print(command)

    process = subprocess.Popen(command, stdout=subprocess.PIPE, text=True)

    # Leia a saída do processo linha a linha
    buffer = ""
    for line in process.stdout:
        print(line, end='')
        buffer += line
        if "SSL handshake has read" in line:
            break

    # Encerre o processo (você pode escolher 'terminate()' ou 'kill()')
    process.terminate()  # Encerra suavemente

    # Espere pelo processo ser encerrado
    process.wait()

    #print(buffer)
    certificados = re.findall(r'(-----BEGIN CERTIFICATE-----\n.*?\n-----END CERTIFICATE-----)', buffer, re.DOTALL)

    with open(f'{server}.cer', 'w') as f:
        for certificado in certificados:
            print(certificado)
            f.write(certificado)
            f.write('\n')


if __name__ == '__main__':
    load_server_certificates('api-pix.bb.com.br')