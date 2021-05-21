Run rsa_key.py using Python 3

python3 rsa_key.py

Program will not rewrite the generated public and private key files, you must delete/rename them to generate new ones.

I learnt about Rivest-Shamir-Adleman (RSA) encryption. It is a public-key cryptosystem tha tis widely used for secure data transmission. A public-key system is where the encryption key is public and the decryption key is private. A public-key is published based on two large prime numbers along with one auxiliary value. To hide the prime numbers, we hash it. It can be decoded only if someone knows the private key. In comparison to other algorithm it is slower. But it is secure if the key is large enough.

Two distinct prime numbers are chosen, their product is computed, the product is passed to Carmichael's totient function, LCM is calculated through the Euclidean algorithm. Then, an integer is chosen where the integer and the range of the Carmichael's totient function both are coprime. This integer is then released as part of the public key. The modular multiplicative inverse of the integer times modulo of Carmichael's totient function will be the private key and it is kept as secret (obviously).


