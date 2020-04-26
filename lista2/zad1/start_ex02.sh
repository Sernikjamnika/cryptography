#bin/bash
python3 main.py --keystore_path aes-keystore.jck --keystore_pass mystorepass --key-id jceksaes --key-pass mykeypass --iv 2137832583667307 --mode oracle --encryption-type CBC --input-files m.txt
python3 xor.py --previous-iv 2137832583667307 --current-iv 2137832583667308 --output-path xored.txt
python3 main.py --keystore_path aes-keystore.jck --keystore_pass mystorepass --key-id jceksaes --key-pass mykeypass --iv 2137832583667308 --mode challenge --encryption-type CBC --input-files xored.txt random_message.txt
cmp --silent "encrypted_message.txt" "encrypted_m.txt" && echo "xored.txt" || echo "random_message.txt"
