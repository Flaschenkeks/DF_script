import os

from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import unpad


def extract_first_and_last_16_bytes(file_path):
    with open(file_path, "rb") as file:
        # Extract the first 16 bytes
        first_16_bytes = file.read(16)

        # Move the file cursor to the end and extract the last 16 bytes
        file.seek(-16, 2)
        last_16_bytes = file.read(16)

    return first_16_bytes, last_16_bytes

def decrypt_file(input_file, output_file, key, iv):
    with open(input_file, 'rb') as file:
        encrypted_data = file.read()

    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted_data = unpad(cipher.decrypt(encrypted_data), 16)

    os.makedirs(os.path.dirname(output_file), exist_ok=True)  # Create output directory if it doesn't exist

    with open(output_file, 'wb') as decrypted_file:
        decrypted_file.write(decrypted_data)

def decrypt_files_in_directory(directory, output_directory, key, iv):
    for filename in os.listdir(directory):
        input_file_path = os.path.join(directory, filename)
        output_file_path = os.path.join(output_directory, f"decrypted(0)_{filename[:-8]}")

        decrypt_file(input_file_path, output_file_path, key, iv)


def decrypt_files_recursiv_in_directory(directory, output_directory, key, iv):
    for root, dirs, files in os.walk(directory):
        for filename in files:
            input_file_path = os.path.join(root, filename)
            relative_path = os.path.relpath(input_file_path, directory)

            relative_path = relative_path.replace("\\", "/")

            output_file_path = os.path.join(output_directory, f"decrypted_{relative_path[:-8]}")

            decrypt_file(input_file_path, output_file_path, key, iv)

# def decrypt_files_recursiv_in_directory(directory, output_directory, key, iv):
#     for root, dirs, files in os.walk(directory):
#         for filename in files:
#             input_file_path = os.path.join(root, filename)
#             relative_path = os.path.normpath(input_file_path, directory)
#             output_file_path = os.path.normpath(output_directory, f"decrypted_{relative_path[:-8]}")
#
#             decrypt_file(input_file_path, output_file_path, key, iv)

if __name__ == "__main__":
    # Replace "path/to/your/file" with the actual path to your file
    file_path = "keys/decryption-data"

    # Call the function to extract bytes
    first_bytes, last_bytes = extract_first_and_last_16_bytes(file_path)



    #hex hex
    hex_representation_first = first_bytes.hex()
    hex_representation_last = last_bytes.hex()
    # Display or use the extracted bytes     print("First 16 bytes:", first_bytes)
    print(hex_representation_first)
    print("Last 16 bytes:", last_bytes)
    print(hex_representation_last)
    print("Last 16 bytes:", bytes.fromhex(hex_representation_last))



   # output_file_path = 'decrypt/mechanimals-project-omega-render-3.png'
    iv = first_bytes
    key = last_bytes

    input_file_path = 'files/mechanimals-project-omega-render-3.png.DOGEDOG'
    output_file_path = "decrypt" + input_file_path[5:-8]
    #print(output_file_path)
 #   decrypt_file(input_file_path, output_file_path, key, iv)

    input_file_path = 'files/current-employees.xlsx.DOGEDOG'
    output_file_path = "decrypt" + input_file_path[5:-8]
#    decrypt_file(input_file_path, output_file_path, key, iv)

    input_file_path = 'files/mechanimals-project-sing-prototype-3.png.DOGEDOG'
    output_file_path = "decrypt" + input_file_path[5:-8]
#    decrypt_file(input_file_path, output_file_path, key, iv)

input_directory =  'files/mechanimals-share'
output_directory = 'decrypt' + input_directory[5:]
decrypt_files_recursiv_in_directory(input_directory, output_directory, key, iv)

#
# input_directory =  'files/mechanimals-share/product-development'
# output_directory = 'decrypt' + input_directory[5:]
# decrypt_files_recursiv_in_directory(input_directory, output_directory, key, iv)
#
# input_directory =  'files/mechanimals-share/product-development-privileged'
# output_directory = 'decrypt' + input_directory[5:]
# decrypt_files_recursiv_in_directory(input_directory, output_directory, key, iv)
#
# input_directory =  'files/mechanimals-share/mechanimals-organization'
# output_directory = 'decrypt' + input_directory[5:]
# decrypt_files_recursiv_in_directory(input_directory, output_directory, key, iv)
#
# input_directory =  'files/mechanimals-share/it-stuff'
# output_directory = 'decrypt' + input_directory[5:]
# decrypt_files_recursiv_in_directory(input_directory, output_directory, key, iv)