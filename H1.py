import hashlib
from time import time

class Block:
    def __init__(self, index, timestamp, data, previous_hash, nonce):
        """
        Khởi tạo các thuộc tính của khối
        """
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.hash = self.hashing()
 
    def hashing(self):
        """
        Tính giá trị băm của khối
        """
        key = hashlib.sha256()
        key.update(str(self.index).encode('utf-8'))
        key.update(str(self.timestamp).encode('utf-8'))
        key.update(str(self.data).encode('utf-8'))
        key.update(str(self.previous_hash).encode('utf-8'))
        key.update(str(self.nonce).encode('utf-8'))
        return key.hexdigest()
 
class Blockchain:
    def __init__(self):
        self.chain = []
        self.new_block(previous_hash='1', nonce=100, data="Genesis block")
 
    def valid_chain(self):
        """
        Kiểm tra chuỗi hợp lệ
        """
        flag = True
        for i in range(1, len(self.chain)):
            if self.chain[i].index != i+1:
                flag = False
                print(f'Trường index bị thay đổi tại khối {i}.')
            if self.chain[i-1].hash != self.chain[i].previous_hash:
                flag = False
                print(f'Trường previous hash bị thay đổi tại khối {i}.')
            if self.chain[i].hash != self.chain[i].hashing():
                flag = False
                print(f'Giá trị băm bị thay đổi tại khối {i}.')
            if self.proof_of_work(self.chain[i-1]) != self.chain[i].nonce:
                return False
 
        return flag
 
    def new_block(self, nonce, previous_hash, data):
        """
        Tạo thêm một khối trong chuỗi
        """
 
        block = Block(len(self.chain) + 1, time(), data, previous_hash, nonce)
        self.chain.append(block)
        return block
 
    def proof_of_work(self, last_block):
        """
        Thuật toán Proof of Work đơn giản
         - Tìm ra một số p' sao cho hàm băm hash(pp') trả về một giá trị băm chứa 4 số 0 ở đầu
         - p là giá trị nonce của khối trước và p' là giá trị nonce của khối mới
        """
 
        last_nonce = last_block.nonce
 
        nonce = 0
        while self.valid_nonce(last_nonce, nonce) is False:
            nonce += 1
 
        return nonce
 
    def valid_nonce(self, last_nonce, nonce):
        """
        Kiểm tra tính hợp lệ của nonce
        """
 
        guess = f'{last_nonce}{nonce}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"

    def get_chain_size(self):
        """
        Lấy ra kích thước của chuỗi
        """
        return len(self.chain)

    def last_block(self):
        """
        Lấy ra khối cuối cùng trong chuỗi
        """
        return self.chain[-1]

    def print_blockchain(self):
        """
        In ra chuỗi khối
        """
        i = 0
        for block in self.chain:
            print(f'--------------Block number {i+1}')
            print("Timestamp: ", block.timestamp)
            print("Data: ", block.data)
            print("previous hash: ", block.previous_hash)
            print("Hash: ", block.hash)
            print("nonce: ", block.nonce)
            i += 1
 
blockchain = Blockchain()
answer = 0
print("""1. Thêm khối
2. Hiển thị chuỗi khối
3. Kiểm tra chuỗi khối
4. Thoát""")
answer = 1
while answer != 4:
    number = int(input('Nhập lựa chọn: '))
    if number == 1:
        data = str(input("Nhập dữ liệu: "))
        last_block = blockchain.last_block()
        new_nonce = blockchain.proof_of_work(last_block)
        new_block = blockchain.new_block(new_nonce, last_block.hash, data)
        print("Đã thêm khối vào chuỗi!")
    elif number == 2:
        blockchain.print_blockchain()
    elif number == 3:
        if blockchain.valid_chain() == True:
            print("Chuỗi khối hợp lệ")
        else:
            print("Chuỗi khối không hợp lệ!")
            break
    else:
        answer = 4
