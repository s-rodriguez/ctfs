import base64
import os


def too_much_decode():
    joined_cnt = ''

    for f_path in os.listdir('./data'):
        with open('./data/' + f_path) as f:
            content = f.read()
            joined_cnt += content

    with open('joined_data', 'w') as w:
        w.write(joined_cnt)
    
    decode = base64.b64decode(content)
    with open('decoded_data.64', 'wb') as w:
        w.write(decode)
    

if __name__ == "__main__":
    too_much_decode()
